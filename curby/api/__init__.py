from uuid import uuid4

from curby.core import (
    FrameMetadata, 
    Song, 
    SongCompilationThread, 
    SongCompilationTask, 
    TaskStatus,
)
from curby.gather.binder import get_song
from curby.gather.service import billboardservice
from curby.generate import generate_compilation
from curby.error import (
    BillboardError,
    SongBinderError
)

from fastapi import HTTPException

tasks : dict[str, SongCompilationTask] = {}

async def create_songcompilation(theme: FrameMetadata):    
    try:
        songs: list[tuple[str, str]] = billboardservice.get_popular()
        all_songs: list[Song] = [get_song(author, title) for author, title in songs]

        task_id: str = str(uuid4())

        thread = SongCompilationThread(
            lambda : on_songcompilation_ended(task_id), 
            target=generate_compilation, 
            args=(theme, all_songs, )
        )

        task = SongCompilationTask(task_id, TaskStatus.QUEUED, thread)
        
        tasks[task_id] = task
        tasks[task_id].thread.start()
        tasks[task_id].status = TaskStatus.PROCESSING

        return { "task_id" : task_id }
    except BillboardError as error:
        print(error)
        raise HTTPException(status_code=400, detail= "scrapping error occured")
    except SongBinderError as error:
        print(error)
        raise HTTPException(status_code=400, detail= "song creationg error occured")
    except Exception as error:
        print(error)
        raise HTTPException(status_code=400, detail= "couldnt create task")

async def songcompilation_status(task_id: str):
    try:
        task: SongCompilationTask = tasks.get(task_id)
        return { "task_status" : task.status }
    except Exception as error:
        print(error)
        raise HTTPException(status_code=400, detail=f"couldnt find task {task_id}")

async def songcompilation_status_global():
    try:
        statuses = {}
        for uuid, task in tasks.items():
            if task.status in statuses:
                statuses[task.status] += 1
            else:
                statuses[task.status] = 1
        return statuses
    except Exception as error:
        print(error)
        raise HTTPException(status_code=418, detail=f"coffee time !")

def on_songcompilation_ended(task_id: str):
    tasks[task_id].status = TaskStatus.FINISHED
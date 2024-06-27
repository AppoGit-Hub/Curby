from uuid import uuid4

from curby.core import (
    FrameMetadata, 
    Song, 
    SongCompilationThread, 
    SongCompilationTask, 
    TaskStatus
)
from curby.gather.binder import get_song
from curby.gather.controller import billboardcontroller
from curby.generate import generate_compilation

tasks : dict[str, SongCompilationTask] = {}

async def create_songcompilation(theme: FrameMetadata):    
    try:
        songs: list[tuple[str, str]] = billboardcontroller.get_popular()
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

        return { "status" : "succes", "message" : "compilation task created", "task_id" : task_id}
    except Exception as error:
        print(error)
        return { "status" : "error", "message" : "couldnt create task" }

async def songcompilation_status(task_id: str):
    try:
        task: SongCompilationTask = tasks.get(task_id)
        return { "status" : "succes", "message" : f"got status of task {task_id}", "task_status" : task.status}
    except Exception as error:
        print(error)
        return { "status" : "error", "message" : f"couldnt find task {task_id}" }

async def songcompilation_status_global():
    statuses = {}
    for uuid, task in tasks.items():
        if task.status in statuses:
            statuses[task.status] += 1
        else:
            statuses[task.status] = 1
    return statuses

def on_songcompilation_ended(task_id: str):
    tasks[task_id].status = TaskStatus.FINISHED
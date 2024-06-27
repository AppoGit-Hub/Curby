from fastapi import FastAPI

from curby.core import FrameMetadata
import curby.api as api

app = FastAPI()

@app.get("/")
def get_root():
    return {"test": "root"}

@app.post("/create/songcompilation/")
async def create_compilation(theme: FrameMetadata):        
    return await api.create_songcompilation(theme)

@app.get("/status/songcompilation/{task_id}")
async def songcompilation_status(task_id: str):
    return await api.songcompilation_status(task_id)

@app.get("/status/global/songcompilation/")
async def songcompilation_status_global():
    return await api.songcompilation_status_global()
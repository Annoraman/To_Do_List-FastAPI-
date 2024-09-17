from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID, uuid4

app = FastAPI() #create instance of FastAPI

class Task(BaseModel):
    id : Optional[UUID] = None
    title : str
    descrition : Optional[str] = None
    completed : bool = False

tasks =[] #empty list to store task data instead of database table.    


@app.post("/tasks/", response_model=Task)
def Add_task(task:Task):
    task.id = uuid4()
    tasks.append(task)
    print(Task)
    return task

    
@app.get("/tasks/", response_model=List[Task]) #decorator of router that handle get reqest
def read_tasks():     #router function
    return tasks


@app.get("/tasks/{task_id}", response_model=Task )
def read_tasks(task_id:UUID):
    for task in tasks:
        if task_id == task.id:
            return task
    raise HTTPException(status_code=404, detail="task is not found!")
    
    
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: UUID, task_update:Task):
    for idx,task in enumerate(tasks):
        if task.id == task_id :
            updated_task= task.copy(update = task_update.dict(exclude_unset=True))
            tasks[idx] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="task is not found")


@app.delete("/tasks/{task_id}", response_model= Task)
def delete_task(task_id: UUID)  :
    for idx, task in enumerate(tasks):
         if task.id == task_id:
            return tasks.pop(idx)
    raise HTTPException(status_code=404, detail="task is not found")


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app,host="127.0.0.1", port= 8000 )
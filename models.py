from pydantic import BaseModel

class Todo(BaseModel):
    task: str  # field to store task name
    description: str  # field to store task description

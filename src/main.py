from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi import Request, Response
from pydantic import BaseModel
from repository import Repository
from logging import getLogger, INFO

load_dotenv()

logger = getLogger(__name__)
logger.setLevel(INFO)

# This schema is needed for POST request - /create endpoint
class Task(BaseModel):
    description: str
    user: str
    category: str

# Define the app
app = FastAPI(
    title="MyApp",
    description="Hello API developer!",
    version="0.1.0"
)

# Initialize repository
repository = Repository(logger)

# API for health check of App
@app.get("/")
async def main(request: Request):
    
        logger.info("Hello World endpoint was reached. . .")
        return {"message": "Hello World"}

# API to get all the data from ToDo list
@app.get("/all")
async def main(request: Request):  # noqa: F811
        logger.info("Get all tasks endpoint was reached. . . validating the scope of request. . .")
        try:
            print('get_all_tasks endpoint was reached. . .')
            tasks =  await repository.get_all()
            return tasks
        except Exception as ex:
            logger.error(ex)
            return Response(content=str(ex), status_code=500)


# API to submit data to ToDo list
@app.post("/create")
async def submit(task: Task):
        logger.info("/create endpoint was reached. . .")
        
        try:
            await repository.add_task(task.description, task.user, task.category)
            return {"message": "Data submitted successfully"}
        except Exception as ex:
            logger.error(ex)
            return Response(content=str(ex), status_code=500)
        

# API to mark a task as 'Completed'
@app.post("/done")
async def complete(task_id: int, request: Request):
    
        logger.info("/done endpoint was reached. . .")
        try:
            await repository.update_task_status(task_id)
            return {"message": "Task marked as completed successfully"}
        except Exception as ex:
            logger.error(ex)
            return Response(content=str(ex), status_code=500)
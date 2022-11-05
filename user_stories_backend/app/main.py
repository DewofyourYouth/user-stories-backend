from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .resources import project

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(project.router)


@app.get("/")
def app_is_running():
    return {"message": "The app is running"}

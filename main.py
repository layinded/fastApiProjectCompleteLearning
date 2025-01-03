from fastapi import FastAPI
from routers import admin, todos, auth, users
import models
from database import engine
from starlette.staticfiles import StaticFiles

app = FastAPI()


@app.get("/status-checker")
def status_checker():
    return {"status": "ok"}


models.Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


def mount_path(app: FastAPI, path: str) -> None:
    app.mount("/", StaticFiles(directory=path))

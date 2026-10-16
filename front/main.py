from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI


def mount_path(app: FastAPI, path: str) -> None:
    app.mount("/", StaticFiles(directory=path))

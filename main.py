from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_test() -> dict[str, str]:
    return {"Hello": "World"}

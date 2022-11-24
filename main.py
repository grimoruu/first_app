from fastapi import FastAPI

app = FastAPI()


@app.get("/student/")
def students():
    return {"status": "success"}


@app.get("/")
def root():
    return {"message": "Hello World"}

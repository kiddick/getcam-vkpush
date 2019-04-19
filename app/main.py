from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    from app import conf
    return {"message": conf.test}

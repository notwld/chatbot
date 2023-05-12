# fast api boiler plate

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from predict import get_response
import uvicorn

app = FastAPI()

# middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])

# routes


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/predict")
async def predict(query: str):
    return get_response(query)

if __name__ == "__main__":
    uvicorn.run(app)

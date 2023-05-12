# fast api boiler plate

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from predict import get_response
import uvicorn
from typing import Any,Dict

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
def root():
    return {"message": "Hello World"}


@app.post("/predict")
def predict(query: Dict[Any, Any]):
    print(query)
    return {
        "response":get_response(str(query['query'])),
    }

if __name__ == "__main__":
    uvicorn.run(app)

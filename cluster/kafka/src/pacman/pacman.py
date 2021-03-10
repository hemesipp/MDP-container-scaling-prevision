from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

class User(BaseModel):
    first_name: str
    last_name: str = None
    age: int


app = FastAPI()

@app.post("/user/", response_model=User)
async def create_user(user: User):
    return user

@app.get("/")
def root():
    a = "a"
    b = "b" + a
    return {"hello world": b}


"""
def main(nb_container_asked, nb_container):
    while True:
        while nb_container_asked<=nb_container:
            "send end message"
            nb_container-=1
        while nb_container_asked>=:
            "create new pod"
            nb_container+=1
        if nb_container_asked==nb_container:
            "send packet"
            app.run(host='0.0.0.0')
"""

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)

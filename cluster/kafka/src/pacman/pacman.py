from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import time


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
main est appelée à chaque nouvelle requete reçu

waiting_list: liste de new_consumer en attente
nb_container_asked: valeur rendue par l'algo de prédiction
nb_container: nombre de pods actifs
"""


"""
def main(nb_container_asked, nb_container, waiting_list):
    while True:
        while nb_container_asked<=nb_container:
            remove_new_consumer(waiting_list[0])
            nb_container-=1
        while nb_container_asked>=nb_container:
            add_new_consumer(nb_container_asked)
            nb_container+=1
        if nb_container_asked==nb_container:
            "send packet"
"""

if __name__ == "__main__":
    uvicorn.run("pacman:app", host="0.0.0.0", port=80)
    """
    nb_container = 0
    While True:
        #How to wait a request and add to waiting_list?
        nb_container_asked = algo(param1, param2, nb_container)         
        main(nb_container_asked, nb_container, waiting_list)
    """


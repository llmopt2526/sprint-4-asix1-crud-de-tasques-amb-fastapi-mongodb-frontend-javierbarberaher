from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ConfigDict, BaseModel, Field
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from bson import ObjectId
from pymongo import MongoClient
from typing import Optional, List

app = FastAPI(title="Gestor de Pel·lícules")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

MONGODB_URL = "mongodb+srv://javierbarbera_db_user:p@peliscluster.ugu6qw7.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGODB_URL)
db = client.cinema_db
movie_collection = db.get_collection("movies")
user_collection = db.get_collection("users")

PyObjectId = Annotated[str, BeforeValidator(str)]

class UserModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    username: str = Field(...)
    email: str = Field(...)
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

class MovieModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    titol: str = Field(...)
    descripcio: str = Field(...)
    estat: str = Field(...)
    puntuacio: int = Field(...)
    genere: str = Field(...)
    usuari: str = Field(...)
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)


@app.get("/users", response_model=List[UserModel], tags=["Users"])
def list_users():
    return list(user_collection.find().limit(1000))

@app.post("/users", response_model=UserModel, tags=["Users"])
def create_user(user: UserModel = Body(...)):
    new_user = user_collection.insert_one(user.model_dump(by_alias=True, exclude={"id"}))
    return user_collection.find_one({"_id": new_user.inserted_id})

@app.delete("/users/{id}", tags=["Users"])
def delete_user(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID no vàlid")
    delete_result = user_collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail="Usuari no trobat")


@app.get("/movies", response_model=List[MovieModel], tags=["Movies"])
def list_movies():
    return list(movie_collection.find().limit(1000))

@app.post("/movies", response_model=MovieModel, tags=["Movies"])
def create_movie(movie: MovieModel = Body(...)):
    user_exists = user_collection.find_one({"username": movie.usuari})
    if not user_exists:
        raise HTTPException(status_code=400, detail="L'usuari ha d'existir")
    new_movie = movie_collection.insert_one(movie.model_dump(by_alias=True, exclude={"id"}))
    return movie_collection.find_one({"_id": new_movie.inserted_id})

@app.patch("/movies/{id}/toggle-status", tags=["Movies"])
def toggle_movie_status(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID no vàlid")
    movie = movie_collection.find_one({"_id": ObjectId(id)})
    if not movie:
        raise HTTPException(status_code=404, detail="Peli no trobada")
    
    nou_estat = "vista" if movie["estat"] == "pendent de veure" else "pendent de veure"
    movie_collection.update_one({"_id": ObjectId(id)}, {"$set": {"estat": nou_estat}})
    return {"message": "Estat canviat", "nou_estat": nou_estat}

@app.delete("/movies/{id}", tags=["Movies"])
def delete_movie(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID no vàlid")
    delete_result = movie_collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail="No trobada")
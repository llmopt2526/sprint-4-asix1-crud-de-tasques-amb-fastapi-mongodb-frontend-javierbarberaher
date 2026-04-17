from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ConfigDict, BaseModel, Field
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from bson import ObjectId
from pymongo import MongoClient
from typing import Optional, List

# ------------------------------------------------------------------------ #
#                         Inicialització de l'aplicació                    #
# ------------------------------------------------------------------------ #
# Creació de la instància FastAPI
app = FastAPI(title="Gestor de Pel·lícules")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------------------ #
#                   Configuració de la connexió amb MongoDB                #
# ------------------------------------------------------------------------ #
# Aquesta es la URL de conexió amb mongo
MONGODB_URL = "mongodb+srv://javierbarbera_db_user:p@peliscluster.ugu6qw7.mongodb.net/?retryWrites=true&w=majority"
# Creem el client de MongoDB utilitzant la URL de connexió
client = MongoClient(MONGODB_URL)
db = client.cinema_db
movie_collection = db.get_collection("movies")
user_collection = db.get_collection("users")

# Els documents de MongoDB tenen `_id` de tipus ObjectId.
# Aquí definim PyObjectId com un string serialitzable per JSON, que serà utilitzat als models Pydantic.
PyObjectId = Annotated[str, BeforeValidator(str)]

# ------------------------------------------------------------------------ #
#                            Definició dels models                         #
# ------------------------------------------------------------------------ #
class UserModel(BaseModel):
    # Clau primaria del Usuari
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    # La resta de camps de l'usuari, son obligatoris
    username: str = Field(...)
    email: str = Field(...)
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

class MovieModel(BaseModel):
    # Clau primaria de les pelicules
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    # La resta de camps de les pelicules, son obligatoris
    titol: str = Field(...)
    descripcio: str = Field(...)
    estat: str = Field(...)
    puntuacio: int = Field(...)
    genere: str = Field(...)
    usuari: str = Field(...)
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

# ------------------------------------------------------------------------ #
#                             Endpints d'usuaris                           #
# ------------------------------------------------------------------------ #
# Endpoint per a GET, llista limitada a 1000 entrades.
@app.get("/users", response_model=List[UserModel], tags=["Users"])
def list_users():
    return list(user_collection.find().limit(1000))
# Endpoint per a POST.
@app.post("/users", response_model=UserModel, tags=["Users"])
def create_user(user: UserModel = Body(...)):
    new_user = user_collection.insert_one(user.model_dump(by_alias=True, exclude={"id"}))
    return user_collection.find_one({"_id": new_user.inserted_id})
# Endpoint per a DELETE, amb missatges d'error
@app.delete("/users/{id}", tags=["Users"])
def delete_user(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID no vàlid")
    delete_result = user_collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail="Usuari no trobat")

# ------------------------------------------------------------------------ #
#                          Endpints de pel·licules                         #
# ------------------------------------------------------------------------ #
# Endpoint per a GET de Pel·lícules, llista limitada a 1000 entrades.
@app.get("/movies", response_model=List[MovieModel], tags=["Movies"])
def list_movies():
    return list(movie_collection.find().limit(1000))
# Endpoint per a POST.
@app.post("/movies", response_model=MovieModel, tags=["Movies"])
def create_movie(movie: MovieModel = Body(...)):
    user_exists = user_collection.find_one({"username": movie.usuari})
    if not user_exists:
        raise HTTPException(status_code=400, detail="L'usuari ha d'existir")
    new_movie = movie_collection.insert_one(movie.model_dump(by_alias=True, exclude={"id"}))
    return movie_collection.find_one({"_id": new_movie.inserted_id})
# Endpoint per a PATCH, que cambia els estats de les pel·lícules. 
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
# Endpoint per a DELETE, amb missatges d'error.
@app.delete("/movies/{id}", tags=["Movies"])
def delete_movie(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID no vàlid")
    delete_result = movie_collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail="No trobada")

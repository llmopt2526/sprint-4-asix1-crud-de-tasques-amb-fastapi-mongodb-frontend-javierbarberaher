from fastapi import FastAPI, Body, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ConfigDict, BaseModel, Field
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from bson import ObjectId
import motor.motor_asyncio
from typing import Optional, List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

MONGODB_URL = "mongodb+srv://javierbarbera_db_user:p@peliscluster.ugu6qw7.mongodb.net/"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
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
    estat: str = Field(..., pattern="^(pendent de veure|vista)$")
    puntuacio: int = Field(..., ge=1, le=5)
    genere: str = Field(...)
    usuari: str = Field(...)
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)


@app.get("/users", response_model=List[UserModel], tags=["Users"])
async def list_users():
    return await user_collection.find().to_list(1000)

@app.post("/users", response_model=UserModel, tags=["Users"])
async def create_user(user: UserModel = Body(...)):
    new_user = await user_collection.insert_one(user.model_dump(by_alias=True, exclude={"id"}))
    return await user_collection.find_one({"_id": new_user.inserted_id})

@app.delete("/users/{id}", tags=["Users"])
async def delete_user(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=400, 
            detail="L'ID d'usuari no té un format vàlid de MongoDB (han de ser 24 caràcters)"
        )
    delete_result = await user_collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        # Retornem un missatge confirmant l'eliminació
        return {"message": f"Usuari amb ID {id} eliminat correctament"}
    raise HTTPException(
        status_code=404, 
        detail="No s'ha trobat cap usuari amb aquest ID"
    )


@app.get("/movies", response_model=List[MovieModel], tags=["Movies"])
async def list_movies():
    return await movie_collection.find().to_list(1000)

@app.post("/movies", response_model=MovieModel, tags=["Movies"])
async def create_movie(movie: MovieModel = Body(...)):
    # Comprovem si l'usuari existeix abans de deixar-li penjar la peli
    user_exists = await user_collection.find_one({"username": movie.usuari})
    if not user_exists:
        raise HTTPException(status_code=400, detail="L'usuari ha d'estar registrat a la base de dades")
    
    new_movie = await movie_collection.insert_one(movie.model_dump(by_alias=True, exclude={"id"}))
    return await movie_collection.find_one({"_id": new_movie.inserted_id})

@app.delete("/movies/{id}", tags=["Movies"])
async def delete_movie(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="El formato del ID no es válido")
    delete_result = await movie_collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return {"message": "Pel·lícula eliminada correctament"}
    raise HTTPException(status_code=404, detail="No se ha encontrado la película con ese ID")
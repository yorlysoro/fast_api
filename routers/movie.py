# -*- coding: utf-8 -*-

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
from fastapi import APIRouter
from fastapi import Depends, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService

movie_router = APIRouter()


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=15)
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(le=2022)
    rating: float = Field(default=10, ge=1, le=10)
    category: str = Field(default="Categoria", min_length=5, max_length=15)

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Mi pelicula",
                "overview": "Descripcion de la pelicula",
                "year": 2022,
                "rating": 8.5,
                "category": "Accion"
            }
        }


@movie_router.get('/movies',
                  tags=['movies'],
                  response_model=List[Movie],
                  status_code=200,
                  dependencies=[Depends(JWTBearer())]
                  )
def get_movies() -> JSONResponse:
    db = Session()
    result = MovieService(db).get_movies()
    db.close()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@movie_router.get('/movies/{id}',
                  tags=['movies'],
                  response_model=Movie,
                  status_code=200
                  )
def get_movie(id: int = Path(ge=1, le=2000)) -> JSONResponse:
    db = Session()
    result = MovieService(db).get_movie(id)
    db.close()
    if not result:
        return JSONResponse(status_code=404, content={'message': "Pelicula no encontrada"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@movie_router.get('/movies/',
                  tags=['movies'],
                  response_model=List[Movie]
                  )
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> JSONResponse:
    db = Session()
    result = MovieService(db).get_movie_by_category(category)
    if not result:
        return JSONResponse(status_code=404, content={'message': "Pelicula no encontrada"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@movie_router.post('/movies',
                   tags=['movies'],
                   response_model=dict,
                   status_code=201
                   )
def create_movie(
        id: int,
        movie: Movie
) -> JSONResponse:
    db = Session()
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    db.close()
    return JSONResponse(status_code=201, content={"message": "La pelicula ha sido creada con exito"})


@movie_router.put('/movies/{id}',
                  tags=['movies'],
                  response_model=dict,
                  status_code=200
                  )
def update_movie(
        id: int,
        movie: Movie
) -> JSONResponse:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={"message": "No encontrado!!"})
    result.title = movie.title
    result.overview = movie.overview
    result.year = movie.year
    result.rating = movie.rating
    result.category = movie.category
    db.commit()
    db.close()
    return JSONResponse(status_code=200, content={"message": "Se ha modificado"})


@movie_router.delete('/movies/{id}',
            tags=['movies'],
            response_model=dict,
            status_code=200
            )
def delete_movie(id: int) -> JSONResponse:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={"message": "No encontrado!!"})
    db.delete(result)
    db.commit()
    db.close()
    return JSONResponse(status_code=200, content={"message": "Se ha eliminado correctamente"})

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

from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List

from starlette.responses import JSONResponse

app = FastAPI()
app.title = "Aplicacion con FastAPI"
app.version = "0.0.1"


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


movies = [
    {
        "id": 1,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        "year": "2009",
        "rating": 7.8,
        "category": "Acción"
    },
    {
        "id": 2,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        "year": "2009",
        "rating": 7.8,
        "category": "Acción"
    }
]


@app.get('/', tags=["home"])
def message():
    return HTMLResponse('<h1>Hello World!</h1>')


@app.get('/movies', tags=['movies'], response_model=List[Movie])
def get_movies() -> JSONResponse:
    return JSONResponse(content=Movie)


@app.get('/movies/{id}', tags=['movies'], response_model=Movie)
def get_movie(id: int = Path(ge=1, le=2000)) -> JSONResponse:
    for item in movies:
        if item["id"] == id:
            return JSONResponse(content=item)
    return JSONResponse(content=[])


@app.get('/movies/', tags=['movies'], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15),
                           year: int = Query(min_value=2010, max_value=2020)) -> JSONResponse:
    data = [item for item in movies if item['category'] == category or item['year'] == str(year)]
    return JSONResponse(content=data)


@app.post('/movies', tags=['movies'], response_model=dict)
def create_movie(
        id: int,
        movie: Movie
) -> JSONResponse:
    movies.append(movie)
    return JSONResponse(content={"message": "La pelicula ha sido creada con exito"})


@app.put('/movies/{id}', tags=['movies'], response_model=dict)
def update_movie(
        id: int,
        movie: Movie
) -> JSONResponse:
    for i, item in enumerate(movies):
        if item["id"] == id:
            item["title"] = movie.title
            item["overview"] = movie.overview
            item["year"] = movie.year
            item["rating"] = movie.rating
            item["category"] = movie.category
            return JSONResponse(content={"message": "Se ha modificado la pelicula correctamente"})


@app.delete('/movies/{id}', tags=['movies'], response_model=dict)
def delete_movie(id: int) -> JSONResponse:
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return JSONResponse(content={"message": "La pelicula ha sido eliminada"})

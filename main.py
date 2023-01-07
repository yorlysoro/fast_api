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

from fastapi import FastAPI
from fastapi.responses import  HTMLResponse

app = FastAPI()
app.title = "Aplicacion con FastAPI"
app.version = "0.0.1" 


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


@app.get('/movies', tags=['movies'])
def get_movies():
	return movies
	
@app.get('/movies/{id}', tags=['movies'])
def get_movie(id: int):
	for item in movies:
		if item["id"] == id:
			return item
	return []

@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str, year: int):
	movie = [item for item in movies if item['category'] == category or item['year'] == str(year)]
	return movie

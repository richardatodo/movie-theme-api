from typing import Optional
from fastapi import FastAPI, HTTPException, Query
import json


app = FastAPI()

# Read data.json at startup
try:
    with open("movies.json", "r") as f:
        movies = json.load(f)
except FileNotFoundError:
    movies = []
    print("data.json file not found!")
except json.JSONDecodeError:
    movies = []
    print("Error decoding JSON data.")

# Home
@app.get("/")
def read_root():
    return {"Welcome to the Movie Theme Song Finder API!"}

# Get all movies
@app.get("/api/movies")
async def get_all():
    return{"movies": movies}

# Get movie by id
@app.get("/api/movies/id/{id}")
async def get_by_id(id: int):
    movie = [m for m in movies if m["id"] == id]
    if not movie:
        raise HTTPException(
            status_code=404, 
            detail=f"This movie currently not available. Please check again later"
        )
    return{"movies": movie}

# Search Movies by Title or Genre or Artist or Song Title
@app.get("/api/movies/search")
async def search(
    title: Optional[str] = Query(None, description="Search by movie title"),
    genre: Optional[str] = Query(None, description="Search by movie genre"),
    artist: Optional[str] = Query(None, description="Search by artist of the theme song"),
    theme_song_title: Optional[str] = Query(None, description="Search by theme song title")
):
    # Filter movies based on provided parameters
    filtered_movies = [
        movie for movie in movies
        if (
            (title and title.lower() in movie["title"].lower()) or 
            (genre and genre.lower() in movie["genre"].lower()) or
            (artist and movie["theme_song"] and artist.lower() in movie["theme_song"]["artist"].lower()) or
            (theme_song_title and movie["theme_song"] and theme_song_title.lower() in movie["theme_song"]["title"].lower())
        )
    ]
    if not filtered_movies:
        raise HTTPException(
            status_code=404,
            detail="No movie matched your criteria"
        )
    return{"result": filtered_movies}

# Get movies by year   
@app.get("/api/movies/year/{year}")
async def get_by_year(year: int):
    moviesYear = [m for m in movies if m["year"] == year]
    if not moviesYear:
        raise HTTPException(
            status_code=404, 
            detail=f"We don't have any {year} movie currently. Please check again later"
        )
    return{"movies": moviesYear}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
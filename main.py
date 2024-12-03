from typing import Optional
from fastapi import FastAPI, HTTPException, Query
import json
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key not found in .env file.")
OpenAI.api_key = OPENAI_API_KEY

app = FastAPI()

client = OpenAI()

# Read data.json at startup
try:
    with open("movies.json", "r") as f:
        movies = json.load(f)
except FileNotFoundError:
    movies = []
    print("movies.json file not found!")
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

# Get movie summary
def generate_movie_summary(title: str, year: int, genre: str) -> str:
    """
    Generated Movie Summary from OpenAI API
    """
    prompt = (
        f"Write a concise and engaging summary for a movie titled '{title}' "
        f"released in {year}. The genre of the movie is {genre}. "
        f"Focus on the plot and main themes without revealing spoilers."
    )

    try:
        response = client.chat.completions.create(
            model= "gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert movie reviewer."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choice[0].message
    except Exception as e:
        return f"Error generating summary: {str(e)}"

@app.get("/api/movies/summary/{id}")
async def get_movie_summary(id: int):
    """AI Generated Movie Summary by ID"""
    movie = next((m for m in movies if m["id"] == id), None)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie Not Found")
    
    summary = generate_movie_summary(movie["title"], movie["year"], movie["genre"])
    return {
        "id": movie["id"],
        "title": movie["title"],
        "summary": summary
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
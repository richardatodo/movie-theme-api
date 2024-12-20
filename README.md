# Movie Theme Song Finder API

A **FastAPI-based API** to search for movies by title, genre, artist, or theme song title. This API also integrates with **OpenAI** to generate AI-powered movie summaries, making it a versatile tool for developers working on movie-related applications.

---

## Features

- Search movies by:
  - Title
  - Genre
  - Theme song artist
  - Theme song title
- Supports flexible, case-insensitive searches.
- AI-Generated Movie Summaries.

---

## Getting Started

### Prerequisites

- Python 3.9 or later
- FastAPI and Uvicorn installed (`pip install -r requirements.txt`)

---

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/richardatodo/movie-theme-api.git
   cd movie-theme-api

2. Install dependencies:
   ```bash
   pip install -r requirements.txt

3. Run the API:
   ```bash
   python.main.py

4. Open your browser and navigate to:
   * Interactive API Docs: http://127.0.0.1:8000/docs
   * ReDoc Documentation: http://127.0.0.1:8000/redoc

### API Endpoints
#### Home
* GET /
  * Description: Welcome message.

#### Get All Movies
* `GET /api/movies`
  * Description: Returns all available movies.

#### Get Movie by ID
* `GET /api/movies/id/{id}`
  * Description: Fetch a movie by its ID.
  * Parameters:
    * `id` (int): Movie ID.

#### Search Movies
* `GET /api/movies/search`
   * Description: Search for movies using various criteria.
   * Query Parameters:
     * `title` (str, optional): Search by movie title.
     * `genre` (str, optional): Search by movie genre.
     * `artist` (str, optional): Search by theme song artist.
     * `theme_song_title` (str, optional): Search by theme song title.

#### Get Movies by Year
* `GET /api/movies/year/{year}`
   * Description: Get movies released in a specific year.
   * Parameters:
     * `year` (int): Release year.

#### AI-Generated Movie Summary
* `GET /api/movies/summary/{id}`
   * Generate a concise, engaging summary for a specific movie.
   * Parameters:
     * `Id`(int): Movie ID.
   * Requires:
     * A valid OpenAI API Key.

### Contributing
If you find any issues or have suggestions, feel free to open an issue or submit a pull request or reach out to me.
* **Ameh Richard Atodo** [@RichardAtodo](https://x.com/RichardAtodo)
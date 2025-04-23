import requests
import json
import os
import sys
import time
from typing import List, Dict, Any, Optional

# TMDB API - Free with registration at https://www.themoviedb.org/
TMDB_API_KEY = "23cc57835e00ff5675bf698ea2c75afc"  # Already configured API key

# Ollama API endpoint (default for local installation)
OLLAMA_API_URL = "http://localhost:11434/api/generate"

# Genre ID to name mapping for TMDB
GENRE_MAP = {
    28: "Action",
    12: "Adventure",
    16: "Animation",
    35: "Comedy",
    80: "Crime",
    99: "Documentary",
    18: "Drama",
    10751: "Family",
    14: "Fantasy",
    36: "History",
    27: "Horror",
    10402: "Music",
    9648: "Mystery",
    10749: "Romance",
    878: "Science Fiction",
    10770: "TV Movie",
    53: "Thriller",
    10752: "War",
    37: "Western"
}

def check_ollama_running() -> bool:
    """Check if Ollama is running locally."""
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            models = response.json().get("models", [])
            if models:
                print(f"Ollama is running with available models: {', '.join([m['name'] for m in models])}")
                return True
            else:
                print("Ollama is running but no models are available.")
                print("Run 'ollama pull mistral' to download a model.")
                return False
        else:
            print("Ollama API returned an error.")
            return False
    except requests.exceptions.ConnectionError:
        print("Ollama is not running. Please install and start Ollama:")
        print("1. Download from https://ollama.com/")
        print("2. Start Ollama")
        print("3. Run 'ollama pull mistral' to download a model")
        return False

def get_genre_id(genre_name: str) -> Optional[int]:
    """Convert genre name to genre ID."""
    genre_name_lower = genre_name.lower()
    for genre_id, name in GENRE_MAP.items():
        if name.lower() == genre_name_lower:
            return genre_id
    return None

def get_all_genres() -> List[Dict[str, Any]]:
    """Get all available genres from TMDB."""
    url = "https://api.themoviedb.org/3/genre/movie/list"
    params = {
        "api_key": TMDB_API_KEY,
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("genres", [])
    else:
        print(f"Error: {response.status_code}")
        return []

def discover_movies_by_genre(genre_id: int, page: int = 1, year: Optional[int] = None) -> List[Dict[str, Any]]:
    """Discover movies based on genre."""
    url = "https://api.themoviedb.org/3/discover/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "with_genres": genre_id,
        "sort_by": "popularity.desc",
        "include_adult": "false",
        "page": page
    }
    
    if year:
        params["primary_release_year"] = year
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        print(f"Error: {response.status_code}")
        return []

def get_movie_details(movie_id: int) -> Optional[Dict[str, Any]]:
    """Get detailed information about a movie."""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {
        "api_key": TMDB_API_KEY,
        "append_to_response": "credits,keywords"
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

def get_llm_recommendation(model: str, movies: List[Dict[str, Any]], user_preferences: str) -> str:
    """Get movie recommendations from local LLM using Ollama."""
    # Prepare movie data for the LLM
    movie_data = []
    for movie in movies[:10]:  # Limit to 10 movies to avoid overwhelming the LLM
        movie_data.append({
            "id": movie["id"],
            "title": movie["title"],
            "overview": movie["overview"],
            "popularity": movie["popularity"],
            "vote_average": movie["vote_average"],
            "release_date": movie.get("release_date", "Unknown")
        })
    
    # Create prompt for the LLM
    prompt = f"""You are a movie recommendation expert. Based on the user's preferences and the following movies, recommend the top 3 movies that best match their preferences.
    
User preferences: {user_preferences}

Available movies:
{json.dumps(movie_data, indent=2)}

For each recommended movie, explain why you think it's a good match for the user's preferences. Format your response as:

1. [Movie Title] - [Release Year]
   Rating: [Rating]/10
   Why it's a good match: [Your explanation]

2. [Movie Title] - [Release Year]
   Rating: [Rating]/10
   Why it's a good match: [Your explanation]

3. [Movie Title] - [Release Year]
   Rating: [Rating]/10
   Why it's a good match: [Your explanation]
"""

    # Call Ollama API
    try:
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }
        response = requests.post(OLLAMA_API_URL, json=payload)
        
        if response.status_code == 200:
            return response.json().get("response", "No recommendations available.")
        else:
            return f"Error: Failed to get recommendations. Status code: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

def print_movie_info(movie: Dict[str, Any]) -> None:
    """Print formatted movie information."""
    title = movie.get("title", "Unknown Title")
    release_date = movie.get("release_date", "Unknown")
    release_year = release_date[:4] if release_date and len(release_date) >= 4 else "Unknown"
    vote_average = movie.get("vote_average", 0)
    overview = movie.get("overview", "No overview available")
    
    print(f"Title: {title} ({release_year})")
    print(f"Rating: {vote_average}/10")
    print(f"Overview: {overview[:200]}..." if len(overview) > 200 else f"Overview: {overview}")
    print()

def main():
    """Main function to run the genre-based movie recommender."""
    print("\n=== Genre-Based Movie Recommender (with Free LLM) ===")
    
    # Check if Ollama is running
    if not check_ollama_running():
        print("Please start Ollama and try again.")
        return
    
    # Get available LLM models
    try:
        response = requests.get("http://localhost:11434/api/tags")
        models = [m["name"] for m in response.json().get("models", [])]
        
        if not models:
            print("No LLM models found. Please run 'ollama pull mistral' to download a model.")
            return
        
        # Select model (prefer mistral if available, otherwise use the first available model)
        model = "mistral" if "mistral" in models else models[0]
        print(f"Using LLM model: {model}")
    except Exception as e:
        print(f"Error checking LLM models: {str(e)}")
        return
    
    # Get all available genres
    genres = get_all_genres()
    if not genres:
        print("Failed to retrieve genres. Please check your internet connection.")
        return
    
    # Print available genres
    print("\nAvailable movie genres:")
    for i, genre in enumerate(genres, 1):
        print(f"{i}. {genre['name']}")
    
    # Main interaction loop
    while True:
        print("\nCommands:")
        print("  recommend <genre> - Get personalized recommendations for a specific genre")
        print("  list - List all available genres")
        print("  exit - Quit the program")
        
        command = input("\nEnter command: ").strip()
        
        if command.lower() in ["exit", "quit", "q"]:
            break
        
        parts = command.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        
        if cmd == "list":
            print("\nAvailable movie genres:")
            for i, genre in enumerate(genres, 1):
                print(f"{i}. {genre['name']}")
        
        elif cmd == "recommend" and args:
            # Get genre ID
            genre_id = None
            
            # Check if input is a number (index in the list)
            if args.isdigit() and 1 <= int(args) <= len(genres):
                genre_id = genres[int(args) - 1]["id"]
                genre_name = genres[int(args) - 1]["name"]
            else:
                # Try to match by name
                for genre in genres:
                    if genre["name"].lower() == args.lower():
                        genre_id = genre["id"]
                        genre_name = genre["name"]
                        break
            
            if genre_id is None:
                print(f"Genre '{args}' not found. Use 'list' to see available genres.")
                continue
            
            print(f"\nFetching movies for genre: {genre_name}")
            
            # Get user preferences for this genre
            preferences = input(f"Tell me more about what you like in {genre_name} movies (e.g., themes, actors, style): ")
            
            # Get movies for this genre
            movies = discover_movies_by_genre(genre_id)
            if not movies:
                print(f"No movies found for genre: {genre_name}")
                continue
            
            print(f"\nFound {len(movies)} {genre_name} movies. Generating personalized recommendations...")
            
            # Get LLM recommendations
            recommendations = get_llm_recommendation(model, movies, f"Genre: {genre_name}, Preferences: {preferences}")
            
            print("\n=== Personalized Recommendations ===\n")
            print(recommendations)
            print("\n" + "=" * 50 + "\n")
        
        else:
            print("Unknown command or missing arguments. Try 'recommend <genre>' or 'list'.")
    
    print("\nThank you for using the Genre-Based Movie Recommender!")

if __name__ == "__main__":
    main()

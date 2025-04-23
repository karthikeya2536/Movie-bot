import requests
import pandas as pd
import os
from pathlib import Path

# TMDB API - Free with registration at https://www.themoviedb.org/
# You'll need to sign up and get an API key, but it's free
TMDB_API_KEY = "23cc57835e00ff5675bf698ea2c75afc"  # Replace with your TMDB API key after registering

def search_movies(query, page=1):
    """Search for movies using TMDB API"""
    url = f"https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "query": query,
        "page": page,
        "include_adult": "false"
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

def get_movie_details(movie_id):
    """Get detailed information about a movie"""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {
        "api_key": TMDB_API_KEY,
        "append_to_response": "credits,recommendations"
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

def get_movie_recommendations(movie_id):
    """Get movie recommendations based on a movie ID"""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations"
    params = {
        "api_key": TMDB_API_KEY,
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

def discover_movies(genre=None, year=None, sort_by="popularity.desc"):
    """Discover movies based on criteria"""
    url = "https://api.themoviedb.org/3/discover/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "sort_by": sort_by,
        "include_adult": "false",
        "include_video": "false",
        "page": 1
    }

    if genre:
        params["with_genres"] = genre
    if year:
        params["primary_release_year"] = year

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

def format_movie_info(movie):
    """Format movie information for display"""
    title = movie.get("title", "Unknown Title")
    release_date = movie.get("release_date", "Unknown")
    vote_average = movie.get("vote_average", 0)
    overview = movie.get("overview", "No overview available")

    return f"Title: {title}\nRelease Date: {release_date}\nRating: {vote_average}/10\nOverview: {overview}\n"

def main():
    print("\n=== Movie Recommendation Bot (TMDB API) ===")
    print("Search for movies, get recommendations, or discover new films.")
    print("Commands:")
    print("  search <query> - Search for movies")
    print("  details <movie_id> - Get details about a specific movie")
    print("  recommend <movie_id> - Get recommendations based on a movie")
    print("  discover [genre_id] [year] - Discover popular movies, optionally by genre and year")
    print("  exit - Quit the program")
    print("\nAPI key is already configured and ready to use!\n")

    # Skip the warning since we already have an API key
    if False:
        print("WARNING: You need to replace 'YOUR_TMDB_API_KEY' with your actual TMDB API key.")
        print("Register for free at https://www.themoviedb.org/ and update the script.\n")

    while True:
        command = input("> ").strip()

        if command.lower() in ['exit', 'quit', 'q']:
            break

        parts = command.split(maxsplit=1)
        if len(parts) == 0:
            continue

        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        if cmd == "search" and args:
            results = search_movies(args)
            if results and "results" in results:
                print(f"\nFound {len(results['results'])} movies:")
                for movie in results["results"][:10]:  # Show top 10 results
                    print(f"ID: {movie['id']} - {movie['title']} ({movie.get('release_date', 'N/A')[:4]})")
                    print(f"  Rating: {movie.get('vote_average', 'N/A')}/10")
                    print(f"  Overview: {movie.get('overview', 'No overview')[:100]}...")
                    print()
            else:
                print("No results found or API error.")

        elif cmd == "details" and args:
            try:
                movie_id = int(args)
                movie = get_movie_details(movie_id)
                if movie:
                    print("\nMovie Details:")
                    print(f"Title: {movie['title']} ({movie.get('release_date', 'N/A')[:4]})")
                    print(f"Genres: {', '.join([g['name'] for g in movie.get('genres', [])])}")
                    print(f"Rating: {movie.get('vote_average', 'N/A')}/10 ({movie.get('vote_count', 0)} votes)")
                    print(f"Runtime: {movie.get('runtime', 'N/A')} minutes")
                    print(f"Budget: ${movie.get('budget', 0):,}")
                    print(f"Revenue: ${movie.get('revenue', 0):,}")
                    print(f"Overview: {movie.get('overview', 'No overview')}")

                    # Show top cast
                    if "credits" in movie and "cast" in movie["credits"]:
                        cast = movie["credits"]["cast"][:5]  # Top 5 cast members
                        if cast:
                            print("\nTop Cast:")
                            for actor in cast:
                                print(f"  {actor['name']} as {actor.get('character', 'Unknown')}")
                else:
                    print("Movie not found or API error.")
            except ValueError:
                print("Invalid movie ID. Please provide a numeric ID.")

        elif cmd == "recommend" and args:
            try:
                movie_id = int(args)
                recommendations = get_movie_recommendations(movie_id)
                if recommendations and "results" in recommendations:
                    print(f"\nRecommendations based on movie ID {movie_id}:")
                    for movie in recommendations["results"][:8]:  # Show top 8 recommendations
                        print(f"ID: {movie['id']} - {movie['title']} ({movie.get('release_date', 'N/A')[:4]})")
                        print(f"  Rating: {movie.get('vote_average', 'N/A')}/10")
                        print(f"  Overview: {movie.get('overview', 'No overview')[:100]}...")
                        print()
                else:
                    print("No recommendations found or API error.")
            except ValueError:
                print("Invalid movie ID. Please provide a numeric ID.")

        elif cmd == "discover":
            genre_id = None
            year = None

            # Parse arguments if provided
            args_parts = args.split()
            if len(args_parts) >= 1 and args_parts[0].isdigit():
                genre_id = args_parts[0]
            if len(args_parts) >= 2 and args_parts[1].isdigit() and len(args_parts[1]) == 4:
                year = args_parts[1]

            results = discover_movies(genre_id, year)
            if results and "results" in results:
                print(f"\nDiscovered movies:")
                for movie in results["results"][:10]:  # Show top 10 results
                    print(f"ID: {movie['id']} - {movie['title']} ({movie.get('release_date', 'N/A')[:4]})")
                    print(f"  Rating: {movie.get('vote_average', 'N/A')}/10")
                    print(f"  Overview: {movie.get('overview', 'No overview')[:100]}...")
                    print()
            else:
                print("No results found or API error.")

        else:
            print("Unknown command or missing arguments. Type 'exit' to quit.")

        print("\n" + "-"*50 + "\n")

if __name__ == "__main__":
    main()

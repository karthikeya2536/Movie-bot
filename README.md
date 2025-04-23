# TMDB Movie Recommendation Bot

A command-line application that provides movie recommendations, search functionality, and detailed movie information using The Movie Database (TMDB) API.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Information](#api-information)
- [Common Genre IDs](#common-genre-ids)
- [License](#license)

## Overview

This Movie Recommendation Bot leverages the free TMDB API to help you discover movies, get detailed information about specific films, and find recommendations based on movies you already enjoy. The application runs in the command line and provides an interactive interface for exploring the vast TMDB database.

## Features

- **Search for Movies**: Find movies by title, keywords, or phrases
- **Get Movie Details**: View comprehensive information about a movie including cast, budget, revenue, and more
- **Movie Recommendations**: Get personalized movie recommendations based on a movie you like
- **Discover Movies**: Browse popular movies, optionally filtered by genre and year
- **Interactive Interface**: Simple command-line interface for easy navigation

## Installation

1. Ensure you have Python 3.6+ installed
2. Clone this repository or download the files
3. Install the required dependencies:

```bash
pip install requests pandas
```

## Usage

Run the application with:

```bash
python tmdb_movie_bot.py
```

Once running, you can use the following commands:

- `search <query>` - Search for movies by title or keywords
- `details <movie_id>` - Get detailed information about a specific movie
- `recommend <movie_id>` - Get movie recommendations based on a specific movie
- `discover [genre_id] [year]` - Discover popular movies, optionally filtered by genre and year
- `exit` - Quit the program

### Example Usage:

```
> search Inception
> details 27205
> recommend 27205
> discover 28 2023
> exit
```

## API Information

This application uses the free TMDB API. The API key is already included in the script, but if you want to use your own:

1. Register for a free account at [The Movie Database](https://www.themoviedb.org/)
2. Request an API key from your account settings
3. Replace the `TMDB_API_KEY` value in the script with your own key

## Common Genre IDs

Use these genre IDs with the `discover` command:

- 28: Action
- 12: Adventure
- 16: Animation
- 35: Comedy
- 80: Crime
- 99: Documentary
- 18: Drama
- 10751: Family
- 14: Fantasy
- 36: History
- 27: Horror
- 10402: Music
- 9648: Mystery
- 10749: Romance
- 878: Science Fiction
- 53: Thriller
- 10752: War
- 37: Western

## License

This project is licensed under the MIT License - see the LICENSE file for details.

The movie data is provided by [The Movie Database (TMDB)](https://www.themoviedb.org/), but this project is not endorsed or certified by TMDB.

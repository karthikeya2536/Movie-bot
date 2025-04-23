# Genre-Based Movie Recommendation System

A command-line application that provides personalized movie recommendations based on genres using The Movie Database (TMDB) API and a free local LLM (Ollama).

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Information](#api-information)
- [Common Genre IDs](#common-genre-ids)
- [License](#license)

## Overview

This Genre-Based Movie Recommendation System combines the free TMDB API with a locally-running LLM (via Ollama) to provide highly personalized movie recommendations based on your genre preferences. The system uses the TMDB API to fetch movie data and the LLM to analyze your preferences and suggest the most suitable movies within your chosen genre.

## Features

- **Genre-Based Recommendations**: Get personalized movie recommendations for specific genres
- **AI-Powered Analysis**: Uses a free, locally-running LLM to analyze your preferences
- **Personalization**: Tell the system what aspects of a genre you enjoy for better recommendations
- **No API Keys Required**: Pre-configured with TMDB API key
- **Privacy-Focused**: All processing happens locally on your machine
- **Interactive Interface**: Simple command-line interface for easy navigation

## Installation

1. Ensure you have Python 3.6+ installed
2. Clone this repository or download the files
3. Install Ollama from [ollama.com](https://ollama.com/)
4. After installing Ollama, download the Mistral model:
   ```bash
   ollama pull mistral
   ```
5. Install the required Python dependencies:
   ```bash
   pip install requests
   ```

## Usage

Run the application with:

```bash
python genre_movie_recommender.py
```

Make sure Ollama is running in the background before starting the application.

Once running, you can use the following commands:

- `list` - List all available movie genres
- `recommend <genre>` - Get personalized recommendations for a specific genre
- `exit` - Quit the program

### Example Usage:

```
> list
> recommend Action
> recommend Comedy
> exit
```

When you use the `recommend` command, you'll be prompted to provide more details about what you like in that genre. For example:

```
> recommend Action
Tell me more about what you like in Action movies (e.g., themes, actors, style): I like movies with martial arts, minimal CGI, and strong character development.
```

The LLM will analyze your preferences and provide personalized recommendations based on the available movies in that genre.

## API and LLM Information

### TMDB API
This application uses the free TMDB API. The API key is already included in the script, but if you want to use your own:

1. Register for a free account at [The Movie Database](https://www.themoviedb.org/)
2. Request an API key from your account settings
3. Replace the `TMDB_API_KEY` value in the script with your own key

### Local LLM with Ollama
The application uses Ollama to run a free, open-source LLM locally on your machine. By default, it uses the Mistral model, which provides excellent accuracy for this type of task while being completely free and running locally.

Ollama benefits:
- Completely free and open-source
- All processing happens locally (privacy-preserving)
- No API keys or accounts required
- Good accuracy with models like Mistral
- Low latency since everything runs on your machine

## Available Genres

The application automatically fetches the latest genre list from TMDB, but here are the common genres you can use with the `recommend` command:

- Action
- Adventure
- Animation
- Comedy
- Crime
- Documentary
- Drama
- Family
- Fantasy
- History
- Horror
- Music
- Mystery
- Romance
- Science Fiction
- Thriller
- War
- Western

You can also use the `list` command to see all available genres.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

The movie data is provided by [The Movie Database (TMDB)](https://www.themoviedb.org/), but this project is not endorsed or certified by TMDB.

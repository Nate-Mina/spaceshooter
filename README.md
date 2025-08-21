# Space Invaders (Pygame)

A classic arcade-style Space Invaders game built with Python and Pygame. Control your spaceship, shoot down waves of enemies, collect power-ups, and aim for the highest score!

## Features
- Fast-paced arcade gameplay
- Power-ups: rapid fire, shield, and extra lives
- Animated explosions and starfield background
- Score and lives tracking

## Controls
- **Arrow keys**: Move your spaceship
- **Spacebar**: Shoot bullets

## Installation

1. **Install Python**
   - Download and install from [python.org](https://www.python.org/downloads/)
2. **Install dependencies**
   - Open a terminal in the project folder and run:
     ```
     pip install -r requirements.txt
     ```
   - Or, install via setup.py:
     ```
     pip install .
     ```

## Running the Game

- Run the game with:
  ```
  python main.py
  ```
- Or, if installed as a package:
  ```
  space-invaders
  ```

## Requirements
- Python 3.7+
- Pygame 2.0+

## Project Structure
- `main.py` - Main game loop and logic
- `player.py` - Player spaceship
- `enemy.py` - Enemy logic
- `bullet.py` - Bullets, power-ups, and explosions

## Django Web Integration

You can integrate this game into a Django-powered website to make it downloadable or playable online.

### 1. Install Django
```
pip install django
```

### 2. Create a Django Project and App
```
django-admin startproject mysite
cd mysite
python manage.py startapp spaceinvaders
```

### 3. Add Game Files
- Copy your game files (`main.py`, `player.py`, `enemy.py`, `bullet.py`, etc.) into the `spaceinvaders` app directory.
- (Optional) If you want to serve the game as a downloadable, place a zip or installer in the app's `static` folder.

### 4. Create a View and Template
- In `spaceinvaders/views.py`, add a view to render a page with game instructions and a download/play button.
- In `spaceinvaders/templates/`, create an HTML file for the game page.

### 5. Configure URLs
- Add a URL pattern in `spaceinvaders/urls.py` and include it in your project's `urls.py`.

### 6. Run the Server
```
python manage.py runserver
```

Visit `http://127.0.0.1:8000/spaceinvaders/` to access your game page.

---

For a full playable web version, you would need to port the game to JavaScript (e.g., using Pyodide or rewrite in JS). Otherwise, you can provide the game as a download or instructions to run locally.

Enjoy blasting enemies and chasing high scores!

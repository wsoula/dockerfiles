FROM python:3.11-slim

WORKDIR /app

# Copy all your game engine python scripts and the html web container frame
COPY main.py snake.py hangman.py platformer.py index.html ./

# Expose standard web traffic port
EXPOSE 8000

# Fire up a native python HTTP server to serve the static assets
CMD ["python", "-m", "http.server", "8000"]

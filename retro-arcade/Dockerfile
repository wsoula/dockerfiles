FROM python:3.11-slim

WORKDIR /app

# Copy all your game engine python scripts and the html web container frame
COPY main.py snake.py hangman.py platformer.py index.html shooter.py poop_simulator.py ./

# Initialize an empty scores repository inside the working directory
RUN mkdir -p /app/data && \
  echo '{"high_score": 0}' > /app/data/shooter.json && \
  echo '{"dollars": 30, "history": []}' > /app/data/poop_sim.json

# Create a lightweight Python web server script with a save API endpoint built-in
RUN echo 'import http.server, json, os\n\
class ArcadeServer(http.server.SimpleHTTPRequestHandler):\n\
  def do_POST(self):\n\
    length = int(self.headers["Content-Length"])\n\
    # Read data and strip trailing byte-junk or spacing buffers\n\
    raw_payload = self.rfile.read(length).decode("utf-8").strip()\n\
    try:\n\
      data = json.loads(raw_payload)\n\
      filename = "data/poop_sim.json" if self.path == "/save_poop" else "data/shooter.json"\n\
      with open(filename, "w") as f:\n\
        json.dump(data, f)\n\
        f.flush()\n\
        os.fsync(f.fileno())\n\
      self.send_response(200)\n\
    except Exception as e:\n\
      print("Save Error:", e)\n\
      self.send_response(500)\n\
    self.end_headers()\n\
  def do_GET(self):\n\
    if self.path in ["/load_poop", "/load"]:\n\
      self.send_response(200)\n\
      self.send_header("Content-Type", "application/json")\n\
      self.end_headers()\n\
      filename = "data/poop_sim.json" if self.path == "/load_poop" else "data/shooter.json"\n\
      with open(filename, "r") as f: self.wfile.write(f.read().encode())\n\
    else: super().do_GET()\n\
http.server.HTTPServer(("0.0.0.0", 8000), ArcadeServer).serve_forever()\n\
' > server.py


# Expose standard web traffic port
EXPOSE 8000

CMD ["python", "server.py"]

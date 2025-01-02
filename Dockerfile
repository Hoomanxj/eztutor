# 1. Base image
FROM python:3.12-slim

# 2. Install any OS-level dependencies if needed
# RUN apt-get update && apt-get install -y <packages> && rm -rf /var/lib/apt/lists/*

# 3. Create and use a working directory
WORKDIR /app

# 4. Copy your source code
COPY . /app

# 5. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 6. Expose port 5000 (the same port your app will listen on)
EXPOSE 5000

# 7. Final command to run your app
CMD gunicorn run:app --bind 0.0.0.0:5000
# 1. Base image
FROM python:3.12-slim

# 2. Install any OS-level dependencies if needed
# RUN apt-get update && apt-get install -y <packages> && rm -rf /var/lib/apt/lists/*

# 3. Create and use a working directory
WORKDIR /app

# 4. Copy your source code
COPY . /app

# 5. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 6. Expose port 5000 (the same port your app will listen on)
EXPOSE 5000

# 7. Final command to run your app
CMD gunicorn run:app --bind 0.0.0.0:5000

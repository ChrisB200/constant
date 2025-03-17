FROM python:3.12-slim

WORKDIR /app

# Install Poetry using pip
RUN pip install poetry

# Copy dependency files first (for caching layers)
COPY pyproject.toml poetry.lock /app/

# Install dependencies using Poetry
RUN poetry install --no-root

# Copy the rest of the application
COPY . /app/

# Expose port 8000
EXPOSE 8000

# Correct CMD command using the right Poetry path
CMD ["bash", "-c", "source ~/.bashrc && poetry run gunicorn -w 4 -b 0.0.0.0:8000 app:app"]


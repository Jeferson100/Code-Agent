FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Install UV
RUN pip install uv

# Set working directory
WORKDIR /app

# Create virtual environment using UV
RUN uv venv venv

# Activate virtual environment
ENV PATH="/app/venv/bin:$PATH"

# Copy dependency files first (para melhor cache)
COPY requirements.txt pyproject.toml ./

# Install dependencies
RUN uv pip install -r pyproject.toml

COPY . .

# Expose port
EXPOSE 3000

# Start the application
CMD ["python", "-m", "uvicorn", "app.app_fastapi:app", "--host", "0.0.0.0", "--port", "3000"]
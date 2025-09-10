# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-slim-bullseye

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install project dependencies from pyproject.toml
COPY pyproject.toml .
RUN python -m pip install --no-cache-dir .

# Copy the rest of the application code
COPY . .

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
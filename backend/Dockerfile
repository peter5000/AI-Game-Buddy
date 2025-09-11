# Use Python 3.10 for compatibility
FROM python:3.10-slim-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Create non-root user
RUN adduser --uid 5678 --disabled-password --gecos "" --no-create-home appuser

# Set working directory
WORKDIR /app

# Copy and install Python dependencies first (better layer caching)
COPY --chown=appuser:appuser pyproject.toml .

# Install Python dependencies
RUN python -m pip install --no-cache-dir .

# Copy application code
COPY --chown=appuser:appuser backend/ .

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
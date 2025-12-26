# Use a specific, small base image
FROM python:3.9-slim

# Create a non-root user for security (UID 10001)
RUN groupadd -g 10001 appuser && \
    useradd -u 10001 -g appuser appuser

WORKDIR /app

# Install dependencies first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY app.py .

# Switch to non-root user
USER 10001

# Command to run
CMD ["python", "app.py"]

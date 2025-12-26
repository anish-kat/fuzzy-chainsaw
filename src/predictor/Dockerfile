FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app.py .

# Create a home directory for kagglehub cache and set permissions
ENV HOME=/tmp
RUN chmod -R 777 /tmp

CMD ["python", "app.py"]

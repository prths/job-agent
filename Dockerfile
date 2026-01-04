FROM python:3.12-slim

# Prevent python buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose ports
EXPOSE 8000
EXPOSE 8501

# Start FastAPI + Streamlit
CMD ["bash", "-c", "python -m app.api.main & streamlit run ui/app.py --server.port 8501 --server.address 0.0.0.0"]

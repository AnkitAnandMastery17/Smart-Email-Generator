# ================================
# Smart Email Generator - Dockerfile
# ================================

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the app
COPY . /app

# Expose Streamlit port
EXPOSE 8501

# Default command to run Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

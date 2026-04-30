# Use python base image
FROM python:3.11-alpine

# Set working directory inside container
WORKDIR /app

# Copy requirements first
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy all project files
COPY . .

# Expose port (Streamlit uses 8501)
EXPOSE 8501

# Run the app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
FROM python:3.10-slim

# Install system dependencies including OpenJDK (required for Apache Spark)
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-jdk \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME="/usr/lib/jvm/default-java"
ENV PATH="${JAVA_HOME}/bin:${PATH}"

WORKDIR /app

# Copy dependency specifications
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy source repository
COPY . .

# Expose Streamlit dashboard port
EXPOSE 8501

CMD ["streamlit", "run", "dashboard/app.py", "--server.port=8501", "--server.address=0.0.0.0"]

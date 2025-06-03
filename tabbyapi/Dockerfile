FROM python:3.11-slim

WORKDIR /app

# Install necessary system dependencies
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Clone TabbyAPI repository
RUN git clone https://github.com/theroyallab/tabbyAPI.git .

# Install Python dependencies
RUN pip install --upgrade pip && pip install .[cu121]  # Adjust for your GPU setup

# Copy configuration files if needed
# COPY config.yml /app/config.yml
# COPY api_keys.yml /app/api_keys.yml

EXPOSE 5000

CMD ["python", "main.py"]

# Use your custom Python base image
FROM python:3.9-slim

# Update and install bash if not already included
RUN apt-get update && apt-get install -y bash

COPY requirements.txt /requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# Copy the contents of the repository into the container
COPY . /app
WORKDIR /app

# Configure Streamlit settings
RUN printf "[server]\nenableCORS = false\n" > .streamlit/config.toml

# Expose port
ENV PORT 8080

# Run streamlit app
CMD ["streamlit", "run", "main.py", "--server.port", "8080"]

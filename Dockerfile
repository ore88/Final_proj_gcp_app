FROM python:3.8.0-slim

WORKDIR /app
ADD . /app

# Upgrade PIP
RUN pip install --upgrade pip

#Install python libraries from requirements.txt
RUN pip install -r requirements.txt

# Set $PORT environment variable
ENV PORT 8080

# Run the web service on container startup
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app

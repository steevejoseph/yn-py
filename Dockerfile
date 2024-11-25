# syntax=docker/dockerfile:1
FROM python:3.9-slim-buster
WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

# Set an environment variable to configure the port (default to 8080)
ENV PORT=8080

# Expose the port the application will listen on
EXPOSE 8080

RUN chdmod 755 firebase.json

CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=8080" ]
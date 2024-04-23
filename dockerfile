FROM python:3.10.12-slim-buster

# Create the MongoDB data directory
RUN mkdir -p /data/db

# Create the MongoDB data directory
RUN mkdir -p /data/code

# Update os
RUN apt-get update

# Install tmux for run mongodb
RUN apt-get install -y tmux

# Install MongoDB
RUN apt-get install gnupg wget -y
RUN wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | apt-key add -
RUN echo "deb http://repo.mongodb.org/apt/debian buster/mongodb-org/6.0 main" | tee /etc/apt/sources.list.d/mongodb-org-6.0.list
RUN apt-get update
RUN apt-get install -y mongodb-org

# Copy local code to container
COPY . /app

# Expose MongoDB port
EXPOSE 27017

# Install Python dependencies
RUN pip3 install -r /app/requirements.txt

# Set the working directory
WORKDIR /app

# Start mongodb
# Run the Python script
CMD tmux new-session -s mongodb -d 'mongod'; python3 main.py
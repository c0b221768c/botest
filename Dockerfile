# Base image:
FROM ubuntu:latest

# Package installation
RUN apt-get update && apt-get install -y curl

# Install uv and set up the environment
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Set the environment variables
ENV PATH="/root/.local/bin/:$PATH"

# Set the working directory
WORKDIR /root/local/app

# Copy the source code
COPY . .

# Install the dependencies
RUN uv sync
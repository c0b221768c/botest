# Base image:
FROM ubuntu:latest

# Package installation
# curl, git, github-cli
RUN apt-get update && apt-get install -y curl git gh

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Set the environment variables
ENV PATH="/root/.local/bin/:$PATH"

# Set the working directory
WORKDIR /usr/local/app

# Copy the source code
COPY . .

# Install the dependencies
RUN uv sync

# Default command
CMD ["uv", "run", "src/bot.py"]
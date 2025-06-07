# Use an official Python runtime as a parent image
# Choose a specific slim version compatible with Raspberry Pi's ARM architecture
# For example, for Python 3.11 on a Raspberry Pi 4 (ARMv7/ARM64):
FROM python:3.11-slim-bullseye

# Set the working directory in the container
WORKDIR /app

# Copy the contents of the Sr directory (relative to the Dockerfile)
# into the container's /app directory
COPY . /app/

# If you have a requirements.txt file in your Sr directory, uncomment the next two lines:
# COPY ./rasp_pi/requirements.txt /app/
 RUN pip install --no-cache-dir -r requirements.txt

# Command to run your application (replace your_app.py with your main script)
 CMD ["python", "__main__.py"]

# If you don't have a specific script to run, you can keep the container running for debugging:
# CMD ["tail", "-f", "/dev/null"]
FROM balenalib/raspberrypi3-python:latest

# Install required packages
RUN apt-get update && apt-get install -y \
    libatlas-base-dev \
    libjasper-dev \
    python3-opencv

# Set working directory
WORKDIR /app

# Copy the camera streaming script
COPY video_stream.py camera_stream.py 

# Run the camera streaming script
CMD ["python3", "camera_stream.py"]


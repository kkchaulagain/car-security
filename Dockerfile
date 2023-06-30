FROM balenalib/raspberry-pi-python:latest
RUN pip install --upgrade pip

RUN apt-get update && apt-get install -y \
    python3-dev \
    build-essential \
    cmake
RUN pip install --no-cache-dir numpy


# Install OpenCV
RUN pip install opencv-python-headless

CMD ["bash"]

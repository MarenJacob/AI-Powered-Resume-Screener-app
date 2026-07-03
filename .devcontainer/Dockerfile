FROM mcr.microsoft.com/devcontainers/python:3.11

RUN sudo apt-get update && \
    sudo apt-get install -y \
    poppler-utils \
    tesseract-ocr \
    libgl1 \
    libglib2.0-0 \
    git

WORKDIR /workspace
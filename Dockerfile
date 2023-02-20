# syntax=docker/dockerfile:1
# app/Dockerfile

FROM python:3.10.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY src/* .

ENTRYPOINT ["python", "claim_validator_rewards.py"]
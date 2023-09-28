# syntax=docker/dockerfile:1

FROM python:3.10-bullseye

EXPOSE 7865
EXPOSE 5000

WORKDIR /app

COPY . .

RUN apt update && apt install -y git make
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 aria2  -y

RUN pip3 install torch torchaudio --extra-index-url https://download.pytorch.org/whl/cu118
RUN pip3 install -r requirements.txt
RUN pip3 install torch torchaudio --extra-index-url https://download.pytorch.org/whl/cu118

CMD ["python3", "infer_api.py"]
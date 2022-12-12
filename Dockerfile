FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .

RUN apt-get update \
    && apt-get install libasound-dev portaudio19-dev libportaudio2 \
    libavcodec-extra \
    libportaudiocpp0 ffmpeg build-essential -y
RUN pip install --upgrade pip -r requirements.txt

# Нужно для работы библиотеки Spacy. Т.н. модель распознования
RUN python -m spacy download ru_core_news_sm

COPY . .

CMD uvicorn main:app \
    --host 0.0.0.0 \
    --port 8007
EXPOSE 8007

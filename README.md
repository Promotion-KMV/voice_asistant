## About
В этом проекте реализован голосовой помощник.  
С её помощью пользователь может осуществлять поиск информации по фильмам и сериалам,  
актёрам и режиссёрам в нашем сервисе MovieApi с помощью голоса.  
голосовой помощник умеет преобразовывать голосовой запрос  
пользователя в текст, понять суть вопроса, запросить нужную информацию по фильмам/актёрам  
и ответить пользователю голосом. Для демонстрации способностей Греты, в проекте сделан  
простой чат, который позволяет пообщаться с Гретой.

## Very QuickStart MovieApi
### 1) make start
etl упадёт, так как не найдёт в postgres данных. Это норма
### 2) make insert-data
### 3) Установка модели Spacy (Для локального запуска)
Так же необходимо скачать и установить модель для опредения смысла в запросе с помощью команды:

`python -m spacy download ru_core_news_sm`

где `ru_core_news_sm` - название модели.

Это название необходимо поместить в переменную окружения `SPACY_MODEL_NAME`

Для русского языка доступны на выбор 3 модели, отличающиеся по размеру и степени обученности.:
- `ru_core_news_sm` 
- `ru_core_news_md` 
- `ru_core_news_lg`

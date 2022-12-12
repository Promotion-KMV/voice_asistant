from config import get_config
from director.models import DirectorResult, SearchKey, FilterKey

from movie_api.response_abc import ResponseABC
from movie_api.models import PersonResponse, FilmResponse

settings = get_config().mv

filter_key = FilterKey

search_key = SearchKey


async def call_desire_api(result: DirectorResult):
    """Для определения вызова нужного класса, вызывается из director"""
    if result.search_key == search_key.filmwork:
        return await ResponseFilm(settings.url_film % result.search_string).generation_response(result.filters)
    if result.search_key == search_key.person:
        return await ResponsePerson(settings.url_person % result.search_string).generation_response(result.filters)


class ResponseFilm(ResponseABC):
    """Формируем ответы по запросам фильмов"""

    async def generation_response(self, filters: dict) -> str:
        """Формирование логически правильного ответа"""
        data_response = await self.get_response()
        if isinstance(data_response, str):
            return await self.get_response()
        data_response = FilmResponse(**data_response)
        filters_key = list(filters.keys())[0].value
        message_dict = {filter_key.date.value:
                            f'фильм {data_response.title} сняли {"".join(data_response.created)}',
                        filter_key.actor.value:
                            f'В фильме {data_response.title} снимались актеры {", ".join(data_response.actors)}',
                        'description':
                            f'Описание фильма {data_response.title}. {data_response.description}',
                        filter_key.genre.value:
                            f'Жанры фильма {data_response.title} {", ".join(data_response.genre)}',
                        filter_key.director.value:
                            f'Режисер фильма {data_response.title}{" ".join(data_response.directors)}'}
        return message_dict[filters_key] if filters_key in message_dict.keys() else settings.empty_message


class ResponsePerson(ResponseABC):
    """Формируем ответы по запросам персон"""

    async def generation_response(self, filters) -> str:
        data_response = await self.get_response()
        if isinstance(data_response, str):
            return await self.get_response()
        data_response = PersonResponse(**data_response)
        if len(filters) == 1:
            filters_key = list(filters.keys())[0].value
            message_dict = {filter_key.filmwork.value:
                                f'Актер {data_response.name} снялся в фильмах {", ".join(data_response.actor)}'
                                if data_response.actor else settings.empty_message,
                            filter_key.director.value:
                                f'Режисер {data_response.name} снял фильмы {", ".join(data_response.director)}'
                                if data_response.director else settings.empty_message}
            return message_dict[filters_key] if filters_key in message_dict.keys() else settings.empty_message
        else:
            generation_difficult_response = self.helper_generation(filters, data_response)
            if filter_key.filmwork.value in generation_difficult_response['filters_keys']:
                message_dict = {filter_key.filmwork.value:
                                    f'Актер {data_response.name} снялся в '
                                    f'{generation_difficult_response["filter_values"][0]}: '
                                    f'{", ".join(generation_difficult_response["lst_film"])}'
                                    if generation_difficult_response["lst_film"] else settings.empty_message}
                return message_dict[generation_difficult_response['filters_keys'][0]]
            if filter_key.director.value in generation_difficult_response['filters_keys']:
                message_dict = {filter_key.director.value:
                                    f'Режисер {data_response.name}'
                                    f' снял {generation_difficult_response["filter_values"][0]}:'
                                    f' {", ".join(generation_difficult_response["lst_film"])}'
                                    if generation_difficult_response["lst_film"] else settings.empty_message}
                return message_dict[generation_difficult_response['filters_keys'][0]]

    def helper_generation(self, filters, data_response) -> dict:
        """Помощь формирования ответе из нескольких фильтров"""
        filters_keys = list(filters.keys())
        filter_values = list(filters.values())[1]
        created_data = {}
        filter_val = ''
        if filter_key.filmwork.value and filter_key.genre.value in filters_keys \
                or filter_key.director.value and filter_key.genre.value in filters_keys:
            for i in settings.lst_genre:
                if i[:4] == filter_values[0][:4]:
                    filter_val = i
        lst_film = []
        for k, v in data_response.genre_actor.items():
            if filter_val in v:
                lst_film.append(k)
        created_data['filters_keys'] = filters_keys
        created_data['filter_values'] = filter_values
        created_data['lst_film'] = lst_film

        return created_data

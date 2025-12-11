from source.handler_files import HandlerFiles
from source.handler_info_city import HandlerInfo
from source.handler_weather import HandlerWeather
from datetime import datetime, timedelta

class WebFunc:
    def __init__(self):
        self.roads_handler_free = HandlerFiles('free-trails_city.json')
        self.roads_handler_toll = HandlerFiles('toll_trails_city.json')
        self.train_handler = HandlerFiles('train_ways.json')
        self.plane_handler = HandlerFiles('plane_ways.json')
        self.detail_info = HandlerInfo('detailed_info_about_cities.json', flag_detail=True)
        self.simple_info = HandlerInfo('info_city.json')
        self.weather_handler = HandlerWeather('weather.json')

    @staticmethod
    def _calculate_weather_modifier(dataframe_from, dataframe_to):
        if dataframe_from.empty or dataframe_to.empty:
            return 1.0
        def compute_modifier_for_city(dataframe):
            avg_visibility = dataframe['visibility'].mean()
            avg_precipitation = dataframe['precipitation'].mean()
            avg_wind_speed = dataframe['wind_speed'].mean()
            modifier = 1.0
            # Видимость
            if avg_visibility < 3:
                modifier += 0.25
            elif avg_visibility < 6:
                modifier += 0.1
            elif avg_visibility < 8:
                modifier += 0.05
            elif avg_visibility < 10:
                modifier += 0.02

            # Влажность
            if avg_precipitation > 15:
                modifier += 0.20
            elif avg_precipitation > 5:
                modifier += 0.10
            elif avg_precipitation > 1:
                modifier += 0.03

            # Ветер
            if avg_wind_speed > 15:
                modifier += 0.10
            elif avg_wind_speed > 10:
                modifier += 0.05

            return modifier

        mod_from = compute_modifier_for_city(dataframe_from)
        mod_to = compute_modifier_for_city(dataframe_to)

        avg_mod = (mod_from + mod_to) / 2.0
        return min(avg_mod, 1.35)

    @staticmethod
    def calculate_finish_date(start_date, time_delta):
        """
        Функция вычисления даты конца поездки по заданному дню старта и длительности поездки.
        :param start_date: Дата начала поездки.
        :param time_delta: Длительность поездки в часах
        :return: finish_date - дата конца поездки (str)
        """
        start_dt = datetime.fromisoformat(start_date) # ISO формат даты как раз YYYY-MM-DD
        finish_dt = start_dt + timedelta(hours=time_delta)
        return finish_dt.date().isoformat()

    def _correct_time(self, to, fr, date_start, transport):
        """
        Функция получения затрат по времени (в часах) на путешествие на указанном виде транспорта.
        :param to: Куда путешествуем.
        :param fr: Откуда путешествуем.
        :param date_start: Стартовая дата.
        :param transport: Вид транспорта
        :return: время на путешествие из fr в to на transport
        """
        if transport == "train":
            base_time = self.train_handler.get_info_route(to, fr)['time']
            cor_time = base_time
        elif transport == "plane":
            base_time = self.plane_handler.get_info_route(to, fr)['time']
            weather_data_from = self.weather_handler.get_info_weather(date_start, fr)
            weather_data_to = self.weather_handler.get_info_weather(date_start, to)
            cor_time = base_time + WebFunc._calculate_weather_modifier(weather_data_from, weather_data_to)
        elif transport == "toll_trails":
            base_time = float(self.roads_handler_toll.get_info_route(to, fr)['time'])
            cor_time = base_time
        elif transport == "free_trails":
            base_time = float(self.roads_handler_free.get_info_route(to, fr)['time'])
            cor_time = base_time
        else:
            raise KeyError("Неизвестный вид транспорта.")
        return cor_time

    def sorted_mass_time(self, to, fr, date_start):
        """
        Возвращает список кортежей (время в часах, вид транспорта), отсортированный по времени.
        :param to: Город, из которого мы планируем начать путешествие.
        :param fr: Город, в который мы планируем приехать
        :param date_start: День начала путешествия
        :return: Список кортежей вида [(время, 'transport_type'), ...], отсортированный по времени.
        """
        time = [
            (self._correct_time(to=to, fr=fr, date_start=date_start, transport="train"), 'train'),
            (self._correct_time(to=to, fr=fr, date_start=date_start, transport="plane"), 'plane'),
            (self._correct_time(to=to, fr=fr, date_start=date_start, transport="toll_trails"), 'toll_trails'),
            (self._correct_time(to=to, fr=fr, date_start=date_start, transport="free_trails"), 'free_trails')
        ]
        return sorted(time, key=lambda x: x[0])

    def sorted_mass_cost(self, to, fr):
        """
        Возвращает список кортежей (стоимость, вид транспорта), отсортированный по стоимости
        :param to: Город, из которого мы планируем начать путешествие.
        :param fr: Город, в который мы планируем приехать
        :return: Список кортежей вида [(стоимость, 'transport_type'), ...], отсортированный по стоимости.
        """
        costs = [
            (self.train_handler.get_info_route(to, fr)['cost'], "train"),
            (self.plane_handler.get_info_route(to, fr)['cost'], "plane"),
            (self.roads_handler_toll.get_info_route(to, fr)['fuel_cost'] +
             self.roads_handler_toll.get_info_route(to, fr)['trails_cost'], "toll_trails"
            ),
            (self.roads_handler_free.get_info_route(to, fr)['fuel_cost'], "free_trails"),
        ]
        return sorted(costs, key=lambda x: x[0])
import os
import json
import pandas as pd

class HandlerWeather:
    def __init__(self, file_name):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.json_path = os.path.join(self.current_dir, '..', 'data', file_name)
        try:
            with open(self.json_path, 'r', encoding='utf-8') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            print(f"Файл {self.json_path} не найден.")

    def get_info_weather(self, date: str, city: str = None) -> pd.DataFrame:
        """
        Находит информацию о погоде в конкретную дату, в конкретном городе. Если город не задан,
        то выводит информацию для всех городов
        :param date: Дата, по которой хотим получить данные о погоде.
                     Формат даты: YYYY-MM-DD
        :param city: Название города (опционально), для которого мы хотим получить данные о погоде.
                     Если не указан (city=None), то выведется информация обо всех городах в этот день.
        :return: Возвращает объект данных в виде DataFrame (либо в виде списка DataFrame).
        """
        records = []
        for city_data in self.data:
            if city is not None and city_data['city'] != city:
                continue
            for day in city_data['data']:
                if day['date'] == date:
                    for period_name, period_data in day['periods'].items():
                        record = {
                            'city': city_data['city'],
                            'date': day['date'],
                            'period': period_name,
                            'temperature': period_data['temperature'],
                            'precipitation': period_data['precipitation'],
                            'visibility': period_data['visibility'],
                            'wind_speed': period_data['wind_speed'],
                            'weather_phenomenon': period_data['weather_phenomenon']
                        }
                        records.append(record)
                    break
        return pd.DataFrame(records)
import json
import os
import translations


class HandlerInfo:

    def __init__(self, file_name, flag_detail=False):
        self.name_key = "name"
        if flag_detail:
            self.name_key = "city_name"

        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.json_path = os.path.join(self.current_dir, '..', 'data', file_name)
        try:
            with open(self.json_path, 'r', encoding='utf-8') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            print(f"Файл {self.json_path} не найден.")


    def get_info_city(self, name):
        """
        Находит информацию о городе по его названию.

        Args:
            :param name: Название города на русском языке.

        Returns:
            dict: Словарь с информацией о городе.
                  Если город не найден, возвращает пустой словарь {}.
        """
        trans = translations.CITY_TRANSLATIONS
        city_key = trans[f"{name}"]["en"]

        if city_key not in self.data.get("cities", {}):
            raise KeyError("Такого города нету.")

        city_info = self.data["cities"][city_key]

        result = {}
        for key, value in city_info.items():
            if key == "name":
                result[self.name_key] = value
            else:
                result[key] = value

        return result
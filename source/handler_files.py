import json
import os
import translations

class HandlerFiles:

    def __init__(self, name_file):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.json_path = os.path.join(self.current_dir, '..', 'data', name_file)
        with open(self.json_path, 'r', encoding='utf-8') as file:
            self.data = json.load(file)

    def get_info_route(self, to, fr):
        """
            Находит информацию о маршруте из города A в город B.
            Args:
                A - (str): Название города отправления (на русском).
                B - (str): Название города назначения (на русском).
            Returns:
                list: Список словарей с информацией о маршруте.
                      Если маршрут не найден, возвращает пустой список.
        """
        trans = translations.CITY_TRANSLATIONS
        from_city_key = trans[f"{to}"]["en"]
        routes_key = f"routes_from_{from_city_key}"
        if routes_key not in self.data.get("routes", {}):
            raise KeyError("Такого маршрута нету.")
        target_route_name = f"{to}-{fr}"
        route_info = {}
        for key in self.data["routes"][routes_key]:
            if key["route"] == target_route_name:
                route_info = key

        return route_info
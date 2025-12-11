import matplotlib.pyplot as plt
from source.handler_files import HandlerFiles


def plot_transport(to: str, fr: str, filter: str, type: str):
    """
    Строит график зависимости вида транспорта от выбранного фильтра (цена, время, расстояние).

    Args:
        to (str): Город отправления (на русском)
        fr (str): Город назначения (на русском)
        filter (str): 'price', 'time', или 'dist'
        type (str): 'bar' — столбчатый, 'line' — линейный
    """
    roads_handler_free = HandlerFiles('free-trails_city.json')
    roads_handler_toll = HandlerFiles('toll_trails_city.json')
    train_handler = HandlerFiles('train_ways.json')
    plane_handler = HandlerFiles('plane_ways.json')
    transport_types = ['Поезд', 'Самолёт', 'Платные трассы', 'Бесплатные трассы']
    values = []

    try:
        # Поезд
        train_data = train_handler.get_info_route(to, fr)
        if filter == 'cost':
            train_val = train_data['cost']
        elif filter == 'time':
            train_val = train_data['time']
        else:
            raise ValueError("Filter должен быть 'price', 'time' или 'dist'")
        values.append(train_val)

        # Самолёт
        plane_data = plane_handler.get_info_route(to, fr)
        if filter == 'cost':
            plane_val = plane_data['cost']
        elif filter == 'time':
            plane_val = plane_data['time']
        else:
            raise ValueError("Filter должен быть 'price', 'time' или 'dist'")
        values.append(plane_val)

        # Платные трассы
        toll_data = roads_handler_toll.get_info_route(to, fr)
        if filter == 'cost':
            toll_val = toll_data['fuel_cost'] + toll_data['trails_cost']
        elif filter == 'time':
            toll_val = toll_data['time']
        else:
            raise ValueError("Filter должен быть 'price', 'time' или 'dist'")
        values.append(toll_val)

        # Бесплатные трассы
        free_data = roads_handler_free.get_info_route(to, fr)
        if filter == 'cost':
            free_val = free_data['fuel_cost']  # нет платных дорог
        elif filter == 'time':
            free_val = free_data['time']
        else:
            raise ValueError("Filter должен быть 'price', 'time' или 'dist'")
        values.append(free_val)

    except KeyError as e:
        raise ValueError(f"Данные для маршрута '{to}-{fr}' не найдены: {e}")
    except Exception as e:
        raise ValueError(f"Ошибка при получении данных: {e}")

    if filter == 'cost':
        label = 'Цена (руб.)'
    elif filter == 'time':
        label = 'Время (часов)'

    plt.figure(figsize=(10, 6))

    if type == 'bar':
        colors = ['blue', 'green', 'orange', 'gray']
        plt.bar(transport_types, values, color=colors)
        plt.ylabel(label)
        plt.title(f'Зависимость {label.lower()} от вида транспорта ({to} → {fr})')

    elif type == 'line':
        plt.plot(transport_types, values, marker='o', color='b', linewidth=2)
        plt.ylabel(label)
        plt.title(f'Зависимость {label.lower()} от вида транспорта ({to} → {fr})')

    else:
        raise ValueError("Type должен быть 'bar' или 'line'")

    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

plot_transport(to="Москва", fr="Казань", filter="cost", type="bar")
plot_transport(to="Санкт-Петербург", fr="Москва", filter="time", type="line")
plot_transport(to="Элиста", fr="Псков", filter="cost", type="bar")
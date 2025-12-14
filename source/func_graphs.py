import os

import matplotlib.pyplot as plt
from io import BytesIO
import base64
from source.handler_files import HandlerFiles

def plot_transport(to: str, fr: str, filter_name: str, type_name: str):
    """
    Строит график зависимости вида транспорта от выбранного фильтра (цена, время, расстояние).
    Возвращает base64-строку изображения графика зависимости вида транспорта от выбранного фильтра.
    Args:
        to (str): Город отправления (на русском)
        fr (str): Город назначения (на русском)
        filter_name (str): 'price', 'time', или 'dist'
        type_name (str): 'bar' — столбчатый, 'line' — линейный
    Returns:
        str: base64-строка изображения PNG графика
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
        if filter_name == 'cost':
            train_val = train_data['cost']
        elif filter_name == 'time':
            train_val = train_data['time']
        else:
            raise ValueError("Filter должен быть 'price', 'time' или 'dist'")
        values.append(train_val)

        # Самолёт
        plane_data = plane_handler.get_info_route(to, fr)
        if filter_name == 'cost':
            plane_val = plane_data['cost']
        elif filter_name == 'time':
            plane_val = plane_data['time']
        else:
            raise ValueError("Filter должен быть 'price', 'time' или 'dist'")
        values.append(plane_val)

        # Платные трассы
        toll_data = roads_handler_toll.get_info_route(to, fr)
        if filter_name == 'cost':
            toll_val = toll_data['fuel_cost'] + toll_data['trails_cost']
        elif filter_name == 'time':
            toll_val = toll_data['time']
        else:
            raise ValueError("Filter должен быть 'price', 'time' или 'dist'")
        values.append(toll_val)

        # Бесплатные трассы
        free_data = roads_handler_free.get_info_route(to, fr)
        if filter_name == 'cost':
            free_val = free_data['fuel_cost']  # нет платных дорог
        elif filter_name == 'time':
            free_val = free_data['time']
        else:
            raise ValueError("Filter должен быть 'price', 'time' или 'dist'")
        values.append(free_val)

    except KeyError as e:
        raise ValueError(f"Данные для маршрута '{to}-{fr}' не найдены: {e}")
    except Exception as e:
        raise ValueError(f"Ошибка при получении данных: {e}")

    label = ""
    if filter_name == 'cost':
        label = 'Цена (руб.)'
    elif filter_name == 'time':
        label = 'Время (часов)'
    plt.figure(figsize=(10, 6))
    if type_name == 'bar':
        colors = ['blue', 'green', 'orange', 'gray']
        plt.bar(transport_types, values, color=colors)
    elif type_name == 'line':
        plt.plot(transport_types, values, marker='o', color='b', linewidth=2)
    else:
        plt.close()
        raise ValueError("Type должен быть 'bar' или 'line'")

    plt.ylabel(label)
    plt.title(f'Зависимость {label.lower()} от вида транспорта ({to} → {fr})')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    # сохраняем в буфер
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return img_base64

def save_plot_as_png(to: str, fr: str, date: str,  filter_name: str, type_name: str, output_dir: str):
    """
    Генерирует график и сохраняет его как PNG-файл в указанную директорию.
    Args:
        to (str): Город назначения
        fr (str): Город отправления
        filter_name (str): 'cost' или 'time'
        type_name (str): 'bar' или 'line'
        output_dir (str): Путь к папке для сохранения
    Returns:
        str: Путь к сохранённому файлу
    """

    img_base64 = plot_transport(fr=fr, to=to, filter_name=filter_name, type_name=type_name)

    save_from = fr.replace(' ', '_')
    save_to = to.replace(' ', '_')
    filename = f"{save_from}_{save_to}_{date}_{filter_name}.png"
    filepath = os.path.join(output_dir, filename)

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    img_data = base64.b64decode(img_base64)
    with open(filepath, 'wb') as f:
        f.write(img_data)
    return filepath

def get_plot_from_file(filepath: str):
    """
    Функция п
    :param filepath: Путь к файлу
    :return: base64-строку изображения
    """
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'rb') as f:
        img_data = f.read()

    return base64.b64encode(img_data).decode('utf-8')
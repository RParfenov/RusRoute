import matplotlib.pyplot as plt
import pandas as pd
import json
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(current_dir, '..', 'data', 'weather.json')


def load_weather_data():
    with open(data_dir, 'r', encoding='utf-8') as json_file:
        weather_data = json.load(json_file)

    records = []

    for city_data in weather_data:
        city_name = city_data['city']
        for day in city_data['data']:
            date = day['date']
            for period_name, period_data in day['periods'].items():
                record = {
                    'city': city_name,
                    'date': date,
                    'period': period_name,
                    'temperature': period_data['temperature'],
                    'precipitation': period_data['precipitation'],
                    'visibility': period_data['visibility'],
                    'wind_speed': period_data['wind_speed'],
                    'weather_phenomenon': period_data['weather_phenomenon']
                }
                records.append(record)
    return pd.DataFrame(records)


def visualize_weather_impact(weather_data):
    weather_counts = weather_data['weather_phenomenon'].value_counts()

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(24, 12))
    ax1.bar(range(len(weather_counts)), weather_counts.values)
    ax1.set_xticks(range(len(weather_counts)))
    ax1.set_xticklabels(weather_counts.index, rotation=45, ha='right')
    ax1.set_ylabel('Количество периодов')
    ax1.set_title('Распределение погодных явлений', fontweight='bold')
    ax1.grid(True, alpha=0.3)

    months = ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн',
              'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек']

    moscow_weather = weather_data[weather_data['city'] == 'Москва'].copy()
    moscow_weather['date'] = pd.to_datetime(moscow_weather['date'])
    moscow_weather['month'] = moscow_weather['date'].dt.month

    monthly_temp = moscow_weather.groupby('month')['temperature'].agg(['mean', 'std'])

    ax2.errorbar(range(1, 13), monthly_temp['mean'], yerr=monthly_temp['std'], marker='o', linewidth=2,
                 capsize=5, color='red', alpha=0.7)
    ax2.set_xticks(range(1, 13))
    ax2.set_xticklabels(months)
    ax2.set_ylabel('Температура (°C)')
    ax2.set_title('Сезонность температуры (Москва)', fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.axhline(y=0, color='black', linestyle='--', alpha=0.5)

    bad_weather = ['дождь', 'снег с дождем', 'снег', 'мокрый снег']
    city_bad_weather = weather_data[weather_data['weather_phenomenon'].isin(bad_weather)]
    city_bad_counts = city_bad_weather['city'].value_counts().head(
        10)  # топ 10 городов с максимальным числом периодов с плохой погодой

    ax3.barh(range(len(city_bad_counts)), city_bad_counts.values, color='orange', alpha=0.7)
    ax3.set_yticks(range(len(city_bad_counts)))
    ax3.set_yticklabels(city_bad_counts.index)
    ax3.set_xlabel('Периоды с плохой погодой')
    ax3.set_title('Топ 10 городов с максимальным числом периодов с плохой погодой')
    ax3.grid(True, alpha=0.3)
    ax3.invert_yaxis()

    visibility_bins = [1, 3, 5, 10]
    visibility_labels = ['1-3 км', '3-5 км', '5-10 км']

    weather_data['visibility_category'] = pd.cut(weather_data['visibility'],
                                                 bins=visibility_bins, labels=visibility_labels)
    visibility_counts = weather_data['visibility_category'].value_counts()

    ax4.pie(visibility_counts.values, labels=visibility_counts.index, autopct='%1.1f%%',
            colors=['#ff6b6b', '#ffa726', '#ffee58', '#66bb6a', '#42a5f5'])
    ax4.set_title('Распределение видимости', fontweight='bold')

    plt.tight_layout()
    plt.show()


weather_df = load_weather_data()
visualize_weather_impact(weather_df)

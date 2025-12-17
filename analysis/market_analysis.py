import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import json

current_dir = os.path.dirname(os.path.abspath(__file__))
destination = os.path.join(current_dir, '..', 'data', 'popular_routes.csv')
destination_detailed_info = os.path.join(current_dir, '..', 'data', 'detailed_info_about_cities.json')
destination_info_city = os.path.join(current_dir, '..', 'data', 'info_city.json')

def load_info_cities(path):
    with open(path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    return pd.DataFrame(data['cities'].values())

def calculate_data_for_matrix(df_info_city, df_detailed_info):
    # 1. расстояние между городами
    latitude = df_info_city['width'].values
    longitude = df_info_city['longitude'].values
    lat1 = np.radians(latitude[:, np.newaxis])
    lat2 = np.radians(latitude[np.newaxis, :])
    lon1 = np.radians(longitude[:, np.newaxis])
    lon2 = np.radians(longitude[np.newaxis, :])
    d_lat = lat2 - lat1
    d_lon = lon2 - lon1
    a = np.sin(d_lat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(d_lon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    distance_matrix = 6371 * c

    # 2. разница в зарплатах
    salary = df_detailed_info['average_salary'].values
    sal1 = salary[:, np.newaxis]
    sal2 = salary[np.newaxis, :]
    d_sal = sal2 - sal1

    return distance_matrix, d_sal

def add_route_features(df_popular_routes, df_info_city, df_detailed_info):
    distance_matrix, d_sal = calculate_data_for_matrix(
        df_info_city, df_detailed_info
    )

    city_to_idx = {name: idx for idx, name in enumerate(df_info_city['name'])}

    df_popular_routes['from_idx'] = df_popular_routes['city_from'].map(city_to_idx)
    df_popular_routes['to_idx'] = df_popular_routes['city_to'].map(city_to_idx)
    df_popular_routes = df_popular_routes.dropna(subset=['from_idx', 'to_idx']).astype({'from_idx': int, 'to_idx': int})

    df_popular_routes['distance_km'] = distance_matrix[df_popular_routes['from_idx'], df_popular_routes['to_idx']]
    df_popular_routes['salary_diff'] = d_sal[df_popular_routes['from_idx'], df_popular_routes['to_idx']]

    return df_popular_routes

def visualize_market_analysis():
    top_20 = 20 # рассматриваем топ 20 самых популярных маршрутов
    df_popular_routes = pd.read_csv(destination)

    sorted_df = df_popular_routes.sort_values(by=['estimated_travelers_per_year'], ascending=False)
    top_20_df = sorted_df.head(top_20)

    routes = [f"{row['city_from']} - {row['city_to']}" for _, row in top_20_df.iterrows()]
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(24, 12), constrained_layout=True)
    # График 1. Топ 20 маршрутов
    ax1.barh(routes, top_20_df.estimated_travelers_per_year)
    ax1.set_title('Топ 20 самых популярных маршрутов')
    ax1.set_xlabel('Количество туристов за год')
    ax1.set_ylabel('Маршрут: от - до')
    ax1.invert_yaxis()
    ax1.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)

    # График 2.  Выявление корреляции между объемом пассажиропотока и (разницей в зарплатах, расстоянием между городами)

    df_detailed_info_cities = load_info_cities(destination_detailed_info)
    df_info_city = load_info_cities(destination_info_city)

    df_popular_routes = add_route_features(df_popular_routes, df_info_city, df_detailed_info_cities)
    corr_matrix = df_popular_routes[['estimated_travelers_per_year', 'distance_km', 'salary_diff']].corr()
    label_map = {
        'estimated_travelers_per_year': 'Пассажиропоток',
        'distance_km': 'Расстояние (км)',
        'salary_diff': 'Разница в ЗП'
    }
    corr_matrix_readable = corr_matrix.rename(index=label_map, columns=label_map)
    ax2.imshow(corr_matrix_readable, cmap='coolwarm', vmin=-1, vmax=1)
    ax2.set_xticks(np.arange(len(corr_matrix_readable.columns)))
    ax2.set_yticks(np.arange(len(corr_matrix_readable.index)))
    ax2.set_xticklabels(corr_matrix_readable.columns)
    ax2.set_yticklabels(corr_matrix_readable.index)
    ax2.tick_params(axis='x')
    for i in range(len(corr_matrix_readable)):
        for j in range(len(corr_matrix_readable.columns)):
            ax2.text(j, i, f"{corr_matrix_readable.iloc[i, j]:.2f}",
                     ha="center", va="center", color="black")
    ax2.set_title('Корреляция: пассажиропоток, расстояние, разница в ЗП')

    # Часть 3. Анализ объема рынка на уровне города
    # График 3.  график топ 20 городов-магнитов

    outgoing_traffic = df_popular_routes.groupby(by='city_from')['estimated_travelers_per_year'].sum()
    incoming_traffic = df_popular_routes.groupby(by='city_to')['estimated_travelers_per_year'].sum()
    tourist_balance = incoming_traffic - outgoing_traffic
    top_incoming = tourist_balance.sort_values(ascending=False).head(20)
    top_outgoing = tourist_balance.sort_values(ascending=False).tail(20)
    ax3.barh(top_incoming.index, top_incoming.values, color='green')
    ax3.set_title('Топ-20 городов: туристические "магниты"')
    ax3.set_xlabel('Общее число въехавших туристов в год')
    ax3.set_ylabel('Город')
    ax3.invert_yaxis()  # чтобы самый популярный был сверху
    ax3.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)

    # График 4.
    ax4.barh(top_outgoing.index, top_outgoing.values, color='orange')
    ax4.set_title('Топ-20 городов: туристические "доноры"')
    ax4.set_xlabel('Общее число выехавших туристов в год')
    ax4.set_ylabel('Город')
    ax4.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
    plt.show()

visualize_market_analysis()
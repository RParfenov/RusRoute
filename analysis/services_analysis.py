import json
import matplotlib.pyplot as plt

def plot_average_times(json_file_path: str) -> dict:
    """
    Читает JSON-файл с данными о сервисах, вычисляет среднее время для каждого,
    строит 3 столбчатые диаграммы (среднее время, info, functional) и возвращает
    словарь со средними значениями времени.

    Args:
        json_file_path (str): Путь к файлу services.json.

    Returns:
        dict: Словарь, где ключи - названия сервисов, а значения - средние значения времени.
    """
    avg_times = {}
    info_values = {}
    functional_values = {}

    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if not isinstance(data, list):
            print("Ошибка: Ожидается, что данные в JSON-файле представляют собой список.")
            return {}

        for item in data:
            service_name = list(item.keys())[0]
            service_data = item[service_name]
            time_values = service_data.get("time", [])
            info_val = service_data.get("info", 0)
            functional_val = service_data.get("functional", 0)

            if time_values:
                avg_time = sum(time_values) / len(time_values)
                avg_times[service_name] = avg_time
            else:
                avg_times[service_name] = 0.0
                print(f"Предупреждение: У сервиса '{service_name}' отсутствуют данные в поле 'time'.")

            info_values[service_name] = info_val
            functional_values[service_name] = functional_val

    except FileNotFoundError:
        print(f"Ошибка: Файл {json_file_path} не найден.")
        return {}
    except json.JSONDecodeError:
        print(f"Ошибка: Неверный формат JSON в файле {json_file_path}.")
        return {}
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return {}

    if avg_times:
        service_names = list(avg_times.keys())
        colors = []
        for name in service_names:
            if name.lower() == "yandex":
                colors.append('red')
            elif name.lower() == "rusroute":
                colors.append('green')
            elif name.lower() == "tutu":
                colors.append('blue')
            else:
                colors.append('gray')

        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 15))

        # --- График 1: Среднее время ---
        avg_values = [avg_times[name] for name in service_names]
        ax1.bar(service_names, avg_values, color=colors)
        ax1.set_title('Среднее время выполнения запросов по сервисам')
        ax1.set_xlabel('Сервисы')
        ax1.set_ylabel('Среднее время (мин.)')
        ax1.grid(axis='y', linestyle='--', alpha=0.7)

        # --- График 2: Info ---
        info_vals = [info_values[name] for name in service_names]
        ax2.bar(service_names, info_vals, color=colors)
        ax2.set_title('Количество информации')
        ax2.set_xlabel('Сервисы')
        ax2.set_ylabel('Info (кол-во выводимых параметров)')
        ax2.grid(axis='y', linestyle='--', alpha=0.7)

        # --- График 3: Functional ---
        functional_vals = [functional_values[name] for name in service_names]
        ax3.bar(service_names, functional_vals, color=colors)
        ax3.set_title('Количество функционала')
        ax3.set_xlabel('Сервисы')
        ax3.set_ylabel('Functional (кол-во функций на сервисе)')
        ax3.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()

    return avg_times


if __name__ == "__main__":
    result = plot_average_times('services.json')
    print("Средние времена:", result)
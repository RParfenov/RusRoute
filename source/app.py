from flask import Flask, render_template, request
import translations
from web_funcional import WebFunc as Wf

trans_city = translations.CITY_TRANSLATIONS
trans_transport = translations.TRANSPORT_TYPES_TRANSLATIONS

# Указываем путь к templates и static
app = Flask(__name__,
            template_folder='../templates',
            static_folder='../static')  # <-- ВАЖНО: указываем путь к static!

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plan')
def plan():
    return render_template('plan.html')

@app.route('/route')
def show_route():
    city1 = request.args.get('city_from', 'Москва')
    city2 = request.args.get('city_to', 'Казань')
    date =  request.args.get('date', '2025-11-01')

    img1_en = trans_city[city1]['en']
    img2_en = trans_city[city2]['en']

    img1_path = f"image/{img1_en}.jpg"
    img2_path = f"image/{img2_en}.jpg"

    web_func = Wf()
    times = web_func.sorted_mass_time(city1, city2, date)
    costs = web_func.sorted_mass_cost(city1, city2)
    route_data = dict()
    for cost in costs:
        if cost[1] == times[0][1]: # ищем нужный транспорт
            transport_key = times[0][1] # получаем транспорт
            route_data['transport'] = trans_transport.get(transport_key, {}).get('ru', transport_key) # переводим
            route_data['cost'] = cost[0]
            route_data['time'] = round(times[0][0], 1) # получаем время
            break
    finish_date = web_func.calculate_finish_date(date, route_data['time'])
    return render_template('route.html', city1=city1, city2=city2, date=date,
                           img1=img1_path, img2=img2_path, route_data=route_data,
                           finish_date=finish_date)

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request
import translations

trans = translations.CITY_TRANSLATIONS

# Указываем путь к templates и static
app = Flask(__name__,
            template_folder='../templates',
            static_folder='../static')  # <-- ВАЖНО: указываем путь к static!

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/route')
def show_route():
    city1 = request.args.get('city1', 'Москва')
    city2 = request.args.get('city2', 'Казань')

    img1_en = trans[city1]['en']
    img2_en = trans[city2]['en']

    img1_path = f"image/{img1_en}.jpg"
    img2_path = f"image/{img2_en}.jpg"

    return render_template('route.html', city1=city1, city2=city2, img1=img1_path, img2=img2_path)

if __name__ == '__main__':
    app.run(debug=True)
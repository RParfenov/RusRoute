import os
import translations
import matplotlib
matplotlib.use('Agg')
from dotenv import load_dotenv
from flask import Flask, render_template, request, flash, redirect, url_for, g, session
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from web_functional import WebFunc as Wf
from db_system.config import DATABASE_URL, create_session, global_init
from db_system.models import User
from source.func_graphs import save_plot_as_png, get_plot_from_file

load_dotenv()

trans_city = translations.CITY_TRANSLATIONS
trans_transport = translations.TRANSPORT_TYPES_TRANSLATIONS

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
IMAGE_DIR = os.path.join(PROJECT_ROOT, 'db', 'images')

# Указываем путь к templates и static
app = Flask(__name__,
            template_folder='../templates',
            static_folder='../static')  # <-- ВАЖНО: указываем путь к static!
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

global_init()

@app.before_request
def before_request():
    g.db = create_session()

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'SqlAlchemyBase'):
        g.db.close()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Пожалуйста, войдите, чтобы получить доступ к этой странице.'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(user_id):
    return g.db.get(User, int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plan')
@login_required
def plan():
    return render_template('plan.html')

@app.route('/route')
@login_required
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
    cost_dict = {key: cost for cost, key in costs}

    route_dict = dict()
    for time_val, transport_key in times:
        cost_val = cost_dict[transport_key]
        transport_name = trans_transport.get(transport_key, {}).get('ru', transport_key) # получаем перевод
        finish_date = web_func.calculate_finish_date(date, time_val)
        route_dict[transport_key] = {
            'transport_key': transport_key,
            'transport_name': transport_name,
            'time': round(time_val, 1),
            'cost': cost_val,
            'finish_date': finish_date
        }

    route_images_data = web_func.get_route_image_from_db(user_is_authenticated=current_user.is_authenticated,
                                     user_id=current_user.id, city_from=city1, city_to=city2, date_start=date)
    if route_images_data is None:
        try:
            time_image_path = save_plot_as_png(to=city2, fr=city1, date=date, filter_name='time',
                                               type_name='bar', output_dir=IMAGE_DIR)
            cost_image_path = save_plot_as_png(to=city2, fr=city1, date=date, filter_name='cost',
                                               type_name='bar', output_dir=IMAGE_DIR)
            web_func.save_route_for_user(user_is_authenticated=current_user.is_authenticated,
                                         user_id=current_user.id, city_from=city1, city_to=city2, date_start=date,
                                         cost_image_path=cost_image_path, time_image_path=time_image_path)
            plot_cost = get_plot_from_file(cost_image_path)
            plot_time = get_plot_from_file(time_image_path)
        except Exception as e:
            plot_cost = plot_time = None
    else:
        cost_path = route_images_data['cost_image_path']
        time_path = route_images_data['time_image_path']
        web_func.save_route_for_user(user_is_authenticated=current_user.is_authenticated,
                                     user_id=current_user.id, city_from=city1, city_to=city2, date_start=date,
                                     cost_image_path=cost_path, time_image_path=time_path)
        plot_cost = get_plot_from_file(cost_path)
        plot_time = get_plot_from_file(time_path)

    return render_template('route.html', city1=city1, city2=city2, date=date,
                           img1=img1_path, img2=img2_path, plane_route=route_dict['plane'],
                           train_route=route_dict['train'], free_trails_route=route_dict['free_trails'],
                           toll_trails_route=route_dict['toll_trails'], plot_cost=plot_cost, plot_time=plot_time)

@app.route('/history')
@login_required
def show_history():
    history_items = Wf.get_user_route_history(current_user.id)
    return render_template('history.html', queries=history_items)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        password2 = request.form.get('password2', '')

        if not username or not email or not password or not password2:
            flash('Все поля обязательны.', 'danger')
            return render_template('register.html')

        if password != password2:
            flash('Пароли не совпадают', 'danger')
            return render_template('register.html')

        if len(password) < 6:
            flash('Пароль должен содержать не менее 6 символов.', 'danger')

        existing_user = g.db.query(User).filter((User.username == username) | (User.email == email)).first()

        if existing_user:
            flash('Пользователь с таким именем или почтой уже существует.', 'danger')
            return render_template('register.html')

        new_user = User()
        new_user.username = username
        new_user.email = email
        new_user.set_password(password)

        try:
            g.db.add(new_user)
            g.db.commit()
            flash('Регистрация прошла успешно!', 'success')
            login_user(new_user)
            flash('Вы вошли в систему!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            g.db.rollback()
            flash('Произошла ошибка при регистрации. Попробуйте позже.', 'danger')
            return render_template('register.html')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password', '')

        if not username or not password:
            flash('Пожалуйста, введите имя пользователя или пароль.', 'danger')
            return render_template('login.html')

        user = g.db.query(User).filter_by(username=username).first()

        if user is None or not user.check_password(password):
            flash('Неверное имя пользователя или пароль', 'danger')
            return render_template('login.html')

        login_user(user)
        flash('Вы успешно вошли в систему!', 'success')
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('_flashes', None)
    flash('Вы вышли из аккаунта.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Папапапаа. Папапапапа. Пык.</h1><p>Хехей! Всем привет друзья. Меня зовут Дмитрий. Это канал kuplinov ► play</p>"

if __name__ == '__main__':
    app.run(debug=True)
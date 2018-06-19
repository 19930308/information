from flask import Flask

app = Flask(__name__)
app.debug = True


@app.route('/')
def index():
    return 'good'


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def mainpage():
    return render_template('homepage.html')

@app.route('/content')
def content():
    return render_template('content.html')

if __name__ == '__main__':
    app.run()

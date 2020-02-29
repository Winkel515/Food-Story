from flask import Flask, render_template, redirect, url_for
import random

app = Flask(__name__)


@app.route('/')
def mainpage():
    return render_template('homepage.html')

@app.route('/content')
def content():
    return render_template('content.html')

@app.route('/bibimbap')
def bibimbap():
    return render_template('food/bibimbap.html')

@app.route('/pho')
def pho():
    return render_template('food/pho.html')

@app.route('/shawarma')
def shawarma():
    return render_template('food/shawarma.html')

@app.route('/sushi')
def sushi():
    return render_template('food/sushi.html')

@app.route('/surprise')
def surprise():
    links = ['bibimbap', 'pho', 'shawarma', 'sushi']
    index = random.randint(0, len(links)-1)
    return redirect(url_for(links[index]))

if __name__ == '__main__':
    app.run()

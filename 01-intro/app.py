from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# view function
# represents a html page
# single forward slash --> root url
@app.route('/')
def hello():
    return "Hello World"


@app.route('/about-our-company')
def about():
    return "About Me"


@app.route('/catalog')
def show_catalog():
    return render_template('catalog.template.html')


@app.route('/greeting/<name>')
def greet(name):
    return "Hello " + name


@app.route('/add/<n1>/<n2>')
def add(n1, n2):
    r = int(n1) + int(n2)
    return render_template('results.template.html', result=r)


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
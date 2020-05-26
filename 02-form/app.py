from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return render_template('home.template.html')


@app.route('/', methods=['POST'])
def process_form():
    username = request.form.get('username')
    password = request.form.get('password')
    return render_template('process_form.template.html',
                           username=username,
                           password=password
    )


@app.route('/calculate_bmi')
def calculate_bmi():
    return render_template('bmi.template.html')


@app.route('/calculate_bmi', methods=['POST'])
def process_calculate_bmi():
    weight = float(request.form.get('weight'))
    height = float(request.form.get('height'))
    bmi = weight / (height**2)

    return render_template('bmi_results.template.html', bmi_result=bmi)


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
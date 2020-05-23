from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('show_form.template.html')


@app.route('/', methods=['POST'])
def process_form():
    print(request.form)
    first_name = request.form.get('first-name')
    last_name = request.form.get('last-name')
    comments = request.form.get('comments')
    room_type = request.form.get('room')
    amenities = request.form.getlist('amenities')

    return render_template('results.template.html',
                           fname=first_name,
                           lname=last_name,
                           comments=comments,
                           room_type=room_type,
                           amenities=amenities)


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
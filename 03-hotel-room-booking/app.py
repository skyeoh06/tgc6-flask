from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

room_types = {
    "single-bed": "Single Bed",
    "double-bed": "Double Bed",
    "deluxe": "Deluxe Suite"
}


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

    # for checkboxes, we have to use form.request.getlist()
    amenities = request.form.getlist('amenities')

    check_in_timing = request.form.get('check-in-timing')

    return render_template('results.template.html',
                           fname=first_name,
                           lname=last_name,
                           comments=comments,
                           room_type=room_types[room_type],
                           amenities=", ".join(amenities),
                           check_in_timing=check_in_timing)


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
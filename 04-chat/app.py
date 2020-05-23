from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# messages is in the global socpe. Aother functions is to refer to it
messages = []


@app.route('/')
def index():
    return render_template('show_messages.template.html', messages=messages)


@app.route('/add_message', methods=["POST"])
def add_message():
    text = request.form.get('new-message')
    messages.append(text)
    return redirect(url_for('index'))


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
from flask import Flask, render_template, request, redirect, url_for
import os
import csv

app = Flask(__name__)


@app.route("/")
def index():
    return "home"


# create employee route
@app.route('/employee/create')
def create_employee():
    return render_template('employee/create_employee.template.html')


# process create employee form
@app.route('/employee/create', methods=["POST"])
def process_create_employee():
    print(request.form)
    with open('data.csv', 'a', newline="\n") as fp:
        writer = csv.writer(fp, delimiter=",")
        name = request.form.get('employee_name')
        job_title = request.form.get('job_title')
        salary = request.form.get('salary')
        writer.writerow([name, job_title, salary])
    return "form recieved"


@app.route('/employees')
def read_employee():
    # a state variable that represents all the employees in the system
    all_employees = [] #accumulator
    # fp = open('data.csv', 'r', newline="\n")
    with open('data.csv', 'r', newline="\n") as fp:
        reader = csv.reader(fp, delimiter=",")
        next(reader)
        for line in reader:
            all_employees.append({
                'employee_name': line[0],
                'job_title': line[1],
                'salary': line[2]
            })
    return render_template('employee/view_employees.template.html', employees=all_employees)


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
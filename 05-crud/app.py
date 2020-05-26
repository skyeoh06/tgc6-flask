from flask import Flask, render_template, request, redirect, url_for
import os
import csv
import random

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
        id = random.randint(10000, 99999)
        name = request.form.get('employee_name')
        job_title = request.form.get('job_title')
        salary = request.form.get('salary')
        writer.writerow([id, name, job_title, salary])
    return redirect(url_for('read_employee'))


@app.route('/employees')
def read_employee():
    # a state variable that represents all the employees in the system
    all_employees = read_employees_from_file()

    return render_template('employee/view_employees.template.html', employees=all_employees)


@app.route('/employee/update/<employee_id>')
def update_employee(employee_id):
    editing_employee = find_employee_by_id(employee_id)

    return render_template('employee/update_employee.template.html', employee=editing_employee)


@app.route('/employee/update/<employee_id>', methods=["POST"])
def process_update_employee(employee_id):
    # step 0. retrieve all the employees in the .csv file in a list
    all_employees = read_employees_from_file()

    # step 1. find the employee that we have changed
    changed_employee = find_employee_by_id(employee_id)

    # step 2. update the changed employee to match the form
    changed_employee['employee_name'] = request.form.get('employee_name')
    changed_employee['job_title'] = request.form.get('job_title')
    changed_employee['salary'] = request.form.get('salary')

    # step 3. overwrite the employee information in the list
    for index in range(0, len(all_employees)):
        if all_employees[index]['id'] == changed_employee['id']:
            all_employees[index] = changed_employee

    # step 4. write the entire list back to the csv file
    with open('data.csv', 'w', newline="\n") as fp:
        writer = csv.writer(fp, delimiter=",")

        # write in the header
        writer.writerow(['id', 'employee_name', 'job_title', 'salary'])

        for e in all_employees:
            writer.writerow([e['id'], e['employee_name'], e['job_title'], e['salary']])

    return redirect(url_for('read_employee'))


@app.route('/employee/confirm_delete/<employee_id>')
def confirm_to_delete_employee(employee_id):
    employee = find_employee_by_id(employee_id)
    return render_template('employee/confirm_delete.template.html', employee=employee)


@app.route('/employee/delete/<employee_id>', methods=['POST'])
def delete_employee(employee_id):

    # step 0. retrieve all the employees in the .csv file in a list
    all_employees = read_employees_from_file()

    # step 1. find the employee that we have changed
    employee_to_be_deleted = find_employee_by_id(employee_id)

    for index in range(len(all_employees)):
        if employee_to_be_deleted['id'] == all_employees[index]['id']:
            # remove the employee to be deleted from the list of all employees
            del all_employees[index]
            break

    write_to_file(all_employees)
    return redirect(url_for('read_employee'))


def find_employee_by_id(employee_id):
    employee = None
    with open('data.csv', 'r', newline="\n") as fp:
        reader = csv.reader(fp, delimiter=",")
        next(reader)  # skip the headr
        for line in reader:
            if line[0] == employee_id:
                employee = {
                    'id': line[0],
                    'employee_name': line[1],
                    'job_title': line[2],
                    'salary': line[3]
                }
                break
    return employee


def read_employees_from_file():
    all_employees = []  # accumulator
    # fp = open('data.csv', 'r', newline="\n")
    with open('data.csv', 'r', newline="\n") as fp:
        reader = csv.reader(fp, delimiter=",")
        next(reader)
        for line in reader:
            all_employees.append({
                'id': line[0],
                'employee_name': line[1],
                'job_title': line[2],
                'salary': line[3]
            })
    return all_employees


def write_to_file(all_employees):
    with open('data.csv', 'w', newline="\n") as fp:
        writer = csv.writer(fp, delimiter=",")

        # write in the header
        writer.writerow(['id', 'employee_name', 'job_title', 'salary'])

        for e in all_employees:
            writer.writerow([e['id'], e['employee_name'], e['job_title'], e['salary']])


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
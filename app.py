from flask import *
import os


import database.db_connector as db

db_connection = db.connect_to_database()

app = Flask(__name__)


@app.route('/employees' , methods = [ "GET" , "POST" ] )
def employees():

    if request.method == "GET" :

        query = "SELECT Employees.employee_id, Employees.first, Employees.last, Employees.street, Employees.city, Employees.state, Employees.phone FROM Employees;"
        some = db.execute_query(db_connection=db_connection, query=query)

        data = some.fetchall()
        return render_template( "employees.j2" , employees = data )

    elif request.method == "POST" :

        if request.form.get( "addEmployee" ) :

            employee_first , employee_last , employee_street , employee_city , employee_state , employee_phone = request.form[ "employeeFirst" ] , request.form["employeeLast" ] , request.form["employeeStreet" ] , request.form["employeeCity" ] , request.form["employeeState" ] , request.form["employeePhone" ]
            query = f"INSERT INTO Employees (first, last, street, city, state, phone) Values ( { employee_first } , { employee_last } , { employee_street } , { employee_city } , { employee_state } , { employee_phone } );"

            some = db.execute_query(db_connection=db_connection, query=query)
            data = some.fetchall()

            return redirect("/employees")

@app.route("/delete_some_employee/<int:id>" , methods = [ "GET" , "POST" ] )
def delete_some_employee( id ) :

    query = f"DELETE FROM Employees WHERE id = { id } ;"
    some = db.execute_query(db_connection=db_connection, query=query)

    return redirect("/employees")

@app.route( "/update_some_employee/<int:id>" , methods = [ "GET" , "POST" ] )
def update_some_people( id ) :

    if request.method == "GET" :

        query = f"SELECT Employees.employee_id, Employees.first, Employees.last, Employees.street, Employees.city, Employees.state, Employees.phone FROM Employees WHERE Employees.employee_id = { id } ;"
        some = db.execute_query(db_connection=db_connection, query=query)

        data = some.fetchall()
        return render_template("update_some_employee.j2", employee =data)

    elif request.method == "POST" :

        if request.form.get( "updateEmployee" ) :

            employee_first, employee_last, employee_street, employee_city, employee_state, employee_phone = request.form["employeeFirst"], request.form["employeeLast"], request.form["employeeStreet"], request.form["employeeCity"], request.form["employeeState"], request.form["employeePhone"]
            query = f"UPDATE Employees SET first = { employee_first } , last =  { employee_last } , street = { employee_street } , city = { employee_city } , state = { employee_state } , phone = { employee_phone } WHERE employee.id = { request.form[ 'id' ] } ;"

            some = db.execute_query(db_connection=db_connection, query=query)
            data = some.fetchall()

            return redirect("/employees")

if __name__ == "__main__":

    port = int(os.environ.get('PORT', 9112))

    app.run(port=port, debug=True)
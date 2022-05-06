from flask import Flask, render_template, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = "Content-Type"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'clientes'
mysql = MySQL(app)



@app.route("/api/customer", methods=["POST"])
@cross_origin()
def save_and_modify():
    if "id" in request.json:
        modify_customer()
    else:
        save_customer()
    return "ok"


#@app.route("/api/customer", methods=["POST"])
def save_customer():
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO `clientes2` (`id`, `firstname`, `lastname`, `phone`, `email`) VALUES (NULL, %s, %s, %s, %s);",
                (request.json['firstname'], request.json['lastname'], request.json['phone'], request.json['email']))
    mysql.connection.commit()
    return "cliente guardado"


#@app.route("/customer", methods=["PUT"])
def modify_customer():
    cur = mysql.connection.cursor()
    cur.execute("UPDATE `clientes2` SET `firstname` = %s, `lastname` = %s, `phone` = %s, `email` = %s WHERE `clientes2`.`id` = %s;",
                (request.json['firstname'], request.json['lastname'], request.json['phone'], request.json['email'], request.json['id']))
    mysql.connection.commit()
    return "Cliente modificado"



@app.route("/api/customer/<int:id>", methods=["DELETE"])
@cross_origin()
def remove_customer(id):
    cur = mysql.connection.cursor()
    cur.execute(
        "DELETE FROM `clientes2` WHERE `clientes2`.`id` = " + str(id) + ";")
    mysql.connection.commit()
    return "cliente eliminado"


@app.route("/api/customer/<int:id>")
@cross_origin()
def get_customer(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT id, firstname, lastname, phone, email FROM clientes2 WHERE id = ' + str(id))
    data = cur.fetchall()
    content = {}
    for row in data:
        content = {"id": row[0], "firstname": row[1], "lastname": row[2], "phone": row[3], "email": row[4]}
    return content


@app.route("/api/customer")
@cross_origin()
def get_all_customer():
    cur = mysql.connection.cursor()
    cur.execute('SELECT id, firstname, lastname, phone, email FROM clientes2')
    data = cur.fetchall()
    result = []
    for row in data:
        content = {"id": row[0], "firstname": row[1], "lastname": row[2], "phone": row[3], "email": row[4]}
        result.append(content)
    return jsonify(result)


@app.route("/")
@cross_origin()
def index():
    return render_template('index.html')

@app.route("/<path:path>")
@cross_origin()
def public_files(path):
    return render_template(path)


if __name__ == "__main__":
    app.run(None, 3000, True)

from flask import Flask, render_template, url_for, request, make_response, redirect, flash
from flask_mysqldb import MySQL
import os
from werkzeug.security import check_password_hash, generate_password_hash
from dotenv import load_dotenv
import time


load_dotenv()

app = Flask(__name__)


app.config["MYSQL_USER"] = os.getenv("user")
app.config["MYSQL_PASSWORD"] = os.getenv("password")
app.config["MYSQL_HOST"] = os.getenv("host")
app.config["MYSQL_DB"] = os.getenv("db")
app.secret_key = os.getenv("secret_key")

mysql = MySQL(app)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        cursor = mysql.connection.cursor()
        email = request.form.get("email")
        password = request.form.get("password")
        cursor.execute("SELECT * from users where email = (%s)",(email,))
        user = cursor.fetchone()
        print(user)
        # print(user[2])
        if user:
            verifpassword = check_password_hash(user[2], password)
            if verifpassword:
                return redirect(url_for("appointments"))
        flash("Credenciales Invalidas")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        cursor = mysql.connection.cursor()
        email = request.form.get("email")
        password = request.form.get("password")
        phone = request.form.get("phone")
        print(email, password, phone)
        
        cursor.execute("INSERT INTO users VALUES (NULL, %s, %s, %s)",(email, generate_password_hash(password), phone))
        mysql.connection.commit()
        if cursor: 
            flash("Usuario registrado ve al login")
            return redirect(url_for("login"))
        
    
    return render_template("register.html")


@app.route("/appointments", methods=["GET", "POST"])
def appointments():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM doctor")
    doctores = cursor.fetchall()
    print(doctores)
    
    cursor.execute("""
    """)

    return render_template("appointments.html", doctores= doctores)


############################ RUTAS PARA GESTION CITAS ###########################33

@app.route("/add/<string:id>", methods=["GET", "POST"])
def add(id):
    cursor = mysql.connection.cursor()
    cita = cursor.execute("INSERT INTO appoinment VALUEs (NULL, %s, %s)",(6, id))
    mysql.connection.commit()
    print(cita)
    return "ruta add"

@app.route("/delete/<string:id>")
def delete(id):
    return "ruta delete"


@app.route("/complete/<string:id>")
def complete(id):
    return "ruta complete"




if __name__ == "__main__":
    app.run(debug=True, port=3030, host="localhost")
from flask import Flask, render_template, url_for, request, make_response, redirect, flash, jsonify
from flask_mysqldb import MySQL
import os
from werkzeug.security import check_password_hash, generate_password_hash
from dotenv import load_dotenv
import jwt
from datetime import datetime, timedelta
import logging

load_dotenv()

# Configuración del logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuración de la base de datos
app.config["MYSQL_USER"] = os.getenv("user")
app.config["MYSQL_PASSWORD"] = os.getenv("password")
app.config["MYSQL_HOST"] = os.getenv("host")
app.config["MYSQL_DB"] = os.getenv("db")
app.secret_key = os.getenv("secret_key")

mysql = MySQL(app)

def get_user_id_from_token():
    token = request.cookies.get("token")
    if not token:
        logger.warning("No token found in request cookies")
        return None
    try:
        data = jwt.decode(token, app.secret_key, algorithms=["HS256"])
        return data["user_id"]
    except Exception as e:
        logger.error(f"Error decoding token: {e}")
        return None

@app.route("/")
def home():
    logger.info("Accessing the home page")
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        cursor = mysql.connection.cursor()
        email = request.form.get("email")
        password = request.form.get("password")
        cursor.execute("SELECT * from users where email = (%s)", (email,))
        user = cursor.fetchone()
        if user:
            verifpassword = check_password_hash(user[2], password)
            if verifpassword:
                # Generar el token JWT
                token = jwt.encode({
                    "user_id": user[0],
                    "exp": datetime.utcnow() + timedelta(hours=1)
                }, app.secret_key, algorithm="HS256")
                resp = make_response(redirect(url_for("appointments")))
                resp.set_cookie("token", token, httponly=True)
                logger.info(f"User {user[0]} logged in successfully")
                return resp

        flash("Credenciales Invalidas")
        logger.warning(f"Failed login attempt for email: {email}")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        cursor = mysql.connection.cursor()
        email = request.form.get("email")
        password = request.form.get("password")
        phone = request.form.get("phone")
        
        cursor.execute("INSERT INTO users (email, password, phone) VALUES (%s, %s, %s)", 
                       (email, generate_password_hash(password), phone))
        mysql.connection.commit()
        flash("Usuario registrado, ve al login")
        logger.info(f"User {email} registered successfully")
        return redirect(url_for("login"))
    
    return render_template("register.html")

@app.route("/appointments", methods=["GET", "POST"])
def appointments():
    user_id = get_user_id_from_token()
    if not user_id:
        logger.warning("User is not authenticated")
        return jsonify({"message": "Usuario no autenticado"}), 401

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM doctor")
    doctores = cursor.fetchall()

    cursor.execute("""
        SELECT a.id, u.email, d.nombre, d.especialidad, a.estado
        FROM appoinment a
        JOIN users u ON a.user_id = u.id
        JOIN doctor d ON a.doctor_id = d.id
        WHERE a.user_id = %s
    """, (user_id,))
    citas = cursor.fetchall()

    logger.info(f"User {user_id} fetched appointments")
    return render_template("appointments.html", doctores=doctores, citas=citas)

@app.route("/add/<string:id>", methods=["GET", "POST"])
def add(id):
    user_id = get_user_id_from_token()
    if not user_id:
        logger.warning(f"User not authenticated for adding appointment")
        return jsonify({"message": "Usuario no autenticado"}), 401

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO appoinment (user_id, doctor_id, estado) VALUES (%s, %s, 'pendiente')", 
                   (user_id, id))
    mysql.connection.commit()
    logger.info(f"Appointment added for user {user_id} with doctor {id}")
    return redirect(url_for("appointments"))

@app.route("/delete/<string:id>")
def delete(id):
    user_id = get_user_id_from_token()
    if not user_id:
        logger.warning(f"User not authenticated for deleting appointment")
        return jsonify({"message": "Usuario no autenticado"}), 401

    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM appoinment WHERE id = (%s) AND user_id = (%s)", (id, user_id))
    mysql.connection.commit()
    logger.info(f"Appointment {id} deleted for user {user_id}")
    return redirect(url_for("appointments"))

@app.route("/complete/<string:id>")
def complete(id):
    user_id = get_user_id_from_token()
    if not user_id:
        logger.warning(f"User not authenticated for completing appointment")
        return jsonify({"message": "Usuario no autenticado"}), 401

    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE appoinment SET estado = 'completada' WHERE id = %s AND user_id = %s", 
                   (id, user_id))
    mysql.connection.commit()
    logger.info(f"Appointment {id} completed for user {user_id}")
    return redirect(url_for("appointments"))

if __name__ == "__main__":
    app.run(debug=True, port=3030, host="localhost")

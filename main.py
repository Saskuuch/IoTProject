from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_cors import CORS
import folium
from flask_bcrypt import Bcrypt
import flask_login as ln
from flask_sqlalchemy import SQLAlchemy
import datetime
import database.model as md
import random

app = Flask(__name__)
CORS (app)

app.config['SECRET_KEY'] = 'test'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://iot_user:iot_pass@localhost/iot_project'
bcrypt = Bcrypt(app)
loginManager = ln.LoginManager(app)
loginManager.login_view = 'login'
db = SQLAlchemy(app)

class User(ln.UserMixin, db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

def map_create():
    lat = 50.676109
    lon = -120.340836
    zoom = 11

    # dfAreas = getAreas()

    map = folium.Map(location=[lat, lon],
                     zoom_start=zoom, control_scale=True)
    folium.Marker(
        [50.667, -120.367],
        popup=folium.Popup("<div style='width:900px;height:500px; background-color:white'><iframe id='popup' width='100%' height='100%' src='/dashboard'></iframe></div>", max_width=900),
        tooltip="TRU",
    ).add_to(map)

    map.get_root().width = "100%"
    map.get_root().height = "700px"

    return map

#--------------Authentication Routes--------------#
@loginManager.user_loader
def loadUser(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get('user')
        password = request.form.get('password')
        print(username + password)
        user = User.query.filter_by(username=username).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            ln.login_user(user)
            return redirect(url_for("homepage"))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('psd1')
        password2 = request.form.get('psd2')
        
        if password1 == password2:
            hashed_password = bcrypt.generate_password_hash(password1).decode('utf-8')
            user = User(username=username, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            # If passwords don't match, redirect to 'openRegister' with an error message
            return redirect(url_for('openRegister', error="Passwords do not match."))
    return render_template('register.html')
    
@app.route('/openRegister', methods = ['GET', 'POST'])
def openRegister():
    return render_template("register.html")

@app.route('/registerPage', methods = ['GET', 'POST'])
def openRegistration():
    return redirect(url_for('openRegister'))


#--------------Page Routes--------------#
@app.route("/")
@ln.login_required
def initialLanding():
    map = map_create()
    html = map._repr_html_()
    return render_template("testhome.html", map_html = html)

@app.route("/homepage")
def homepage():
    map = map_create()
    html = map._repr_html_()
    return render_template("testhome.html", map_html = html)

@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    return render_template("dashboard.html")


#--------------Data Retrival Routes--------------#
@app.route("/getChartData", methods=["GET", 'POST'])
def getChartData():
    databaseOut = md.get_gasses_over_time([4, 10, 1, 3], 1, 60)
    averages = {"carbon": [], "methane": [], "airq": [], "butane": [], "timestamps": []}

    for item in databaseOut:
        if (item[4]%10 == 0):
            averages['carbon'].append(item[0])
            averages['methane'].append(item[1])
            averages['airq'].append(item[2])
            averages['butane'].append(item[3])
            averages['timestamps'].append((datetime.datetime.now() - datetime.timedelta(minutes=item[4])).strftime("%H:%M"))

    data = {
        "carbon": {"timestamp": averages['timestamps'], "value": averages['carbon']},
        "methane": {"timestamp": averages['timestamps'], "value":  averages['methane']},
        "airq": {"timestamp": averages['timestamps'], "value": averages['airq']},
        "butane": {"timestamp": averages['timestamps'], "value": averages['butane']}
    }

    return jsonify (data)

@app.route("/getChartData_24", methods=["GET", 'POST'])
def getChartData_24():
    databaseOut = md.get_gasses_over_time([4, 10, 1, 3], 2, 24)
    averages = {"carbon": [], "methane": [], "airq": [], "butane": [], "timestamps": []}

    for item in databaseOut:
        if (item[4]%2 == 0):
            averages['carbon'].append(item[0])
            averages['methane'].append(item[1])
            averages['airq'].append(item[2])
            averages['butane'].append(item[3])
            averages['timestamps'].append((datetime.datetime.now() - datetime.timedelta(minutes=item[4])).strftime("%H:%M"))

    data = {
        "carbon": {"timestamp": averages['timestamps'], "value": averages['carbon']},
        "methane": {"timestamp": averages['timestamps'], "value":  averages['methane']},
        "airq": {"timestamp": averages['timestamps'], "value": averages['airq']},
        "butane": {"timestamp": averages['timestamps'], "value": averages['butane']}
    }
    return jsonify (data)

@app.route("/getGaugeData", methods=["POST"])
def getGaugeData():
    #get data from database
    data = [random.randint(0, 10000), random.randint(0, 1000), random.randint(0, 1000), random.randint(0, 1600)]
    return data

#--------------Data Insert Routes--------------#
@app.route("/addGasses")
def addGasses():
    data = request.json
    latitute = data['latitude']
    longitutde = data['longitude']

    gasLevels = {4:data['carbonmonoxide'], 10:data['methane'], 1:data['airquality'], 3: data['butane']}
    md.insert_gasses(gasLevels)

@app.route("/updateDangerLevel")
def updateDangerLevel():
    gas = request.args.get("gas")
    level = request.args.get("level")
    md.setDangerLevel(gas, level)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2300)
from flask import Flask, flash, render_template, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = "cualquiercosa"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost/segundo_unificado"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import City, Climate

@app.route('/')
def index():
    return render_template(
        'index.html'
    )

app.route('/city', methods=['POST', 'GET'])
def city():
    if request.method == "POST":
        name = request.form["name"]
        latitude = request.form["lat"]
        longitude = request.form["long"]

        new_city = City(name=name, lat=latitude, long= longitude)
        db.session.add(new_city)
        db.session.commit()
        flash("City added succefuly", "success")

    cities_list = City.query.all()
    return render_template(
        'city.html',
        cities=cities_list
    )

if __name__ == '__main__':
    app.run(debug=True)
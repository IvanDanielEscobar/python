from flask import Flask, render_template, request
import requests

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = ( 
    'mysql+pymysql://iescobar:489796.Mapa96@localhost/segundocomisionb'
)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import City


# diccionario de ciudades
ciudades = {
    "buenos_aires": {"lat": -34.6037, "lon": -58.3816},
    "cordoba": {"lat": -31.4201, "lon": -64.1888},
    "madrid": {"lat": 40.4168, "lon": -3.7038},
    "nueva_york": {"lat": 40.7128, "lon": -74.0060},
    "tokio": {"lat": 35.6895, "lon": 139.6917},
    "paris": {"lat": 48.8566, "lon": 2.3522},
    "londres": {"lat": 51.5074, "lon": -0.1278},
    "sidney": {"lat": -33.8688, "lon": 151.2093},
    "mexico": {"lat": 19.4326, "lon": -99.1332},
    "el_cairo": {"lat": 30.0444, "lon": 31.2357}
}



@app.route('/', methods=['GET'])
def inicio():
    return render_template(
        'index.html', ciudades=ciudades.keys()
        )   # para que se muestren los enlaces a cada ciudad

@app.route('/clima', methods=['GET'])
def mostrar_clima():
    # obtener el nombre de ciudad, request.args es un diccionario con los parametros y .get obtiene el valor 'ciudad'
    ciudad_nombre = request.args.get('ciudad')
    # buscar la cidad en el diccionario para obtener lat y lon
    if (
        ciudad_nombre and ciudad_nombre in ciudades
        ):  # verificacion si el nombre de la ciudad existe en nuestro diccionario
        coordenadas = ciudades[ciudad_nombre]
        lat = coordenadas['lat']
        lon = coordenadas['lon']
        api_url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&timezone=auto' # f-string para insertar lat y lon
        # pido a la api usando requests
    
        try:
            response = requests.get(api_url)    # hace la peticion a open-meteo
            response.raise_for_status()     # detecta de errores si la respuesta es 4xx o 5xx
            datos_clima = response.json()
            if 'current_weather' in datos_clima:
                clima_actual = datos_clima['current_weather']
                fecha = clima_actual['time'] 
                temperatura = clima_actual['temperature']
                viento = clima_actual['windspeed']
                direccion_viento = clima_actual['winddirection']
                dia_noche = clima_actual['is_day']
                clima = clima_actual['weathercode']
                
                if 'current_weather_units' in datos_clima:
                    unidad_actual = datos_clima['current_weather_units']
                    unidad_temp = unidad_actual['temperature']
                    unidad_viento = unidad_actual['windspeed']
                    unidad_dv = unidad_actual['winddirection']
                    unidad_clima = unidad_actual['weathercode']


                datos_mostrar = {
                    'ciudad': ciudad_nombre,    # nombre de la ciudad
                    'fecha': f"{fecha}", # fecha de la ciudad
                    'temperatura': f"{temperatura} {unidad_temp}", # temperatura de la ciudad
                    'velocidad_viento': f"{viento} {unidad_viento}", # velocidad del viento
                    'direccion_viento': f"{direccion_viento} {unidad_dv}", # direccion del viento
                    'dia_noche': f"{dia_noche}", # dia o noche
                    'clima': f"{clima}, {unidad_clima}" # como esta el dia

                }
                return render_template('clima.html', **datos_mostrar)
            else:    
                # si al api no me da 'current_weather' entonces muestro la pagina pero con un error
                return render_template(
                    'clima.html', error='no se puede obtener el clima'
                    )

        except requests.exceptions.RequestsException:
            return render_template('clima.html', error='error al conectarse con la api')
        
    else:
        return render_template('clima.html', error='ciudad no encontrada')
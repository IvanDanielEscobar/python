from flask import Flask, request
from models import (
   db,
   User,
   Movie,
)
from marshmallow import ValidationError
from schemas import UserSchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (
   'mysql+pymysql://BD2021:BD2021itec@143.198.156.171:3306/movies_pp1'
)
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False
db.init_app(app)


@app.route('/users', methods=['GET', 'POST'])
def users():
   if request.method == "POST":
      try: 
          data = UserSchema().load(request.json)     
      except ValidationError as error:
          return {"Mensaje:" f"algo esta mal {error}"}
      new_user = User(name=data.get('name'), email=data.get('email'))
      db.session.add(new_user)
      db.session.commit()
      return UserSchema().dump(new_user)
   users = User.query.all()
   return UserSchema(many=True).dump(users)

@app.route('/users/<int:id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def user(id):
    user = User.query.get_or_404(id)

    if request.method == 'PUT':
         try:
            data = UserSchema().load(request.json)
            user.email = data['email']
            user.name = data['name']
            db.session.commit()

         except ValidationError as error:
            return {"Mensaje:": error.messages}
    
    if request.method == 'PATCH':
         try:
            data = UserSchema(partial=True).load(request.json)
            if 'email' in data:
               user.email = data['email']
            if 'name' in data:
               user.name = data['name']
            db.session.commit()
            
         except ValidationError as error:
            return {"Mensaje:": error.messages}
         
        
    if request.method == "DELETE":
        db.session.delete(user)
        db.session.commit()
        return {"Message": "Deleted user"}, 204
    
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email
    }, 200


@app.route('/users_from_ma', methods=['GET'])
def users_from_ma():
    users = User.query.all()
    return UserSchema(many=True).dump(users), 200

@app.route('/movies')
def movies():
   movies = Movie.query.all()
   return[
      {
         "title": movie.title,
         "year": movie.year,
         #"genres": movie.genres.id
      }
      for movie in movies
   ]
   

@app.route('/movies/<int:id>')
def movie(id):
   movie = Movie.query.get_or_404(id)
   return[
      { 
         "id": movie.id,
         "title": movie.title,
         "year": movie.year,
         #"genres": movie.genres.id
      }
   ]
   

if __name__ == '__main__':
   app.run(debug=True)


# This is where we imported the various packages used in the application 
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

# This is the initial figuatration for flask and the database 
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# This is setting up the model representing the table in the database 
class GameModel(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	users = db.Column(db.Integer, nullable=False)
	likes = db.Column(db.Integer, nullable=False)

	def __repr__(self):
		return f"Games(name = {name}, views = {users}, likes = {likes})"

# Setting up the fields needed for the put API call 
game_put_args = reqparse.RequestParser()
game_put_args.add_argument("name", type=str, help="Name of the game is required", required=True)
game_put_args.add_argument("users", type=int, help="Total number of users", required=True)
game_put_args.add_argument("likes", type=int, help="Likes on the game", required=True)

# Setting up the fields for the updated API call 
game_update_args = reqparse.RequestParser()
game_update_args.add_argument("name", type=str, help="Name of the game is required")
game_update_args.add_argument("users", type=int, help="Number of users ")
game_update_args.add_argument("likes", type=int, help="Number of likes")


resource_fields = {
	'id': fields.Integer,
	'name': fields.String,
	'users': fields.Integer,
	'likes': fields.Integer
}

class Game(Resource):
# This is where the get method is for the API call 
	@marshal_with(resource_fields)
	def get(self, game_id):
		result = GameModel.query.filter_by(id=game_id).first()
		if not result:
			abort(404, message="Could not find game with that id")
		return result

	@marshal_with(resource_fields)
	def put(self, game_id):
		args = game_put_args.parse_args()
		# Checking to ensure that id is not taken 
		result = GameModel.query.filter_by(id=game_id).first()
		if result:
			abort(409, message="Game id taken...")
		# Create the database entry 
		game = GameModel(id=game_id, name=args['name'], views=args['users'], likes=args['likes'])
		# Commit to the database 
		db.session.add(game)
		db.session.commit()
		return game, 201

	@marshal_with(resource_fields)
	def patch(self, game_id):
		args = game_update_args.parse_args()
		# Checking to ensure that game is in the database 
		result = GameModel.query.filter_by(id=game_id).first()
		if not result:
			abort(404, message="Game doesn't exist, cannot update")

		if args['name']:
			result.name = args['name']
		if args['users']:
			result.views = args['users']
		if args['likes']:
			result.likes = args['likes']

		db.session.add(result)
		db.session.commit()

		return result


	def delete(self, game_id):
		abort_if_game_id_doesnt_exist(game_id)
		del game[game_id]
		return '', 204

# Getting the game id 
api.add_resource(Game, "/game/<int:game_id>")

# Basic main method stuff 
if __name__ == "__main__":
	app.run(debug=True)
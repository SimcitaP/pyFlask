from flask import Flask, url_for
from config import SECRET_KEY
from models.user_model import init_user_file
from routes.auth_routes import auth_bp
from routes.home_routes import home_bp
from routes.mineral_routes import minerals_bp
from routes.stats_routes import stats_bp
from routes.map_routes import map_bp

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Initialize CSV file
init_user_file()

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(home_bp)
app.register_blueprint(minerals_bp, url_prefix="/minerals")
app.register_blueprint(stats_bp, url_prefix="/stats")
app.register_blueprint(map_bp, url_prefix="/map")



if __name__ == "__main__":
    app.run(debug=True)

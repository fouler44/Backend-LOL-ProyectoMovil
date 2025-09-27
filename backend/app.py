from flask import Flask
import os
from dotenv import load_dotenv

from routes.base import base_routes
#from routes.players import player_routes
#from routes.stats import stat_routes
#from routes.users import user_routes

load_dotenv()
def create_app():
  app = Flask(__name__)
  #init_db(app)
  app.register_blueprint(base_routes, url_prefix="/")
  #app.register_blueprint(player_routes, url_prefix="/players")
  #app.register_blueprint(stat_routes, url_prefix="/stats")
  #app.register_blueprint(user_routes, url_prefix="/users")
  return app

app = create_app()

if __name__ == "__main__":
  port = int(os.getenv("PORT", 8080))
  print(f"App running on port {port}")
  app.run(host="0.0.0.0",port=port,debug=True)
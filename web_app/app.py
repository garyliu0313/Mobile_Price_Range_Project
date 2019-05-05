from flask import Flask
from web_app.views.index import bp as index_bp
from web_app.views.predict_price import bp as price_bp
app = Flask(__name__)
app.register_blueprint(index_bp)
app.register_blueprint(price_bp)

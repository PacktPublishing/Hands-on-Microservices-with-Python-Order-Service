from flask import Flask
from order_api import order_api_blueprint
from flask_swagger_ui import get_swaggerui_blueprint
import models

app = Flask(__name__)

app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key",
    SQLALCHEMY_DATABASE_URI='mysql+mysqlconnector://root:test@order_db/order',
))

models.init_app(app)
models.create_tables(app)

app.register_blueprint(order_api_blueprint)
SWAGGER_URL = '/api/docs'
API_URL = '/api/order/docs.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

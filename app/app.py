from flask import Flask
from flask_bootstrap import Bootstrap
from order_api import order_api_blueprint
import models

app = Flask(__name__)

bootstrap = Bootstrap(app)

app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key",
    SQLALCHEMY_DATABASE_URI='mysql+mysqlconnector://root:test@order_db/order',
))

models.init_app(app)
models.create_tables(app)

app.register_blueprint(order_api_blueprint)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

from flask import jsonify,json, request, make_response
from . import order_api_blueprint
from models import db, Order, OrderItem
from .api.UserClient import UserClient


@order_api_blueprint.route("/api/order/docs.json", methods=['GET'])
def swagger_api_docs_yml():
    with open('swagger.json') as fd:
        json_data = json.load(fd)

    return jsonify(json_data)


@order_api_blueprint.route('/api/orders', methods=['GET'])
def orders():

    items = []
    for row in Order.query.all():
        items.append(row.to_json())

    response = jsonify(items)

    return response


@order_api_blueprint.route('/api/order/add-item', methods=['POST'])
def order_add_item():

    api_key = request.headers.get('Authorization')
    response = UserClient.get_user(api_key)

    if not response:
        return make_response(jsonify({'message': 'Not logged in'}), 401)

    user = response['result']

    p_id = int(request.form['product_id'])
    qty = int(request.form['qty'])
    u_id = int(user['id'])

    # Find open order
    known_order = Order.query.filter_by(user_id=u_id, is_open=1).first()

    if known_order is None:
        # Create the order
        known_order = Order()
        known_order.is_open = True
        known_order.user_id = u_id

        order_item = OrderItem(p_id, qty)
        known_order.items.append(order_item)

    else:
        found = False
        # Check if we already have an order item with that product
        for item in known_order.items:

            if item.product_id == p_id:
                found = True
                item.quantity += qty

        if found is False:
            order_item = OrderItem(p_id, qty)
            known_order.items.append(order_item)

    db.session.add(known_order)
    db.session.commit()

    response = jsonify({'result': known_order.to_json()})

    return response


@order_api_blueprint.route('/api/order', methods=['GET'])
def order():
    api_key = request.headers.get('Authorization')
    response = UserClient.get_user(api_key)

    if not response:
        return make_response(jsonify({'message': 'Not logged in'}), 401)

    user = response['result']

    open_order = Order.query.filter_by(user_id=user['id'], is_open=1).first()

    if open_order is None:
        response = jsonify({'message': 'No order found'})
    else:
        response = jsonify({'result': open_order.to_json()})

    return response


@order_api_blueprint.route('/api/order/checkout', methods=['POST'])
def checkout():
    api_key = request.headers.get('Authorization')
    response = UserClient.get_user(api_key)

    if not response:
        return make_response(jsonify({'message': 'Not logged in'}), 401)

    user = response['result']

    order_model = Order.query.filter_by(user_id=user['id'], is_open=1).first()
    order_model.is_open = 0

    db.session.add(order_model)
    db.session.commit()

    response = jsonify({'result': order_model.to_json()})

    return response

from flask import Blueprint, jsonify, request
from utils.res_wrapper import success_response, error_response
from controllers.api.users.UserController import profile_user, available_city, your_order, transactions_history, login_proccess, logout_proccess, resto_registration_proccess, user_registration_proccess, transaction, order_history, order, edit_profile_user, update_transaction_status_controller, invoice, payment_qris
from controllers.api.users.FoodWasteController import food_waste_filter, all_food_waste, food_waste_resto_filter, one_food_waste, add_food_waste, update_food_waste, delete_food_waste

food_waste_api = Blueprint("food_waste_api", __name__)

@food_waste_api.route('/api/food-waste/<int:user_id>')
def get_food(user_id):
    return all_food_waste(user_id)

@food_waste_api.route('/api/profile/<int:id>', methods=['GET'])
def get_profile(id):
    return profile_user(id)

@food_waste_api.route('/api/profile/edit/<int:id>', methods=['PUT'])
def put_profile(id):
    return edit_profile_user(id)

@food_waste_api.route('/api/food-waste/filter', methods=['GET'])
def get_food_waste_filter():
    city = request.args.get("city")
    type = request.args.get("type")
    return food_waste_filter(city, type)

@food_waste_api.route('/api/food-waste-resto/filter/<int:user_id>/<string:type>', methods=['GET'])
def get_food_waste_resto_filter(user_id, type):
    return food_waste_resto_filter(user_id, type)

@food_waste_api.route('/api/food-waste/one/<int:id>', methods=['GET'])
def get_one_food_waste(id):
    return one_food_waste(id)

@food_waste_api.route('/api/food-waste/add', methods=['POST'])
def insert_food_waste():
    return add_food_waste()

@food_waste_api.route('/api/food-waste/update/<int:id>', methods=['PUT'])
def put_update_food_waste(id):
    return update_food_waste(id)

@food_waste_api.route('/api/food-waste/delete/<int:id>', methods=['DELETE'])
def del_food_waste(id):
    return delete_food_waste(id)

@food_waste_api.route('/api/available-city', methods=['GET'])
def get_available_city():
    return available_city()

@food_waste_api.route('/api/your-order/<int:id>', methods=['GET'])
def get_your_order(id):
    return your_order(id)

@food_waste_api.route('/api/transactions-history/<int:id>', methods=['GET'])
def get_transactions_history(id):
    return transactions_history(id)

@food_waste_api.route('/api/order/<int:resto_id>', methods=['GET'])
def get_order(resto_id):
    return order(resto_id)

@food_waste_api.route('/api/order-history/<int:resto_id>', methods=['GET'])
def get_order_history(resto_id):
    return order_history(resto_id)

@food_waste_api.route('/api/login', methods=['POST'])
def login():
    return login_proccess()

@food_waste_api.route('/api/logout', methods=['POST'])
def logout():
    return logout_proccess()

@food_waste_api.route('/api/registration-resto', methods=['POST'])
def registration_resto():
    return resto_registration_proccess()

@food_waste_api.route('/api/registration-user', methods=['POST'])
def registration_user():
    return user_registration_proccess()

@food_waste_api.route('/api/transaction', methods=['POST'])
def insert_transaction():
    return transaction()

@food_waste_api.route('/api/invoice/<int:transaction_id>', methods=['GET'])
def get_invoice(transaction_id):
    return invoice(transaction_id)

@food_waste_api.route('/api/invoice/put-qris/<int:transaction_id>', methods=['PUT'])
def put_payment_qris(transaction_id):
    return payment_qris(transaction_id)

@food_waste_api.route('/api/transaction-update/<int:id>', methods=['PUT'])
def update_transaction_status(id):
    return update_transaction_status_controller(id)
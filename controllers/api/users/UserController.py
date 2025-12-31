from flask import Blueprint, jsonify, request
import os
from flask import Flask, session, redirect, url_for
from datetime import datetime, timedelta
from uuid import uuid4
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from utils.res_wrapper import success_response, error_response
from models.user import get_profile, get_available_city, get_your_order, get_transactions_history, login, resto_registration, user_registration, insert_transaction, get_order_history, get_order, put_profile, update_transaction_status, get_invoice, put_payment_qris
from werkzeug.security import check_password_hash, generate_password_hash

def profile_user(id):
    try:
        profile = get_profile(id)

        if not profile:
            return error_response("Data tidak tersediaaaaa", res_code=404)
        else:
            return success_response(data=profile)
    except Exception as e:
        print(e)
        return error_response(message="Internal server error", res_code=500)
    
def clean(value):
    return value if value not in ['', None] else None
    
def edit_profile_user(id):
    data = {
        "name": clean(request.form.get('name')),
        "phone": clean(request.form.get('phone')),
        "email": clean(request.form.get('email')),
        "address": clean(request.form.get('address')),
        "longitude": clean(request.form.get('longitude')),
        "latitude": clean(request.form.get('latitude')),
        "city": clean(request.form.get('city')),
        "open_time": clean(request.form.get('open_time')),
        "closed_time": clean(request.form.get('closed_time'))
    }

    password = request.form.get('password')
    if password:
        data['password'] = generate_password_hash(password)

    UPLOAD_FOLDER = 'static/uploads/users'
    foto_path = None

    foto = request.files.get('foto')
    if foto:
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        ext = foto.filename.rsplit('.', 1)[-1]
        filename = f"{uuid4().hex}.{ext}"
        filename = secure_filename(filename)
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        foto.save(save_path)

        foto_path = f"uploads/users/{filename}"
        data['foto'] = foto_path

    try:
        user = put_profile(id, data)
        
        if not user:
            return error_response("Data gagal updateeeeee", res_code=404)
        
        session['name'] = data['name']
        return success_response(data=user)
    except Exception as e:
        print(e)
        return error_response(message="Internal server error", res_code=500)

def available_city():
    try:
        citys = get_available_city()

        if not citys:
            return error_response("Data tidak tersediaaaaa", res_code=404)
        else:
            return success_response(data=citys)
    except Exception as e:
        print(e)
        return error_response(message="Internal server error", res_code=500)
    
def your_order(id):
    try:
        your_order = get_your_order(id)

        if not your_order:
            return error_response("Data tidak tersediaaaaa", res_code=404)
        else:
            return success_response(data=your_order)
    except Exception as e:
        print(e)
        return error_response(message="Internal server error", res_code=500)

def transactions_history(id):
    try:
        transactions_history = get_transactions_history(id)

        if not transactions_history:
            return error_response("Data tidak tersediaaaaa", res_code=404)
        else:
            return success_response(data=transactions_history)
    except Exception as e:
        print(e)
        return error_response(message="Internal server error", res_code=500)
    
def order(resto_id):
    try:
        order = get_order(resto_id)

        if not order:
            return error_response("Data tidak tersediaaaaa", res_code=404)
        else:
            return success_response(data=order)
    except Exception as e:
        print(e)
        return error_response(message="Internal server error", res_code=500)

def order_history(resto_id):
    try:
        order_history = get_order_history(resto_id)

        if not order_history:
            return error_response("Data tidak tersediaaaaa", res_code=404)
        else:
            return success_response(data=order_history)
    except Exception as e:
        print(e)
        return error_response(message="Internal server error", res_code=500)

    
def login_proccess():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return error_response("Email dan Password wajib diisi", 400)
    
    user = login(email)
    if not user:
        return error_response("User tidak ada", 404)
    
    if not check_password_hash(user['password'], password):
        return error_response("Password salah", 401)
    
    session['user_id'] = user['id']
    session['role'] = user['role']
    session['name'] = user['name']
    return success_response("Login berhasil", data=user, res_code=200)

def logout_proccess():
    session.clear()
    return success_response("Logout berhasil", res_code=200)

def resto_registration_proccess():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    city = data.get('city')
    address = data.get('address')
    role = "resto"

    if not email or not password or not name or not city or not address:
        return error_response("Wajib mengisi semua data", res_code=400)
    
    hashed_password = generate_password_hash(password)
    user = resto_registration(email, hashed_password, name, city, address, role)
    
    if not user:
        return error_response("Gagal daftar", res_code=404)
    
    return success_response("Daftar berhasil", data=user, res_code=200)

def user_registration_proccess():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return error_response("Wajib mengisi semua data", res_code=400)
    
    hashed_password = generate_password_hash(password)
    user = user_registration(name, email, hashed_password)
    
    if not user:
        return error_response("Gagal daftar", res_code=404)
    
    return success_response("Daftar berhasil", data=user, res_code=200)

def transaction():
    data = request.get_json()
    qty = data.get('qty')   #qty ini juga sebagai KG (jika type food waste yg dibeli nya adalah waste)
    price_food = data.get('price')
    payment_type = data.get('payment_type')
    user_id = data.get('user_id')
    food_waste_id = data.get('food_waste_id')

    transaction_date = datetime.now()
    status = 'pending'

    if not qty or not price_food or not payment_type or not user_id or not food_waste_id:
        return error_response("Wajib mengisi semua data", res_code=400)
    
    price_total = qty * price_food
    transaction = insert_transaction(qty, price_total, transaction_date, status, payment_type, user_id, food_waste_id)

    if not transaction:
        return error_response("Gagal transaksi", res_code=404)
    
    return success_response("Transaksi berhasil", data=transaction, res_code=200)

def invoice(transaction_id):
    try:
        invoice = get_invoice(transaction_id)

        if not invoice:
            return error_response("Data tidak tersediaaaaa", res_code=404)
        else:
            return success_response(data=invoice)
    except Exception as e:
        print(e)
        return error_response(message="Internal server error", res_code=500)

def payment_qris(transaction_id):
    try:
        data = put_payment_qris(transaction_id)

        if not data:
            return error_response("Data tidak tersediaaaaa", res_code=404)
        else:
            return success_response(data=data)
    except Exception as e:
        print(e)
        return error_response(message="Internal server error", res_code=500)

def update_transaction_status_controller(id):
    try:
        payload = request.get_json() or {}
        status = payload.get('status')
        if not status:
            return error_response("Field 'status' wajib diisi", res_code=400)

        updated, err = update_transaction_status(id, status)
        if err:
            return error_response(err, res_code=400)
        if not updated:
            return error_response("Update gagal", res_code=500)

        return success_response("Update status berhasil", data=updated)
    except Exception as e:
        print(e)
        return error_response("Internal server error", res_code=500)

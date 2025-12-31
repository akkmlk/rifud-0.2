from flask import Blueprint, jsonify, request
import os
from uuid import uuid4
from werkzeug.utils import secure_filename
from utils.res_wrapper import success_response, error_response
from models.food_waste import get_food_waste_filter, get_all_food_waste, get_food_waste_resto_filter, get_one_food_waste, insert_food_waste, put_update_food_waste, del_food_waste

UPLOAD_FOLDER = 'static/uploads/food_waste'

def food_waste_filter(city=None, type=None):
    try:
        data = get_food_waste_filter(city, type)

        if not data:
            return error_response("Data tidak tersediaaaaa", res_code=404)
        else:
            return success_response(data=data)
    except Exception as e:
        print(e)
        return error_response(message="Internal server error", res_code=500)
    
def all_food_waste(id):
    try:
        data = get_all_food_waste(id)

        if not data:
            return error_response("Data tidak tersediaaaaa", res_code=404)
        else:
            return success_response(data=data)
    except Exception as e:
        print(e)
        return error_response(message="Internal server error", res_code=500)
    
def food_waste_resto_filter(id, type):
    try:
        data = get_food_waste_resto_filter(id, type)

        if not data:
            return error_response("Data tidak tersediaaaaa", res_code=404)
        else:
            return success_response(data=data)
    except Exception as e:
        print(e)
        return error_response(message="Internal server error", res_code=500)

def one_food_waste(id):
    try:
        data = get_one_food_waste(id)

        if not data:
            return error_response("Data tidak tersediaaaaa", res_code=404)
        else:
            return success_response(data=data)
    except Exception as e:
        print(e)
        return error_response(message="Internal server error", res_code=500)
    
def add_food_waste():
    name = request.form.get('name')
    description = request.form.get('description')
    foto = request.files.get('foto')
    price = request.form.get('price')
    stock = request.form.get('stock')
    type = request.form.get('type')
    user_id = request.form.get('user_id')

    if not name or not description or not foto or not price or not stock or not type or not user_id:
        return error_response("Wajib mengisi semua data kecuali foto", res_code=400)
    
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    ext = foto.filename.rsplit('.', 1)[-1]
    filename = f"{uuid4().hex}.{ext}"
    filename = secure_filename(filename)
    save_path = os.path.join(UPLOAD_FOLDER, filename)
    foto.save(save_path)

    foto_path = f"uploads/food_waste/{filename}"

    try:
        food_waste = insert_food_waste(name, description, foto_path, price, stock, type, user_id)

        if not food_waste:
            return error_response("Tambah data gagal", res_code=404)

        return success_response("Tambah berhasil", data=food_waste)
    except Exception as e:
        print(e)
        return error_response(message="Internal server error", res_code=500)
    
def update_food_waste(id):
    name = request.form.get('name')
    description = request.form.get('description')
    foto = request.files.get('foto')
    price = request.form.get('price')
    stock = request.form.get('stock')
    type = request.form.get('type')

    if not name or not description or not price or not stock or not type:
        return error_response("Wajib mengisi semua data kecuali foto", res_code=400)
    
    foto_path = None
    if foto:
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        ext = foto.filename.rsplit('.', 1)[-1]
        filename = f"{uuid4().hex}.{ext}"
        filename = secure_filename(filename)
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        foto.save(save_path)

        foto_path = f"uploads/food_waste/{filename}"

    try:
        food_waste = put_update_food_waste(id, name, description, foto_path, price, stock, type)

        if not food_waste:
            return error_response("Data gagal updateeeeee", res_code=404)

        return success_response("Update berhasil", data=food_waste)
    except Exception as e:
        print(e)
        return error_response(message="Internal server error", res_code=500)
    
def delete_food_waste(id):
    try:
        food_waste = del_food_waste(id)
        if not food_waste:
            return error_response("Data tidak tersediaaaaa", res_code=404)
        
        if food_waste.get('foto'):
            foto_path = os.path.join("static", food_waste['foto'])
            if os.path.exists(foto_path):
                os.remove(foto_path)

        return success_response("Hapus berhasil", data=food_waste)
    except Exception as e:
        print(e)
        return error_response(message="Internal server error", res_code=500)
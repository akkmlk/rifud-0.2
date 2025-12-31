from extensions import mysql
from MySQLdb.cursors import DictCursor
from flask import url_for
import os

def get_food_waste_filter(city=None, type=None):
    cur = mysql.connection.cursor(DictCursor)
    query = """
                SELECT 
                food_waste.id AS id_food_waste,
                food_waste.name AS name, 
                food_waste.foto AS foto, 
                food_waste.price AS price, 
                food_waste.stock AS stock, 
                food_waste.description AS description, 
                food_waste.type AS type, 
                users.name AS resto_name, 
                users.city AS city, 
                users.address AS address,
                users.open_time AS open, 
                users.closed_time AS closed,
                users.longitude AS longitude,
                users.latitude AS latitude
                FROM food_waste 
                JOIN users ON food_waste.user_id = users.id 
                WHERE 1=1
                """
    params = []

    if city:
        query += " AND users.city = %s"
        params.append(city)

    if type:
        query += " AND food_waste.type = %s"
        params.append(type)

    query += " AND users.role = %s"
    params.append("resto")
    query += " LIMIT 8"
    cur.execute(query, tuple(params))
    data = cur.fetchall()
    cur.close()

    for row in data:
        if row.get('open'):
            row['open'] = str(row['open'])
        if row.get('closed'):
            row['closed'] = str(row['closed'])

        if row.get('foto'):
            row['foto_url'] = (url_for('static', filename=row['foto'], _external=True))
        else:
            row['foto_url'] = None

    return data

def get_food_waste_resto_filter(user_id, type):
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("SELECT * FROM food_waste WHERE user_id = %s AND type = %s ORDER BY stock DESC", (user_id, type, ))
    data = cur.fetchall()
    cur.close()
    return data

def get_all_food_waste(user_id):
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("SELECT * FROM food_waste WHERE user_id = %s ORDER BY stock DESC", (user_id, ))
    data = cur.fetchall()
    cur.close()
    return data

def get_one_food_waste(id):
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("SELECT * FROM food_waste WHERE id = %s ORDER BY stock DESC", (id, ))
    data = cur.fetchone()
    cur.close()
    return data

def insert_food_waste(name, description, foto, price, stock, type, user_id):
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("""
            INSERT INTO food_waste(
                name, 
                description, 
                foto, 
                price, 
                stock, 
                type, 
                user_id)
            VALUES(%s, %s, %s, %s, %s, %s, %s)
        """, (name, description, foto, price, stock, type, user_id, )
    )
    mysql.connection.commit()
    id_food_waste = cur.lastrowid

    cur.execute("SELECT * FROM food_waste WHERE id = %s", (id_food_waste, ))
    food_waste = cur.fetchone()
    cur.close()

    if food_waste.get('foto'):
        food_waste['foto_url'] = (url_for('static', filename=food_waste['foto'], _external=True))
    else:
        food_waste['foto_url'] = None

    return food_waste

def put_update_food_waste(id, name, description, foto, price, stock, type):
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("SELECT foto FROM food_waste WHERE id = %s", (id, ))
    old_data = cur.fetchone()
    old_foto = old_data['foto'] if old_data else None

    query = """UPDATE 
                food_waste SET 
                name = %s, 
                description = %s, 
                price = %s, 
                stock = %s, 
                type = %s"""
    
    params = [name, description, price, stock, type] 
    if foto:
        if old_foto:
            old_path = os.path.join("static", old_foto)
            if os.path.exists(old_path):
                os.remove(old_path)

        query += ", foto = %s"
        params.append(foto)

    query += " WHERE id = %s"
    params.append(id)

    cur.execute(query, tuple(params))
    mysql.connection.commit()

    if cur.rowcount == 0:
        cur.close()
        return None

    cur.execute("SELECT * FROM food_waste WHERE id = %s", (id, ))
    food_waste = cur.fetchone()
    cur.close()

    if food_waste.get('foto'):
        food_waste['foto_url'] = (url_for('static', filename=food_waste['foto'], _external=True))
    else:
        food_waste['foto_url'] = None

    return food_waste

def del_food_waste(id):
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("SELECT * FROM food_waste WHERE id = %s", (id, ))
    food_waste = cur.fetchone()

    if not food_waste:
        cur.close()
        return None

    cur.execute("DELETE FROM food_waste WHERE id = %s", (id, ))
    mysql.connection.commit()
    cur.close()
    return food_waste
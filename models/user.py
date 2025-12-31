import os
from datetime import timedelta
from flask import url_for
from extensions import mysql
from MySQLdb.cursors import DictCursor

def get_profile(id):
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("SELECT * FROM users WHERE id = %s", (id,))
    profile = cur.fetchone()
    cur.close()

    if profile.get('open_time'):
        profile['open_time'] = str(profile['open_time'])
    if profile.get('closed_time'):
        profile['closed_time'] = str(profile['closed_time'])

    return profile

def put_profile(id, data):
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("SELECT foto FROM users WHERE id = %s", (id,))
    old_data = cur.fetchone()
    old_foto = old_data['foto'] if old_data else None

    foto = data.get('foto')
    if foto:
        if old_foto:
            old_path = os.path.join("static", old_foto)
            if os.path.exists(old_path):
                os.remove(old_path)

    fields = []
    params = []

    for key, value in data.items():
        if value is not None:
            fields.append(f"{key} = %s")
            params.append(value)

    if not fields:
        return None
    
    query = f"""
                UPDATE users SET {', '.join(fields)}
                WHERE id = %s
        """
    params.append(id)

    cur.execute(query, tuple(params))
    mysql.connection.commit()
    
    cur.execute("SELECT * FROM users WHERE id = %s", (id, ))
    user = cur.fetchone()
    cur.close()

    if user.get('foto'):
        user['foto_url'] = (url_for('static', filename=user['foto'], _external=True))
    else:
        user['foto_url'] = None

    if isinstance(user.get('open_time'), timedelta):
        user['open_time'] = str(user['open_time'])
    if isinstance(user.get('closed_time'), timedelta):
        user['closed_time'] = str(user['closed_time'])

    return user

def get_available_city():
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("SELECT DISTINCT city FROM users ORDER BY city ASC")
    citys = cur.fetchall()
    cur.close()
    return citys

def get_your_order(id):
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("""
        SELECT 
            users.foto AS foto_resto,
            transactions.id AS id_transaction,
            food_waste.name AS name,
            food_waste.foto AS foto_fw,
            food_waste.description AS description,
            transactions.status AS status,
            transactions.price_total AS price_total,
            CONCAT(
                CASE DAYNAME(transactions.transaction_date)
                    WHEN 'Monday' THEN 'Senin'
                    WHEN 'Tuesday' THEN 'Selasa'
                    WHEN 'Wednesday' THEN 'Rabu'
                    WHEN 'Thursday' THEN 'Kamis'
                    WHEN 'Friday' THEN 'Jumat'
                    WHEN 'Saturday' THEN 'Sabtu'
                    WHEN 'Sunday' THEN 'Minggu'
                END,
                ', ',
                DATE_FORMAT(transactions.transaction_date, '%%H:%%i:%%s')
            ) AS transaction_date
        FROM transactions
        JOIN food_waste ON transactions.food_waste_id = food_waste.id
        JOIN users ON transactions.user_id = users.id
        WHERE users.id = %s 
                AND transactions.status IN ('pending', 'waiting', 'ready')
        ORDER BY transactions.transaction_date ASC
    """, (id,))
    your_order = cur.fetchall()
    cur.close()

    for row in your_order:
        if row.get('foto_fw'):
            row['url_foto_fw'] = (url_for('static', filename=row['foto_fw'], _external=True))
        if row.get('foto_resto'):
            row['url_foto_resto'] = (url_for('static', filename=row['foto_resto'], _external=True))
    return your_order

def get_transactions_history(id):
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("""
        SELECT 
            users.foto AS foto_resto,
            transactions.id AS id_transaction,
            food_waste.name AS name,
            food_waste.foto AS foto_fw,
            food_waste.description AS description,
            transactions.status AS status,
            transactions.price_total AS price_total,
            CONCAT(
                CASE DAYNAME(transactions.transaction_date)
                    WHEN 'Monday' THEN 'Senin'
                    WHEN 'Tuesday' THEN 'Selasa'
                    WHEN 'Wednesday' THEN 'Rabu'
                    WHEN 'Thursday' THEN 'Kamis'
                    WHEN 'Friday' THEN 'Jumat'
                    WHEN 'Saturday' THEN 'Sabtu'
                    WHEN 'Sunday' THEN 'Minggu'
                END,
                ', ',
                DATE_FORMAT(transactions.transaction_date, '%%H:%%i:%%s')
            ) AS transaction_date
        FROM transactions
        JOIN food_waste ON transactions.food_waste_id = food_waste.id
        JOIN users ON transactions.user_id = users.id
        WHERE users.id = %s 
                AND transactions.status IN ('success', 'cancel', 'declined')
        ORDER BY transactions.transaction_date ASC
    """, (id,))
    transactions_history = cur.fetchall()
    cur.close()

    for row in transactions_history:
        if row.get('foto_fw'):
            row['foto_url_fw'] = (url_for('static', filename=row['foto_fw'], _external=True))
        else:
            row['foto_url_fw'] = None

        if row.get('foto_resto'):
            row['foto_url_resto'] = (url_for('static', filename=row['foto_resto'], _external=True))
        else:
            row['foto_url_resto'] = None
    return transactions_history

def login(email):
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("SELECT id, name, phone, email, password, address, role FROM users WHERE email = %s", (email, ))
    data = cur.fetchone()
    cur.close()
    return data

def resto_registration(email, password, name, city, address, role):
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("INSERT INTO users (email, password, name, city, address, role) VALUES (%s, %s, %s, %s, %s, %s)", (email, password, name, city, address, role))
    mysql.connection.commit()

    user_id = cur.lastrowid
    cur.execute("SELECT id, name, email, password, city, address, role FROM users WHERE id = %s", (user_id, ))
    user = cur.fetchone()
    cur.close()
    return user

def user_registration(name, email, password):
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password, ))
    mysql.connection.commit()

    user_id = cur.lastrowid
    cur.execute("SELECT id, name, email, password FROM users WHERE id = %s", (user_id, ))
    user = cur.fetchone()
    cur.close()
    return user

def insert_transaction(qty, price_total, transaction_date, status, payment_type, user_id, food_waste_id):
    cur = mysql.connection.cursor(DictCursor)

    cur.execute("""
        INSERT INTO transactions (
            qty, price_total, transaction_date,
            status, payment_type, user_id, food_waste_id
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (qty, price_total, transaction_date, status, payment_type, user_id, food_waste_id))
    mysql.connection.commit()

    transaction_id = cur.lastrowid
    cur.execute("SELECT * FROM transactions WHERE id = %s", (transaction_id,))
    transaction = cur.fetchone()

    cur.execute(
        "SELECT * FROM food_waste WHERE id = %s",
        (transaction['food_waste_id'],)
    )
    food_waste = cur.fetchone()

    reduce_qty = food_waste['stock'] - qty
    cur.execute(
        "UPDATE food_waste SET stock = %s WHERE id = %s", (reduce_qty, transaction['food_waste_id'])
    )
    mysql.connection.commit()
    cur.close()

    if transaction.get('transaction_date'):
        transaction['transaction_date'] = str(transaction['transaction_date'])

    return transaction


def get_invoice(transaction_id):
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("""SELECT 
                transactions.id, 
                food_waste.foto, 
                food_waste.price, 
                buyer.name AS pembeli, 
                seller.name AS resto_name, 
                food_waste.name AS fw_name, 
                transactions.qty, 
                transactions.price_total, 
                transactions.payment_type, 
                transactions.status 
                FROM transactions 
                JOIN users buyer ON transactions.user_id = buyer.id 
                JOIN food_waste ON transactions.food_waste_id = food_waste.id 
                JOIN users seller on food_waste.user_id = seller.id
                WHERE transactions.id = %s """, (transaction_id, ))
    invoice = cur.fetchone()
    cur.close()

    if invoice.get('foto'):
        invoice['url_foto_fw'] = (url_for('static', filename=invoice['foto'], _external=True))

    return invoice

def put_payment_qris(transaction_id):
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("UPDATE transactions SET status = %s WHERE id = %s", ("waiting", transaction_id, ))
    mysql.connection.commit()
    cur.close()

    return transaction_id

def get_order(resto_id):
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("""SELECT 
                transactions.id, 
                food_waste.foto, 
                food_waste.type, 
                users.name AS pembeli, 
                food_waste.name AS fw_name, 
                transactions.qty, 
                transactions.price_total, 
                transactions.payment_type, 
                transactions.status 
                FROM transactions 
                JOIN users ON transactions.user_id = users.id 
                JOIN food_waste ON transactions.food_waste_id = food_waste.id 
                WHERE food_waste.user_id = %s 
                AND transactions.status IN ('waiting', 'ready')
                ORDER BY transactions.transaction_date DESC""", (resto_id, ))
    order = cur.fetchall()
    cur.close()

    for row in order:
        if row.get('foto'):
            row['url_foto_fw'] = (url_for('static', filename=row['foto'], _external=True))
    return order

def get_order_history(resto_id):
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("""SELECT 
                transactions.id, 
                food_waste.foto, 
                food_waste.type, 
                users.name AS pembeli, 
                food_waste.name AS fw_name, 
                transactions.qty, 
                transactions.price_total, 
                transactions.payment_type, 
                transactions.status 
                FROM transactions 
                JOIN users ON transactions.user_id = users.id 
                JOIN food_waste ON transactions.food_waste_id = food_waste.id 
                WHERE food_waste.user_id = %s 
                AND transactions.status IN ('success', 'declined')
                ORDER BY transactions.transaction_date DESC""", (resto_id, ))
    order_history = cur.fetchall()
    cur.close()

    for row in order_history:
        if row.get('foto'):
            row['url_foto_fw'] = (url_for('static', filename=row['foto'], _external=True))
    return order_history

def update_transaction_status(tx_id, new_status):
    cur = mysql.connection.cursor(DictCursor)
    allowed = ('pending','waiting','ready','success','declined','cancel')
    if new_status not in allowed:
        cur.close()
        return None, f"Status tidak valid. Nilai yang diizinkan: {', '.join(allowed)}"

    cur.execute("SELECT * FROM transactions WHERE id = %s", (tx_id,))
    row = cur.fetchone()
    if not row:
        cur.close()
        return None, "Transaksi tidak ditemukan"

    cur.execute("UPDATE transactions SET status = %s WHERE id = %s", (new_status, tx_id))
    mysql.connection.commit()

    cur.execute("SELECT * FROM transactions WHERE id = %s", (tx_id,))
    new_row = cur.fetchone()
    cur.close()
    return new_row, None
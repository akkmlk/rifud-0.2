from flask import Blueprint, render_template, session, redirect, abort, request

pages = Blueprint("pages", __name__)

@pages.route('/')
def index():
    return render_template('user/index.html')

# Auth
@pages.route('/register')
def register():
    return render_template('auth/register.html')

@pages.route('/register-resto')
def register_resto():
    return render_template('auth/regist_resto.html')

@pages.route('/login')
def login():
    return render_template('auth/login.html')

@pages.route('/profile')
def profile():
    role = session.get('role')
    if not role:
        return redirect('/login')
    
    if role == 'resto':
        base = 'layout/base_resto.html'
    elif role == 'client':
        base = 'layout/base_user.html'
    return render_template('shared/profile.html', base_template=base)

# Resto
@pages.route('/daftar')
def daftar():
    return render_template('resto/index.html')

@pages.route('/tambah')
def tambah():
    return render_template('resto/add.html')

@pages.route('/edit/<int:id>')
def edit(id):
    return render_template('resto/edit.html', food_id=id)

@pages.route('/pesanan')
def pesanan():
    return render_template('resto/daftar_pesanan.html')

@pages.route('/riwayat_pesanan')
def riwayat_pesanan():
    return render_template('resto/riwayat_pesanan.html')

@pages.route('/home-resto')
def home_resto():
    return render_template('resto/home.html')

# @pages.route('/dashboard')
# def frameset():
#     return render_template('layout/base_resto.html')

@pages.route('/navbar')
def navbar():
    return render_template('resto/navbar.html')

@pages.route('/sidebar')
def sidebar():
    return render_template('resto/sidebar.html')

# User
@pages.route('/transaction-history')
def transaction_history():
    return render_template('user/transaction_history.html')

@pages.route('/your-order')
def your_order():
    return render_template('user/orderan_anda.html')

@pages.route('/invoice')
def invoice():
    transaction_id = request.args.get('id', type=int)

    if not transaction_id:
        abort(404)
    return render_template('user/invoice.html')
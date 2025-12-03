from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from Ramy_Store.auth import login_required
from Ramy_Store.db import get_db

bp = Blueprint('categories', __name__,  url_prefix='/categories')

@bp.route('/furniture')
def furniture():
    db = get_db()
    products = db.execute(
        'SELECT p.product_id, name, price, image_url, category, details'
        ' FROM products p'
        " WHERE category = 'furniture';"
    ).fetchall()
    return render_template("store/category.html", products=products)

@bp.route('/mobile_phones')
def mobile_phones():
    db = get_db()
    products = db.execute(
        'SELECT p.product_id, name, price, image_url, category, details'
        ' FROM products p'
        " WHERE category = 'mobile_phones';"
    ).fetchall()
    return render_template("store/category.html", products=products)

@bp.route('/home_essentials')
def home_essentials():
    db = get_db()
    products = db.execute(
        'SELECT p.product_id, name, price, image_url, category, details'
        ' FROM products p'
        " WHERE category = 'home_essentials';"
    ).fetchall()
    return render_template("store/category.html", products=products)

@bp.route('/perfumes')
def perfumes():
    db = get_db()
    products = db.execute(
        'SELECT p.product_id, name, price, image_url, category, details'
        ' FROM products p'
        " WHERE category = 'perfumes';"
    ).fetchall()
    return render_template("store/category.html", products=products)

@bp.route('/books')
def books():
    db = get_db()
    products = db.execute(
        'SELECT p.product_id, name, price, image_url, category, details'
        ' FROM products p'
        " WHERE category = 'books';"
    ).fetchall()
    return render_template("store/category.html", products=products)

@bp.route('/medical_devices')
def medical_devices():
    db = get_db()
    products = db.execute(
        'SELECT p.product_id, name, price, image_url, category, details'
        ' FROM products p'
        " WHERE category = 'medical_devices';"
    ).fetchall()
    return render_template("store/category.html", products=products)

@bp.route('/electronics')
def electronics():
    db = get_db()
    products = db.execute(
        'SELECT p.product_id, name, price, image_url, category, details'
        ' FROM products p'
        " WHERE category = 'electronics';"
    ).fetchall()
    return render_template("store/category.html", products=products)

@bp.route('/toys')
def toys():
    db = get_db()
    products = db.execute(
        'SELECT p.product_id, name, price, image_url, category, details'
        ' FROM products p'
        " WHERE category = 'toys';"
    ).fetchall()
    return render_template("store/category.html", products=products)
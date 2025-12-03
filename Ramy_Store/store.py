from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from Ramy_Store.auth import login_required
from Ramy_Store.db import get_db

bp = Blueprint('store', __name__,)

@bp.route('/')
def index():
    # كود يظهر عروض عشوائيه في الصفحه الرئيسيه
    db = get_db()
    random_products = db.execute(
    'SELECT product_id, name, price, image_url, category, details FROM products ORDER BY RANDOM() LIMIT 9;'
    ).fetchall()
    return render_template("store/index.html", random_products=random_products)


@bp.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    if request.method == 'POST':
        db = get_db()
        # التحقق من أن المنتج موجود
        product = db.execute(
            'SELECT * FROM products WHERE product_id = ?', (product_id,)
        ).fetchone()

        if product is None:
            flash('المنتج غير موجود')
            return redirect(request.referrer or url_for('store.index'))
        
        db.execute(
            'INSERT INTO cart_items (product_id ,user_id)'
            ' VALUES (?, ?)',
            (product_id, g.user['id'])
        )
        db.commit()
        flash('تم إضافة المنتج إلى السلة بنجاح! ')

        return redirect(request.referrer or url_for('store.index'))


@bp.route('/cart')
@login_required
def cart():
    db = get_db()
    cart_items = db.execute(
        'SELECT ci.user_id, p.name AS product_name, p.price,  p.image_url, ci.added_at, cart_item_id'
        ' FROM cart_items ci'
        ' JOIN products p ON ci.product_id = p.product_id'
        " WHERE ci.user_id = ?"
        ' ORDER BY ci.added_at DESC',
        (g.user['id'],)
    ).fetchall()
    
    user_name = db.execute("SELECT username FROM user WHERE id = ?", (g.user['id'],)).fetchone()

    # تحويل UTC إلى توقيتنا المحلي (+3) لكي تظهر الساعه في وقت الاضافه للسله بشكل صحيح
    from datetime import timedelta

    return render_template("store/cart.html", timedelta=timedelta, cart_items=cart_items, user_name = user_name )


@bp.route('/delete_item_from_cart/<int:item_id>', methods=['POST'])
@login_required
def delete_item_from_cart(item_id):
    if request.method == 'POST':
        db = get_db()
        db.execute('DELETE FROM cart_items WHERE cart_item_id = ?', (item_id,))
        db.commit()
        return redirect(request.referrer or url_for('store.index'))


@bp.route('/payment_step')
@login_required
def payment_step():
    return render_template("store/payment_step.html")


@bp.route('/search')
def search():
    db = get_db()
    query = request.args.get('q', '').strip()
    results = None
    if query:
        
        results = db.execute(
            'SELECT product_id, name, price, image_url, category, details FROM products'
            " WHERE LOWER(name) LIKE LOWER('%' || ? || '%')"
            " OR LOWER(details) LIKE LOWER('%' || ? || '%')"
            ,(query,query)
        ).fetchall()

    return render_template("store/search.html", results=results  ,query=query)



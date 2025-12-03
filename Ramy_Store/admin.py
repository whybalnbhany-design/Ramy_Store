import os
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)
from werkzeug.exceptions import abort

from Ramy_Store.auth import login_required
from Ramy_Store.db import get_db

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/')
@login_required
def index():
    db = get_db()
    user_name = db.execute("SELECT username FROM user WHERE id = ?", (g.user['id'],)).fetchone()
    users = db.execute("SELECT username FROM user").fetchall()
    products = db.execute(
        'SELECT product_id,name, price, category, details'
        ' FROM products'
    ).fetchall()
    return render_template("admin/index.html", user_name=user_name, users=users, products=products)

@bp.route('/create_product', methods=['GET','POST'])
@login_required
def create_product():
    db = get_db()
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        category = request.form['category']
        description = request.form['description']

        # استقبال ملف الصورة 
        image = request.files.get('image')

        image_filename = None

        if image:
            # حفظ اسم الصورة
            image_filename = image.filename

            # حفظ الصورة داخل uploads
            image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], image_filename))

        # الآن خزّن بيانات المنتج والصورة بقاعدة البيانات
        db.execute("""INSERT INTO products (name, price, image_url, category, details)
                                VALUES (?, ?, ?, ?, ?)""",
                                (name, price, f'uploads/{image_filename}', category, description))
        db.commit()
        flash('تم اضافة المنتج بنجاح', 'success')
        return redirect(url_for('admin.index')) 
    return render_template("admin/create_product.html")

def get_product(id):
    db = get_db()
    product = db.execute(
        'SELECT product_id,name, price, image_url, category, details'
        ' FROM products'
        ' WHERE product_id = ?',
        (id,)
    ).fetchone()

    if product is None:
        abort(404, f"product id {id} doesn't exist.")

    return product

@bp.route('/<int:product_id>/edit_product', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    # جلب بيانات المنتج الحالي من قاعدة البيانات
    product = get_product(product_id)

    if request.method == 'POST':
        # قراءة البيانات من النموذج
        name = request.form['name']
        price = request.form['price']
        category = request.form['category']
        description = request.form['description']

        # استقبال ملف الصورة الجديد إن وُجد
        image = request.files.get('image')
        image_url = product['image_url']  # القيمة الافتراضية تبقى كما هي (الصورة القديمة)

        if image:
            upload_folder = current_app.config['UPLOAD_FOLDER']

            # استخراج اسم الملف فقط (بدون المسار) لتفادي مشاكل المسارات
            filename = os.path.basename(image.filename)

            # بناء المسار الكامل لحفظ الصورة الجديدة
            save_path = os.path.join(upload_folder, filename)

            # حفظ الصورة داخل مجلد uploads
            try:
                image.save(save_path)
            except Exception as e:
                current_app.logger.error(f"فشل حفظ الصورة الجديدة: {e}")
                flash('حدث خطأ أثناء حفظ الصورة الجديدة', 'danger')
                return redirect(url_for('admin.edit_product', product_id=product_id))

            # تحديث الرابط الجديد ليكون اسم الملف فقط
            image_url = filename

            # حذف الصورة القديمة إن كانت موجودة
            if product['image_url']:
                # بناء المسار الكامل للصورة القديمة داخل مجلد uploads
                old_path = os.path.join(upload_folder, os.path.basename(product['image_url']))
                if os.path.exists(old_path):
                    try:
                        os.remove(old_path)
                    except OSError:
                        pass

        # تحديث بيانات المنتج في قاعدة البيانات
        db = get_db()
        db.execute(
            'UPDATE products SET name = ?, price = ?, image_url = ?, category = ?, details = ? '
            'WHERE product_id = ?',
            (name, price, f'uploads/{image_url}', category, description, product_id)
        )
        db.commit()

        flash('تم تحديث المنتج بنجاح', 'success')
        return redirect(url_for('admin.index'))

    # إذا كان الطلب GET -> عرض النموذج مع بيانات المنتج الحالية
    return render_template('admin/edit_product.html', product=product)

@bp.route('/<int:product_id>/delete_product', methods=('POST',))
@login_required
def delete_product(product_id):
    db = get_db()
    product = get_product(product_id)

    upload_folder = current_app.config['UPLOAD_FOLDER']

    if product['image_url']:
        # تأكد أن المسار داخل مجلد uploads
        old_path = os.path.join(upload_folder, os.path.basename(product['image_url']))
        if os.path.exists(old_path):
            try:
                os.remove(old_path)
            except OSError as e:
                current_app.logger.error(f"فشل حذف الملف: {e}")

    db.execute('DELETE FROM products WHERE product_id = ?', (product_id,))
    db.commit()
    flash('تم حذف المنتج بنجاح', 'success')
    return redirect(url_for('admin.index'))
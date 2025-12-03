import os

from flask import Flask, render_template, request


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'Ramy_Store.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import categories
    app.register_blueprint(categories.bp)

    from . import store
    app.register_blueprint(store.bp)
    app.add_url_rule('/', endpoint='index') 

    from . import admin
    app.register_blueprint(admin.bp)

    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # علشان نحول اسماء الفئات الانجليزيه الى العربيه في صفحة ادارة المتجر
    category_map = {
        "books": "الكتب",
        "electronics": "الالكترونيات",
        "furniture": "الاثاث",
        "home_essentials": "مستلزمات المنزل",
        "medical_devices": "الاجهزة الطبية",
        "mobile_phones": "الجوالات",
        "perfumes": "العطور",
        "toys": "العاب الاطفال"
    }
    
    # فلتر jinja 
    @app.template_filter("translate_category")
    def translate_category_filter(value):
        return category_map.get(value, value)  # إذا غير موجود يرجع نفس القيمة


    return app

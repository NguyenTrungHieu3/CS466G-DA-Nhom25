from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

 # Tạo đối tượng db với SQLAlchemy để quản lý CSDL đây là công cụ ORM (Object Relational Mapping) dùng để tương tác với cơ sở dữ liệu.
db = SQLAlchemy()
DB_NAME = 'database.sqlite3'


def create_database():
    # tạo các bảng từ các model đã định nghĩa
    db.create_all()
    print('Database Created')


def create_app():
    # Khởi tạo ứng dụng Flask
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hbnwdvbn ajnbsjn ahe'
    # Kết nối csdl, ứng dụng sử dụng SQLite với tên tệp là database.sqlite3.
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html')

    # quản lý quá trình đăng nhập và bảo mật
    login_manager = LoginManager()
    login_manager.init_app(app)
    # định nghĩa view nào sẽ được sử dụng khi người dùng chưa đăng nhập và cố gắng truy cập vào một trang yêu cầu đăng nhập.
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    # Hàm load_user dùng để tải người dùng từ cơ sở dữ liệu dựa trên ID
    def load_user(id):
        # sẽ tìm người dùng có ID tương ứng trong bảng Customer.
        return Customer.query.get(int(id))

    from .views import views
    from .auth import auth
    from .admin import admin
    from .models import Customer, Cart, Product, Order

    app.register_blueprint(views, url_prefix='/') 
    app.register_blueprint(auth, url_prefix='/') 
    app.register_blueprint(admin, url_prefix='/')

    # with app.app_context():
    #     create_database()

    return app


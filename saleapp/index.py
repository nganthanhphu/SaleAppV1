from flask import render_template, request
from werkzeug.utils import redirect

from saleapp import app, login_manager, admin
import dao, math
from flask_login import login_user, current_user, logout_user


@app.route('/')
def index():
    q = request.args.get("q")
    cate_id = request.args.get("cate_id")
    page = request.args.get("page")
    if not page:
        page = 1
    products = dao.load_products(q, cate_id, page)
    pages = math.ceil(dao.count_product() / app.config["PAGE_SIZE"])
    return render_template("index.html", products=products, pages=pages)


@app.route('/product/<int:id>')
def detail(id):
    product = dao.load_product_by_id(id)
    return render_template("product_detail.html", product=product)


@app.route('/login', methods=['get', 'post'])
def login():
    if current_user.is_authenticated:
        return redirect('/')

    err_msg = None

    if request.method.__eq__('POST'):
        username = request.form.get('username')
        pwd = request.form.get('pwd')
        user = dao.auth_user(username, pwd)
        if user:
            login_user(user)
            return redirect('/')
        else:
            err_msg = "Tài khoản hoặc mật khẩu không đúng!"

    return render_template("login.html", err_msg=err_msg)


@login_manager.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id=user_id)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@app.context_processor
def common_attribute():
    return {
        "cates": dao.load_categories()
    }


if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)

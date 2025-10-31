from flask import render_template, request
from saleapp import app
import dao, math

@app.route('/')
def index():
    q = request.args.get("q")
    cate_id = request.args.get("cate_id")
    page = request.args.get("page")
    products = dao.load_products(q, cate_id, page)
    pages = math.ceil(dao.count_product()/app.config["PAGE_SIZE"])
    return render_template("index.html", products = products, pages = pages)

@app.route('/product/<int:id>')
def detail(id):
    product = dao.load_product_by_id(id)
    return render_template("product_detail.html", product = product)


@app.route('/login')
def login():
    return render_template("login.html")

@app.context_processor
def common_attribute():
    return{
        "cates": dao.load_categories()
    }

if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)

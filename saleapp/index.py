from itertools import product

from flask import Flask, render_template, request
from dao import load_categories, load_products, load_product_by_id

app = Flask(__name__)

@app.route('/')
def index():
    q = request.args.get("q")
    cate_id = request.args.get("cate_id")
    cates = load_categories()
    products = load_products(q, cate_id)
    return render_template("index.html", cates = cates, products = products)

@app.route('/product/<int:id>')
def detail(id):
    product = load_product_by_id(id)
    return render_template("product_detail.html", product = product)

if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)

from flask import redirect
from flask_admin import Admin, AdminIndexView, expose, BaseView
from flask_admin.contrib.sqla import ModelView
from flask_admin.theme import Bootstrap4Theme
from flask_login import current_user, logout_user
from saleapp import app, db
from saleapp.models import Category, Product

class MyCategoryView(ModelView):
    column_list = ['name', 'products']
    column_searchable_list = ['name']
    column_filters = ['name']

    def is_accessible(self) -> bool:
        return current_user.is_authenticated

class MyIndexView(AdminIndexView):
    @expose('/')
    def index(self) -> str:
        return self.render('admin/index.html')

class MyLogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect("/admin")

    def is_accessible(self) -> bool:
        return current_user.is_authenticated

admin = Admin(app=app, name='E-COMMERCE', theme=Bootstrap4Theme(), index_view=MyIndexView())

admin.add_view(MyCategoryView(Category, db.session))
admin.add_view(ModelView(Product, db.session))
admin.add_view(MyLogoutView("Đăng xuất"))
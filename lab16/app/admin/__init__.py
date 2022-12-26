from flask import flash, redirect, url_for
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.fileadmin import FileAdmin
from flask_login import current_user

from app.admin.models import UserModelView, TaskModelView, CategoryModelView
from app.auth.models import User
from app.todo.models import Task, Category

import os.path as op


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            flash('Please log in first...', 'error')
            return redirect(url_for('auth.login'))
        if current_user.is_admin:
            return super(MyAdminIndexView, self).index()
        else:
            return redirect(url_for("main"))


def create_module(db, **kwargs):
    admin = Admin(name='Flask Site', template_mode='bootstrap3', index_view=MyAdminIndexView())

    admin.add_view(UserModelView(User, db.session, name='Користувачі',))
    admin.add_view(TaskModelView(Task, db.session, name='Задачі'))
    admin.add_view(CategoryModelView(Category, db.session, name='Категорії'))

    path = op.join(op.dirname(__file__), '..', 'static')
    admin.add_view(FileAdmin(path, '/static/', name='Static Files'))

    return admin
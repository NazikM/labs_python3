from app import bcrypt
from app.admin.views import MyModelView


class UserModelView(MyModelView):
    form_columns = ('username',
                    'email',
                    'about_me',
                    'is_admin',
                    'password')

    column_labels = dict(username='username',
                         email='Email',
                         about_me='About me',
                         is_admin='Is admin',
                         password_hashed='Password')

    def on_model_change(self, form, model, is_created):
        enc_password = form.password_hashed.data.encode('utf-8')
        model.password_hashed = bcrypt.generate_password_hash(enc_password).decode('utf-8')


class TaskModelView(MyModelView):
    column_searchable_list = ['title']
    column_filters = ['priority', 'progress']
    column_sortable_list = ['deadline']

    form_excluded_columns = ('users', 'comments', 'created', 'modified')


class CategoryModelView(MyModelView):
    column_searchable_list = ['name']
    column_filters = ['name']

    form_excluded_columns = 'tasks'
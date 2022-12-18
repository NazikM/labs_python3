from functools import wraps
import datetime

from jwt import ExpiredSignatureError

from app.task_api import api2_bp
from app import db, bcrypt, SECRET_KEY
from app.todo.models import Task
from app.auth.models import User
from flask import request, jsonify, make_response
import jwt
from flask_restful import Resource, Api, reqparse, fields, marshal_with

api = Api(api2_bp)

parser = reqparse.RequestParser()
parser.add_argument('title')
parser.add_argument('description')
parser.add_argument('deadline')
parser.add_argument('priority')
parser.add_argument('category')
parser.add_argument('progress')

product_fields = {
            'id': fields.Integer,
            'title': fields.String,
            'description': fields.String,
            'deadline': fields.DateTime,
            'priority': fields.String,
            'progress': fields.String,
            'category': fields.String
}

def protected(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Token')
        if auth:
            try:
                user_data = jwt.decode(auth, SECRET_KEY, algorithms='HS256')
            except ExpiredSignatureError:
                return make_response(jsonify({'message': 'Token expired!'}), 403)
            user = User.query.filter_by(id=int(user_data['id'])).first()
            return f(*args, user=user, **kwargs)
        return make_response(jsonify({'message': 'Authentication failed!'}), 403)
    return decorated


@api2_bp.route('/login')
def login_api():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticated': 'Basic realm="Login reguired!"'})

    user = User.query.filter_by(username=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticated': 'Basic realm="Login reguired!"'})

    if bcrypt.check_password_hash(user.password, auth.password):
        token = jwt.encode({'id': str(user.id), 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                           SECRET_KEY)

        return jsonify({'token': token})
    return make_response('Could not verify', 401, {'WWW-Authenticated': 'Basic realm="Login reguired!"'})


class TaskList(Resource):
    @protected
    @marshal_with(product_fields)
    def get(self, user):
        return user.tasks_owned.all()

    @protected
    @marshal_with(product_fields)
    def post(self, user):
        args = parser.parse_args()
        title = args['title']
        description = args['description']
        deadline = datetime.datetime.strptime(args['deadline'], '%Y-%m-%d')
        priority = args['priority']
        progress = args['progress']
        category = args['category']
        task_info = Task(title=title,
                         description=description,
                         deadline=deadline,
                         priority=priority,
                         progress=progress,
                         category_id=category,
                         owner=user)
        task_info.users.append(user)
        db.session.add(task_info)
        db.session.commit()

        task = Task.query.filter_by(title=title).first()
        return task


class TaskDetail(Resource):
    @protected
    @marshal_with(product_fields)
    def get(self, user, task_id):
        return Task.query.filter_by(id=task_id).first()

    @protected
    @marshal_with(product_fields)
    def put(self, user, task_id):
        args = parser.parse_args()
        title = args['title']
        description = args['description']
        deadline = datetime.datetime.strptime(args['deadline'], '%Y-%m-%d')
        priority = args['priority']
        progress = args['progress']

        task = Task.query.filter_by(id=task_id).first()
        task.title = title
        task.description = description
        task.deadline = deadline
        task.priority = priority
        task.progress = progress
        db.session.add(task)
        db.session.commit()

        return task

    @protected
    def delete(self, user, task_id):
        task = Task.query.filter_by(id=task_id).first()
        db.session.delete(task)
        db.session.commit()
        return {"message": "Successfully deleted!"}


api.add_resource(TaskList, '/')
api.add_resource(TaskDetail, '/<task_id>')

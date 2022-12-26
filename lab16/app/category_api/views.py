from functools import wraps
import datetime

from app.category_api import api_bp
from app import db, bcrypt, SECRET_KEY
from app.todo.models import Category
from app.auth.models import User

from sqlalchemy.exc import IntegrityError
from flask import request, jsonify, make_response
import jwt


def protected(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth:
            user = User.query.filter_by(username=auth.username).first()
            if user and user.verify_password(auth.password):
                return f(*args, **kwargs)
        return jsonify({'message': 'Authentication failed!'}), 403
    return decorated


@api_bp.route('/login')
def login_api():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticated': 'Basic realm="Login reguired!"'})

    user = User.query.filter_by(username=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticated': 'Basic realm="Login reguired!"'})

    if bcrypt.check_password_hash(user.password, auth.password):
        token = jwt.encode({'id': str(user.id), 'exp': str(datetime.datetime.utcnow() + datetime.timedelta(minutes=30))},
                           SECRET_KEY)

        return jsonify({'token': token})
    return make_response('Could not verify', 401, {'WWW-Authenticated': 'Basic realm="Login reguired!"'})


# GET  api/entities - get list of entities
@api_bp.route('/category', methods=['GET'])
@protected
def get_categories():
    categories = Category.query.all()

    categories_json = []

    for category in categories:
        category_dict = {}
        category_dict['id'] = category.id
        category_dict['name'] = category.name
        categories_json.append(category_dict)

    return jsonify({'categories': categories_json})


# POST / entities - create an entity
@api_bp.route('/category', methods=['POST'])
@protected
def add_category():
    new_category_data = request.get_json()

    if not new_category_data:
        return {'message': 'No input data provided'}, 400
    print(new_category_data)
    name = new_category_data.get('name')
    if not name:
        return jsonify({'message': 'Not key with name'}), 422

    category = Category.query.filter_by(name=name).first()

    if category:
        return jsonify({'message': f'Категорія з назвою {name} існує'}), 400

    category_new = Category(name=name)
    db.session.add(category_new)
    db.session.commit()

    category_add = Category.query.filter_by(name=name).first()

    return jsonify({'id': category_add.id, 'name': category_add.name}), 201


# GET /entities/<entity_id> - get entity information
@api_bp.route('/category/<int:id>', methods=['GET'])
@protected
def get_category(id):
    category = Category.query.get_or_404(id)
    # if not category:
    #   return jsonify({'message' : 'Нема такої категорії'}), 404

    output = {'id': category.id, 'name': category.name}
    return jsonify({'category': output})


# PUT / entities/<entity_id> - update entity
@api_bp.route('/category/<int:id>', methods=['PUT'])
@protected
def edit_category(id):
    new_category_data = request.get_json()

    name = new_category_data.get('name')
    if not name:
        return jsonify({'message': 'Not key with name'})

    category = Category.query.filter_by(id=id).first()

    if not category:
        return jsonify({'message': 'Нема такої категорії'}), 404

    try:
        category.name = name  # Модель Сategory має унікальне поле name
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Така категорія існує'})

    return jsonify({'id': id, 'name': name}), 204


@api_bp.route('/category/<int:id>', methods=['DELETE'])
@protected
def delete_category(id):
    category = Category.query.get(id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({'message': 'The category has been deleted!'}), 204

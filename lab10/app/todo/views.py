from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app import db
from app.todo import todo_bp
from app.todo.forms import TaskForm, CategoryForm
from app.todo.models import Task, Category


@todo_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_task():
    form = TaskForm()
    if request.method == 'GET':
        return render_template('todo/createTask.html', form=form)

    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        deadline = form.deadline.data
        priority = form.priority.data
        category = form.category.data
        task_info = Task(title=title,
                         description=description,
                         deadline=deadline,
                         priority=priority,
                         category_id=category,
                         owner=current_user)
        db.session.add(task_info)
        db.session.commit()

        flash(f"Task successfully added", category='success')
        return redirect(url_for("todo.create_task"))

    flash("Не пройшла валідація з Post", category='warning')
    return redirect(url_for("todo.create_task"))


@todo_bp.route('/', methods=['GET'])
@login_required
def list_task():
    task_list = Task.query.filter_by(owner_id=current_user.id).all()
    return render_template('todo/listTask.html', task_list=task_list)


@todo_bp.route('/<int:task_id>', methods=['GET'])
@login_required
def detail_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    task_detail = {
        'Title': task.title,
        'Description': task.description,
        'Created': task.created,
        'Modified': task.modified,
        'Deadline': task.deadline.date(),
        'Priority': task.priority,
        'Progress': task.progress
    }
    form = TaskForm()
    return render_template('todo/detailTask.html', task_detail=task_detail, task_id=task.id, form=form)


@todo_bp.route('/<int:task_id>/update', methods=['POST'])
@login_required
def update_task(task_id):
    form = TaskForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        deadline = form.deadline.data
        priority = form.priority.data
        progress = form.progress.data

        task = Task.query.filter_by(id=task_id).first()
        task.title = title
        task.description = description
        task.deadline = deadline
        task.priority = priority
        task.progress = progress
        db.session.add(task)
        db.session.commit()

        flash(f"Task successfully updated", category='success')
        return redirect(url_for("todo.detail_task", task_id=task_id))

    flash("Не пройшла валідація з Post", category='warning')
    return redirect(url_for("todo.detail_task", task_id=task_id))


@todo_bp.route('/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    db.session.delete(task)
    db.session.commit()
    flash("Successfully deleted!", category='success')
    return redirect(url_for("todo.list_task"))


@todo_bp.route('/category/', methods=['GET'])
@login_required
def list_category():
    cat_list = Category.query.all()
    return render_template('todo/listCategory.html', cat_list=cat_list)


@todo_bp.route('/category/create', methods=['GET', 'POST'])
@login_required
def create_category():
    form = CategoryForm()
    if request.method == 'GET':
        return render_template('todo/createCategory.html', form=form)

    if form.validate_on_submit():
        name = form.name.data
        cat_info = Category(name=name)
        db.session.add(cat_info)
        db.session.commit()

        flash(f"Category successfully added", category='success')
        return redirect(url_for("todo.create_category"))

    flash("Не пройшла валідація з Post", category='warning')
    return redirect(url_for("todo.create_category"))


@todo_bp.route('/category/<int:cat_id>', methods=['GET'])
@login_required
def detail_category(cat_id):
    cat = Category.query.filter_by(id=cat_id).first()
    cat_detail = {
        'Name': cat.name,
    }
    form = CategoryForm()
    return render_template('todo/detailCategory.html', cat_detail=cat_detail, cat_id=cat.id, form=form)


@todo_bp.route('/category/<int:cat_id>/update', methods=['POST'])
@login_required
def update_category(cat_id):
    form = CategoryForm()
    if form.validate_on_submit():
        name = form.name.data

        cat = Category.query.filter_by(id=cat_id).first()
        cat.name = name
        db.session.add(cat)
        db.session.commit()

        flash(f"Category successfully updated", category='success')
        return redirect(url_for("todo.detail_category", cat_id=cat_id))

    flash("Не пройшла валідація з Post", category='warning')
    return redirect(url_for("todo.detail_category", cat_id=cat_id))


@todo_bp.route('/category/<int:cat_id>/delete', methods=['POST'])
@login_required
def delete_category(cat_id):
    cat = Category.query.filter_by(id=cat_id).first()
    db.session.delete(cat)
    db.session.commit()
    flash("Successfully deleted!", category='success')
    return redirect(url_for("todo.list_category"))

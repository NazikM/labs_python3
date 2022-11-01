from flask import Flask, render_template, request, flash, redirect, url_for, session
from datetime import datetime
import os
from forms import Myform
import logging
logging.basicConfig(filename='app.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jfklahfjhdfh'

@app.route('/')
def main():
    user_agent = request.headers.get('User-Agent')
    time = datetime.now().strftime("%H:%M:%S")
    return render_template('home.html', page=1, footer_info={'os_name': os.uname(), 'user_agent': user_agent, 'time': time})


@app.route('/about')
def about():
    user_agent = request.headers.get('User-Agent')
    time = datetime.now().strftime("%H:%M:%S")
    hobies = ("Programming", "Computer Games", "Board Games", "Tennis", "Basketball", "Reading", "Watching movies")
    return render_template('about.html', hobies=hobies, page=2, footer_info={'os_name': os.uname(), 'user_agent': user_agent, 'time': time})


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = Myform()
    if request.method == 'GET':
        now = datetime.now()
        user_agent = request.headers.get('User-Agent')
        current_time = now.strftime("%H:%M:%S")
        minute = now.strftime("%M")
        return render_template('contact.html', session=session, form=form, time=current_time, minute=minute, page=3, footer_info={'os_name': os.uname(), 'user_agent': user_agent, 'time': current_time})
    
    if form.validate_on_submit():
        username = form.name.data
        email = form.email.data
        phone = form.phone.data
        subject = form.subject.data
        message = form.message.data
        session['name'] = username
        session['email'] = email
        form.name.data = 'виконався метод post і валідація успішно'
        flash(f"Дані успішно відправлено: {username} {email}", category='success')
        logging.info(f"Дані успішно відправлено: {username} {email}")
        return redirect(url_for("contact"))

    flash("Не пройшла валідація з Post", category='warning')
    logging.warning("Не пройшла валідація з Post")
    return redirect(url_for("contact"))


@app.route('/delete_session')
def delete_email():
    session.pop('email', default=None)
    session.pop('name', default=None)
    return '<h1>Session deleted!</h1>'


if __name__ == '__main__':
    app.run()
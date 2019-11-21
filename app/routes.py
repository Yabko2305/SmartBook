# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from flask_login import current_user, login_user
import datetime
from app.models import User, Reservation, Classroom
from app import app, db
from app.forms import LoginForm , RegistrationForm, ReservationForm, PrintReservations
from flask_login import logout_user , login_required
from datetime import datetime
from app.validators import validateLength, validateTime, validate_Date, validate_delay


def validate_all(fro, to, startdate, enddate, classroom):
    returns = []
    returns.append(validate_Date(fro, to, startdate, enddate))
    returns.append(validateLength(fro, to, startdate, enddate))
    returns.append(validateTime(fro, to, startdate, enddate, classroom))
    for elem in returns:
        if elem != True:
            return elem
    return True

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/')
@app.route('/index', methods=['GET','POST'])
@login_required
def index():
    form = ReservationForm()
    if form.validate_on_submit():
        if Classroom.query.filter_by(ClassroomNum=form.classroom.data).first() == None:
            flash("No such classroom")
        else:
            inf = validate_all(form.From.data, form.To.data, form.reservationDate.data, form.endreservationDate.data,
                               Classroom.query.filter_by(ClassroomNum=form.classroom.data).first().id)
            if(inf == True):
                reservation = Reservation(user_id = current_user.id, classroom_num = form.classroom.data,
                                          classroom_id = Classroom.query.filter_by(ClassroomNum=form.classroom.data).first().id,
                                          fromTime= datetime.combine(form.reservationDate.data,form.From.data),
                                          toTime = datetime.combine(form.endreservationDate.data,form.To.data))
                db.session.add(reservation)
                db.session.commit()
                flash("New reservation added!")
            else:
                flash(inf)

    return render_template('index.html', title="Home", form=form, classrooms= Classroom.query.all())


@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, name=form.name.data, surname=form.surname.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congrats, now you are registered!")
        return redirect(url_for('login'))
    return render_template('register.html', title="Register", form=form)


@app.route('/my_reservations', methods=['GET','POST'])
@login_required
def my_reservations():
    next_page = request.args.get('action')
    if not next_page or url_parse(next_page).netloc != '':
        reser = validate_delay(current_user)
        massi = [int(i) for i in range(len(reser))]
        return render_template('reservations.html', title="My Reservations", reservs = reser, mass=massi)
    else:
        return redirect(next_page)

@app.route('/delete<num>')
@login_required
def delete(num):
    de = current_user.reservations.all()[int(num)]
    db.session.delete(de)
    db.session.commit()
    return redirect(url_for('my_reservations'))


@app.route('/edit<num>', methods=['GET','POST'])
@login_required
def edit(num):
    massi = [int(i) for i in range(len(current_user.reservations.all()))]
    massi[int(num)] = -1
    form = ReservationForm()
    reserv = Reservation.query.filter_by(user_id=current_user.id, classroom_num = (current_user.reservations.all()[int(num)]).classroom_num,
                                         fromTime=current_user.reservations.all()[int(num)].fromTime, toTime= current_user.reservations.all()[int(num)].toTime, ).first()

    if request.method=='POST':
        if Classroom.query.filter_by(ClassroomNum=form.classroom.data).first() == None:
            flash("No such classroom")
            return redirect(url_for('my_reservations'))
        else:
            inf = validate_all(form.From.data, form.To.data, form.reservationDate.data, form.endreservationDate.data,
                               Classroom.query.filter_by(ClassroomNum=form.classroom.data).first().id)
            if (inf == True):
                    reserv.classroom_num = form.classroom.data
                    reserv.classroom_id = Classroom.query.filter_by(ClassroomNum=form.classroom.data).first().id
                    reserv.fromTime = datetime.combine(form.reservationDate.data, form.From.data)
                    reserv.toTime = datetime.combine(form.endreservationDate.data, form.To.data)
                    db.session.commit()
                    return redirect(url_for('my_reservations'))
            else:
                flash(inf)
                return redirect(url_for('my_reservations'))

    elif request.method == 'GET':
        form.classroom.data = (current_user.reservations.all()[int(num)]).classroom_num
        form.reservationDate.data = current_user.reservations.all()[int(num)].fromTime.date()
        form.From.data = current_user.reservations.all()[int(num)].fromTime.time()
        form.To.data = current_user.reservations.all()[int(num)].toTime.time()
        form.endreservationDate.data = current_user.reservations.all()[int(num)].toTime.date()

        next_page = request.args.get('action')
        if not next_page:
            return render_template('reservations.html', title="Edit", reservs=current_user.reservations.all(),
                                   mass=massi, form=form, comparator=int(-1))
        else:
            if (next_page == 'cancel'):
                return redirect(url_for('my_reservations'))
            else:
                return redirect(next_page)
    return render_template('reservations.html', title="Edit", reservs=current_user.reservations.all(), mass=massi,
                           form=form, rly=int(-1))




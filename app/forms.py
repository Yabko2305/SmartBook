from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from wtforms.fields.html5 import DateField, TimeField
from app.models import User
import datetime

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    name = StringField("First name", validators=[DataRequired()])
    surname = StringField("Second name", validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat password' , validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user is not None:
            raise ValidationError("Please use a different username")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Please use a different email")

class ReservationForm(FlaskForm):
    classroom = IntegerField("Classroom to book", validators=[DataRequired()])
    reservationDate = DateField("Reservation date", validators=[DataRequired()], default=datetime.date.today())
    From = TimeField("Beggining of reservation", validators=[DataRequired()], default=datetime.time(00,00,00))
    endreservationDate = DateField("End of reservation date", validators=[DataRequired()], default=datetime.date.today())
    To = TimeField("End of reservation", validators=[DataRequired()], default=datetime.date.today())
    submit = SubmitField('Reserve')

    def validate_enddate_field(form, field):
        if field.data < form.From.data:
            raise ValidationError("End date must not be earlier than start date.")

class PrintReservations(FlaskForm):
    text = TextAreaField("")
    edit = SubmitField('Edit')
    cancel = SubmitField('Cancel')

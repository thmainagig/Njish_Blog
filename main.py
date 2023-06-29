from flask import Flask, render_template, request
from datetime import datetime
from smtplib import SMTP
import os
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, Optional

app = Flask(__name__)
year = datetime.now().year

@app.route('/')
def get_index():
    return render_template('home.html', year=year)

@app.route('/about')
def get_about():
    return render_template('about.html', year=year)

class contact_Form(FlaskForm):
    fname = StringField('First Name: ', validators=[DataRequired()])
    lname = StringField('Last Name: ', validators=[Optional()])
    email = StringField('Email Address: ', validators=[DataRequired(), Email(message='Invalid Email')])
    phone = StringField('Phone Number: ', validators=[DataRequired()])
    message = TextAreaField('Enter Message: ', validators=[DataRequired()])

@app.route('/contact', methods=['GET', 'POST'])
def get_contact():
    if request.method =='POST':
        return render_template('home.html', year=year)
    return render_template('contacts.html', year=year)

#
# @app.route('/post/<index>')
# def get_post(index):
#     return render_template()

@app.route('/index', methods=['GET', 'POST'])
def get_mail():
    if request.method == 'POST':
        data = request.form
        with SMTP('smtp.gmail.com') as smtp:
            smtp.starttls()
            smtp.login(user=os.environ.get('EMAIL'), password=os.environ.get('PASSWORD'))
            smtp.sendmail(from_addr=os.environ.get('EMAIL'), to_addrs='grvma23@yahoo.com', msg=f'Subject: Subscriber: \n\n{data["mail"]}')
        return render_template('index.html', year=year)

class loginForm(FlaskForm):
    name = StringField('Username: ', validators=[DataRequired(), Email(message='Email Invalid')])
    password = PasswordField('Password: ', validators=[DataRequired()])
    def validate_password(form, field):
        if len(field.data)<8:
            raise ValidationError('Password must be more than 8 characters')
    submit = SubmitField('Sign In')

@app.route('/dashboard', methods=['GET', 'POST'])
def get_admin():
    form = loginForm(meta={'csrf': False})
    if form.validate_on_submit():
        if form.name.data == 'admin@email.com' and form.password.data == '12345678097':
            return render_template('about.html', year=year)
        else:
            error = 'Invalid Credentials'
            return render_template('base.html', year=year)
    app.secret_key = 'Kenya-Langamberia_Soysambu'
    return render_template('login.html', year=year, form=form)

if __name__ == "__main__":
    app.run(debug=True)
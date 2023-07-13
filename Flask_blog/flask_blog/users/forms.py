from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flask_blog.models import User

class RegistrationForm(FlaskForm):
    username = StringField('username',
                            validators=[DataRequired(), Length(min=2, max=20)]) # Here we add the 'dataRequired()' to make sure that the username is not empty, and the 'length()' to specific how long the username can get
    email = StringField('Email', validators=[DataRequired(), Email()])# Same thing here the 'dataRequired()' to make sure its not ignored, and the 'Email()' to make sure its an format
    password = PasswordField('Password', validators=[DataRequired()]) # The name before the validator is called the label for this field.....same for the ones above too
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username): # This method is to check if username has been taken
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is taken. Please choose a different one !')
        
    def validate_email(self, email):# This method is to check if email has been taken
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email is taken. Please choose a different one !')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])# Same thing here the 'dataRequired()' to make sure its not ignored, and the 'Email()' to make sure its an format
    password = PasswordField('Password', validators=[DataRequired()]) # The name before the validator is called the label for this field.....same for the ones above too
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('username',
                            validators=[DataRequired(), Length(min=2, max=20)]) # Here we add the 'dataRequired()' to make sure that the username is not empty, and the 'length()' to specific how long the username can get
    email = StringField('Email', validators=[DataRequired(), Email()])# Same thing here the 'dataRequired()' to make sure its not ignored, and the 'Email()' to make sure its an format
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username): # This method is to check if username has been taken
        if username.data != current_user.username: # This is to check if user changes there email.....If so, it checks if it doesnt exist before
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username is taken. Please choose a different one !')
        
    def validate_email(self, email):# This method is to check if email has been taken
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email is taken. Please choose a different one !')
            

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])# Same thing here the 'dataRequired()' to make sure its not ignored, and the 'Email()' to make sure its an format
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):# This method is to check if email has been taken
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with this email, You must register first!')
        

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()]) # The name before the validator is called the label for this field.....same for the ones above too
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from flask_login import current_user
from blog.models import User
from flask_wtf.file import FileField,FileAllowed

class Registrationform(FlaskForm):
	username=StringField('Username',
			validators=[DataRequired(),Length(min=2,max=20)])
	email=StringField('Email',
			validators=[DataRequired(),Email()])
	password=PasswordField('Password',
			validators=[DataRequired(),Length(min=5,max=20)])
	confirm_password=PasswordField('Confirm Password',
			validators=[DataRequired(),EqualTo('password')])
	submit=SubmitField('Sign Up')


class AccountForm(FlaskForm):
	username=StringField('Username',
			validators=[DataRequired(),Length(min=2,max=20)])
	email=StringField('Email',
			validators=[DataRequired(),Email()])
	picture=FileField('Update profile pic',validators=[FileAllowed(['jpg','jpeg','png','JPG','JPEG','PNG'])])
	submit=SubmitField('Update')
	def validate_username(self,username):
		if current_user.username!=username.data:
			user=User.query.filter_by(username='username').first()
			if user:
				raise ValidationError('username is taken')
	def validate_email(self,email):
		if current_user.email!=email.data:
			email_user=User.query.filter_by(email='email').first()
			if email_user:
				raise ValidationError('email is taken')





class Loginform(FlaskForm):
	
	email=StringField('Email',
			validators=[DataRequired(),Email()])
	password=PasswordField('Password',
			validators=[DataRequired(),Length(min=5,max=20)])
	
	
	submit=SubmitField('Sign In')


class CreatePost(FlaskForm):
	Title=StringField('Title',validators=[DataRequired()])
	Content=TextAreaField('Content',validators=[DataRequired()])
	submit=SubmitField('Post')

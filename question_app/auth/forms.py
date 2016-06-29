# coding:utf-8
from flask.ext.wtf import Form

from wtforms import StringField, PasswordField, BooleanField, SubmitField

from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

class RegisterForm(Form):
	email = StringField('Email', validators=[Required(), Length(1,64), Email()])
	username = StringField('username', validators=[Required(), Length(1, 64),\
	 	Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Usernames must have only letters, numbers, dots or underscores')])
	password = PasswordField('password', validators=[Required(), EqualTo('password2', message="Please must match.")])
	password2 = PasswordField('Confirm password', validators=[Required()])
	submit = SubmitField(u'注册')
	
	def validate_email(self, field):
		if User.objects(email=field.data).first():
			raise ValidationError('Email already Register.')
	
	def validate_username(self, field):
		if User.objects(name=field.data).first():
			raise ValidationError("Username already in use")
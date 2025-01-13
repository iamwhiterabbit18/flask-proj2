from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

class RegisterForm(FlaskForm):
  username = StringField('username', validators=[
    InputRequired(),
    Length(min=4, max=15)
  ], render_kw={"placeholder": "Username"})
  password = PasswordField('password', validators=[
    InputRequired(),
    Length(min=4, max=15)
  ], render_kw={"placeholder": "Password"})
  submit = SubmitField('Sign Up')

  def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user is not None:
      raise ValidationError('Please use a different username.')

class LoginForm(FlaskForm):
  username = StringField('username', validators=[
    InputRequired(),
    Length(min=4, max=15)
  ], render_kw={"placeholder": "Username"})
  password = PasswordField('password', validators=[
    InputRequired(),
    Length(min=4, max=15)
  ], render_kw={"placeholder": "Password"})
  submit = SubmitField('Login')
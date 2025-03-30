from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email


class ContactForm(FlaskForm):
    """Contact form"""
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[Email(message='Not a valid email address.'), DataRequired()])
    body = TextAreaField('Message', validators=[DataRequired(), Length(min=4, message='Your message is too short.')])
    # recaptcha = RecaptchaField()
    submit = SubmitField('Submit')

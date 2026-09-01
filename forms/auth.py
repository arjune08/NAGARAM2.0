"""
NAGARAM — Authentication Forms
Login, registration, and profile forms.
"""
from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SelectField, BooleanField,
    TextAreaField, SubmitField
)
from wtforms.validators import (
    DataRequired, Email, Length, EqualTo, ValidationError, Optional
)
from app.models.user import User


class LoginForm(FlaskForm):
    """User login form."""
    login = StringField('Email or Username', validators=[
        DataRequired(message='Please enter your email or username.')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Please enter your password.')
    ])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    """User registration form with role selection."""
    full_name = StringField('Full Name', validators=[
        DataRequired(), Length(min=2, max=150)
    ])
    username = StringField('Username', validators=[
        DataRequired(), Length(min=3, max=80)
    ])
    email = StringField('Email Address', validators=[
        DataRequired(), Email()
    ])
    phone = StringField('Phone Number', validators=[
        Optional(), Length(max=20)
    ])
    role = SelectField('Register As', choices=[
        ('citizen', 'Citizen'),
        ('farmer', 'Farmer'),
        ('expert', 'Expert'),
        ('ngo', 'NGO / Organization'),
        ('volunteer', 'Volunteer'),
    ], validators=[DataRequired()])
    location = StringField('Location / City', validators=[
        Optional(), Length(max=200)
    ])
    district = StringField('District', validators=[
        Optional(), Length(max=100)
    ])
    state = SelectField('State', choices=[
        ('', 'Select State'),
        ('Andhra Pradesh', 'Andhra Pradesh'),
        ('Arunachal Pradesh', 'Arunachal Pradesh'),
        ('Assam', 'Assam'),
        ('Bihar', 'Bihar'),
        ('Chhattisgarh', 'Chhattisgarh'),
        ('Goa', 'Goa'),
        ('Gujarat', 'Gujarat'),
        ('Haryana', 'Haryana'),
        ('Himachal Pradesh', 'Himachal Pradesh'),
        ('Jharkhand', 'Jharkhand'),
        ('Karnataka', 'Karnataka'),
        ('Kerala', 'Kerala'),
        ('Madhya Pradesh', 'Madhya Pradesh'),
        ('Maharashtra', 'Maharashtra'),
        ('Manipur', 'Manipur'),
        ('Meghalaya', 'Meghalaya'),
        ('Mizoram', 'Mizoram'),
        ('Nagaland', 'Nagaland'),
        ('Odisha', 'Odisha'),
        ('Punjab', 'Punjab'),
        ('Rajasthan', 'Rajasthan'),
        ('Sikkim', 'Sikkim'),
        ('Tamil Nadu', 'Tamil Nadu'),
        ('Telangana', 'Telangana'),
        ('Tripura', 'Tripura'),
        ('Uttar Pradesh', 'Uttar Pradesh'),
        ('Uttarakhand', 'Uttarakhand'),
        ('West Bengal', 'West Bengal'),
        ('Delhi', 'Delhi'),
        ('Puducherry', 'Puducherry'),
    ], validators=[Optional()])
    password = PasswordField('Password', validators=[
        DataRequired(), Length(min=6, message='Password must be at least 6 characters.')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password', message='Passwords must match.')
    ])
    submit = SubmitField('Create Account')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('This username is already taken.')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('This email is already registered.')


class ProfileForm(FlaskForm):
    """Edit profile form."""
    full_name = StringField('Full Name', validators=[
        DataRequired(), Length(min=2, max=150)
    ])
    phone = StringField('Phone Number', validators=[
        Optional(), Length(max=20)
    ])
    location = StringField('Location', validators=[
        Optional(), Length(max=200)
    ])
    district = StringField('District', validators=[
        Optional(), Length(max=100)
    ])
    state = StringField('State', validators=[
        Optional(), Length(max=100)
    ])
    pincode = StringField('Pincode', validators=[
        Optional(), Length(max=10)
    ])
    submit = SubmitField('Update Profile')


class ChangePasswordForm(FlaskForm):
    """Change password form."""
    current_password = PasswordField('Current Password', validators=[
        DataRequired()
    ])
    new_password = PasswordField('New Password', validators=[
        DataRequired(), Length(min=6)
    ])
    confirm_password = PasswordField('Confirm New Password', validators=[
        DataRequired(), EqualTo('new_password')
    ])
    submit = SubmitField('Change Password')

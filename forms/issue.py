"""
NAGARAM — Issue Forms
Forms for creating, updating, filtering, and commenting on issues.
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField, TextAreaField, SelectField, FloatField,
    MultipleFileField, SubmitField, HiddenField
)
from wtforms.validators import DataRequired, Length, Optional, NumberRange


class CivicIssueForm(FlaskForm):
    """Form for citizens to report civic issues."""
    title = StringField('Issue Title', validators=[
        DataRequired(), Length(min=5, max=300)
    ])
    category_id = SelectField('Category', coerce=int, validators=[
        DataRequired()
    ])
    description = TextAreaField('Description', validators=[
        DataRequired(), Length(min=20, max=5000)
    ])
    location = StringField('Location / Address', validators=[
        DataRequired(), Length(max=300)
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
    latitude = HiddenField('Latitude')
    longitude = HiddenField('Longitude')
    priority = SelectField('Priority', choices=[
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ], default='Medium')
    images = MultipleFileField('Upload Evidence (Images)', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'],
                     'Only image files are allowed.')
    ])
    submit = SubmitField('Submit Issue')


class AgriculturalIssueForm(FlaskForm):
    """Form for farmers to report agricultural issues."""
    title = StringField('Issue Title', validators=[
        DataRequired(), Length(min=5, max=300)
    ])
    category_id = SelectField('Category', coerce=int, validators=[
        DataRequired()
    ])
    description = TextAreaField('Describe the Problem', validators=[
        DataRequired(), Length(min=20, max=5000)
    ])
    crop_name = StringField('Affected Crop', validators=[
        Optional(), Length(max=100)
    ])
    affected_area = FloatField('Affected Area (Acres)', validators=[
        Optional(), NumberRange(min=0)
    ])
    farm_id = SelectField('Farm', coerce=int, validators=[
        Optional()
    ])
    location = StringField('Location', validators=[
        DataRequired(), Length(max=300)
    ])
    district = StringField('District', validators=[
        Optional(), Length(max=100)
    ])
    latitude = HiddenField('Latitude')
    longitude = HiddenField('Longitude')
    priority = SelectField('Priority', choices=[
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ], default='Medium')
    images = MultipleFileField('Upload Images', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'],
                     'Only image files are allowed.')
    ])
    submit = SubmitField('Submit Issue')


class IssueUpdateForm(FlaskForm):
    """Form for updating issue status."""
    status = SelectField('Status', choices=[
        ('Submitted', 'Submitted'),
        ('Under Review', 'Under Review'),
        ('Assigned', 'Assigned'),
        ('In Progress', 'In Progress'),
        ('Waiting for Information', 'Waiting for Information'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
    ], validators=[DataRequired()])
    message = TextAreaField('Update Message', validators=[
        Optional(), Length(max=2000)
    ])
    resolution = TextAreaField('Resolution Details', validators=[
        Optional(), Length(max=5000)
    ])
    submit = SubmitField('Update Issue')


class IssueAssignForm(FlaskForm):
    """Form for assigning issues."""
    assigned_to_id = SelectField('Assign To', coerce=int, validators=[
        DataRequired()
    ])
    notes = TextAreaField('Assignment Notes', validators=[
        Optional(), Length(max=1000)
    ])
    submit = SubmitField('Assign')


class CommentForm(FlaskForm):
    """Form for adding comments to issues."""
    content = TextAreaField('Comment', validators=[
        DataRequired(), Length(min=2, max=2000)
    ])
    submit = SubmitField('Add Comment')


class IssueFilterForm(FlaskForm):
    """Filter form for issue lists."""
    class Meta:
        csrf = False

    search = StringField('Search', validators=[Optional()])
    category = SelectField('Category', coerce=int, validators=[Optional()],
                           choices=[(0, 'All Categories')])
    status = SelectField('Status', validators=[Optional()], choices=[
        ('', 'All Statuses'),
        ('Submitted', 'Submitted'),
        ('Under Review', 'Under Review'),
        ('Assigned', 'Assigned'),
        ('In Progress', 'In Progress'),
        ('Waiting for Information', 'Waiting for Information'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
    ])
    priority = SelectField('Priority', validators=[Optional()], choices=[
        ('', 'All Priorities'),
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ])
    sort = SelectField('Sort By', validators=[Optional()], choices=[
        ('newest', 'Newest First'),
        ('oldest', 'Oldest First'),
        ('priority', 'Priority'),
        ('status', 'Status'),
    ])

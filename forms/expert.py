"""
NAGARAM — Expert & NGO Forms
Forms for expert diagnosis and NGO workflows.
"""
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, Optional, NumberRange


class DiagnosisForm(FlaskForm):
    """Form for expert to diagnose and recommend."""
    diagnosis = TextAreaField('Diagnosis', validators=[
        DataRequired(), Length(min=10, max=5000)
    ])
    recommendation = TextAreaField('Recommendation', validators=[
        DataRequired(), Length(min=10, max=5000)
    ])
    expert_notes = TextAreaField('Internal Notes (not visible to farmer)', validators=[
        Optional(), Length(max=3000)
    ])
    submit = SubmitField('Submit Diagnosis')


class ExpertResponseForm(FlaskForm):
    """Form for expert to respond to consultation."""
    diagnosis = TextAreaField('Diagnosis / Analysis', validators=[
        DataRequired(), Length(min=10, max=5000)
    ])
    recommendation = TextAreaField('Recommendation', validators=[
        DataRequired(), Length(min=10, max=5000)
    ])
    status = SelectField('Status', choices=[
        ('Answered', 'Answered'),
        ('Follow-up', 'Needs Follow-up'),
    ], validators=[DataRequired()])
    submit = SubmitField('Send Response')


class FarmerFeedbackForm(FlaskForm):
    """Form for farmer to provide feedback on consultation."""
    farmer_feedback = TextAreaField('Your Feedback', validators=[
        Optional(), Length(max=2000)
    ])
    farmer_rating = IntegerField('Rating (1-5)', validators=[
        Optional(), NumberRange(min=1, max=5)
    ])
    submit = SubmitField('Submit Feedback')


class NGOUpdateForm(FlaskForm):
    """Form for NGO to update issue progress."""
    message = TextAreaField('Update Message', validators=[
        DataRequired(), Length(min=5, max=3000)
    ])
    status = SelectField('Status', choices=[
        ('In Progress', 'In Progress'),
        ('Waiting for Information', 'Waiting for Information'),
        ('Resolved', 'Resolved'),
    ], validators=[DataRequired()])
    submit = SubmitField('Post Update')

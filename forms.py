from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField,
                     TextAreaField, SelectField, ColorField)
from wtforms.validators import DataRequired, Email, Length, Optional

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit   = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email    = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    role     = SelectField('Role', choices=[('analyst','Analyst'),('viewer','Viewer')], default='analyst')
    submit   = SubmitField('Register')

class NewCallForm(FlaskForm):
    target_number   = StringField('Target Phone Number (+E.164)', validators=[DataRequired()])
    scammer_persona = TextAreaField('Scammer Persona Prompt (optional)',
                                    render_kw={'rows': 5,
                                               'placeholder': 'Describe the scammer persona… leave blank for default PPP fraud narrative.'})
    submit = SubmitField('Initiate Call')

class DashboardSettingsForm(FlaskForm):
    dashboard_title = StringField('Dashboard Title',     validators=[Optional(), Length(max=100)])
    logo_text       = StringField('Logo / Brand Text',   validators=[Optional(), Length(max=20)])
    primary_color   = StringField('Primary Color (hex)', validators=[Optional()], default='#0d6efd')
    accent_color    = StringField('Accent Color (hex)',  validators=[Optional()], default='#198754')
    bg_color        = StringField('Background Color',    validators=[Optional()], default='#121212')
    card_color      = StringField('Card Color',          validators=[Optional()], default='#1e1e2e')
    text_color      = StringField('Text Color',          validators=[Optional()], default='#e0e0e0')
    submit = SubmitField('Save Settings')

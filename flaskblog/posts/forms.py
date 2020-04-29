from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField,SelectField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField,DecimalRangeField
from wtforms_components import DateRange
from datetime import date


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    type = SelectField('Help Type', choices=[('',''),('Food/Other Necessities','Food/Other Necessities'),('Housing/Shelter','Housing/Shelter'),('Medical/Mental Health','Medical/Mental Health'),
                                                ('Utility Services','Utility Services'),('Youth/Child Care','Youth/Child Care'),('Older Care','Older Care'),('Other Support','Other Support')], validators=[DataRequired()])
    sdate=DateField('from',format='%Y-%m-%d',validators=[DataRequired('Please select startdate')])
    fdate=DateField('to',format='%Y-%m-%d',validators=[DataRequired()])
    phonember = StringField('Phone Number', validators=[DataRequired()])
    emailaddress = StringField('Email Address', validators=[DataRequired()])
    address = StringField('Address or Zip Code', validators=[DataRequired()])
    content = TextAreaField('What is your specific request?', validators=[DataRequired()])
    submit = SubmitField('Post')

class SearchForm(FlaskForm):
    location=StringField('Your Location',validators=[DataRequired()])
    type=SelectField('Help Type', choices=[('All','All'),('Food/Other Necessities','Food/Other Necessities'),('Housing/Shelter','Housing/Shelter'),('Medical/Mental Health','Medical/Mental Health'),
                                                ('Utility Services','Utility Services'),('Youth/Child Care','Youth/Child Care'),('Older Care','Older Care'),('Other Support','Other Support')], validators=[DataRequired()])

    sdate = DateField('from', format='%Y-%m-%d', validators=[DataRequired('Please select startdate')])
    fdate = DateField('to', format='%Y-%m-%d', validators=[DataRequired()])
    distance=DecimalRangeField('Select Distance', default=1,rounding=1)
    submit = SubmitField('Search')

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired

class new_ingredient_form( FlaskForm ):
    name = StringField( 'Name', validators=[DataRequired()] )
    search = StringField( 'Search Term', validators=[DataRequired()] )
    quantity = IntegerField( 'Quantity', validators=[DataRequired()] )
    unit = StringField( 'Unit', validators=[DataRequired()] )
    submit = SubmitField( 'Add Ingredient' )

class delete_ingredient_form( FlaskForm ):
    submit = SubmitField( 'Delete' )

class add_to_recipe_form( FlaskForm ):
    select = SelectField( 'Ingredient' )
    quantity = IntegerField( 'Quantity', validators=[DataRequired()] )
    unit = StringField( 'Unit', validators=[DataRequired()] )
    submit = SubmitField( 'Add Ingredient' )
    
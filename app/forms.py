from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, HiddenField
from wtforms.validators import DataRequired

class ingredient_form( FlaskForm ):
    name = StringField( 'Name', validators=[DataRequired()] )
    search = StringField( 'Search Term', validators=[DataRequired()] )
    quantity = IntegerField( 'Quantity', validators=[DataRequired()] )
    unit = StringField( 'Unit', validators=[DataRequired()] )
    submit = SubmitField( 'Add Ingredient' )

class selected_ingredient_form( FlaskForm ):
    select = SelectField( 'Ingredient' )
    quantity = IntegerField( 'Quantity', validators=[DataRequired()] )
    unit = StringField( 'Unit', validators=[DataRequired()] )
    submit = SubmitField( 'Add Ingredient' )

class selected_recipe_form( FlaskForm ):
    select = SelectField( 'Recipe' )
    submit = SubmitField( 'Add Recipe' )

class delete_form( FlaskForm ):
    submit = SubmitField( 'Delete' )
    id = HiddenField('hidden_id')

class add_to_recipe_form( FlaskForm ):
    select = SelectField( 'Ingredient' )
    quantity = IntegerField( 'Quantity', validators=[DataRequired()] )
    unit = StringField( 'Unit', validators=[DataRequired()] )
    submit = SubmitField( 'Add Ingredient' )
    
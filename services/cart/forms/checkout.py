"""
forms/checkout.py ─ Shipping address form used at checkout.
"""

from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Length


class CheckoutForm(FlaskForm):
    shipping_name = StringField(
        "Full Name",
        validators=[DataRequired(), Length(max=150)],
    )
    shipping_email = StringField(
        "Email",
        validators=[DataRequired(), Length(max=150)],
    )
    shipping_address = StringField(
        "Street Address",
        validators=[DataRequired(), Length(max=300)],
    )
    shipping_city = StringField(
        "City",
        validators=[DataRequired(), Length(max=100)],
    )
    shipping_state = StringField(
        "State / Province",
        validators=[DataRequired(), Length(max=100)],
    )
    shipping_zip = StringField(
        "ZIP / Postal Code",
        validators=[DataRequired(), Length(max=20)],
    )
    shipping_country = SelectField(
        "Country",
        choices=[
            ("US", "United States"),
            ("CA", "Canada"),
            ("GB", "United Kingdom"),
            ("AU", "Australia"),
        ],
        default="US",
        validators=[DataRequired()],
    )
    submit = SubmitField("Place Order")

from enum import Enum
from flask_wtf import FlaskForm
from wtforms import (
    FloatField,
    SelectField,
    TextAreaField,
    SubmitField,
    IntegerField,
    StringField,
    HiddenField
)
from wtforms.validators import DataRequired


class Currency(Enum):
    EUR = 978
    USD = 840
    RUB = 643


CURRENCY_CHOICES = [(currency.value, currency.name) for currency in Currency]


class BasePaymentForm(FlaskForm):
    amount = FloatField('Amount', validators=[DataRequired()])
    currency = SelectField('Currency', validators=[DataRequired()],
                           choices=CURRENCY_CHOICES, coerce=int)
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Pay')


class PayMethodForm(BasePaymentForm):
    shop_id = IntegerField('shop_id', validators=[DataRequired()])
    sign = StringField('sign', validators=[DataRequired()])
    shop_order_id = StringField('shop_order_id', validators=[DataRequired()])
    submit = SubmitField('Continue')


class InvoiceMethodForm(FlaskForm):
    lang = HiddenField(validators=[DataRequired()])
    m_curorderid = HiddenField(validators=[DataRequired()])
    m_historyid = HiddenField(validators=[DataRequired()])
    m_historytm = HiddenField(validators=[DataRequired()])
    referer = HiddenField(validators=[DataRequired()])
    submit = SubmitField('Continue')

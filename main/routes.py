import uuid
import logging
from flask import render_template, redirect, flash
from . import app, piastrix, db
from .exceptions import PiastrixApiException
from .forms import BasePaymentForm, PayMethodForm, InvoiceMethodForm,  Currency
from .models import Payment


@app.route('/', methods=['GET', 'POST'])
def home():
    form = BasePaymentForm()

    if form.validate_on_submit():
        shop_order_id = str(uuid.uuid4())
        amount = form.amount.data
        currency = form.currency.data
        description = form.description.data

        if currency == Currency.EUR.value:
            form_data, url = piastrix.pay(amount=amount, currency=currency,
                                          description=description,
                                          shop_order_id=shop_order_id)

            payment = Payment(shop_order_id=shop_order_id, amount=amount,
                              currency=currency, description=description)
            db.session.add(payment)
            db.session.commit()

            new_form = PayMethodForm(data=form_data)
            return render_template('pay.html', form=new_form, url=url)
        elif currency == Currency.USD.value:
            try:
                data = piastrix.bill(shop_amount=amount,
                                     shop_currency=currency,
                                     payer_currency=currency,
                                     shop_order_id=shop_order_id,
                                     description=description)
            except PiastrixApiException as err:
                flash('Something went wrong. Please try again later', 'danger')
                logging.warning(f"Failed to create bill: {err}")
                return render_template('home.html', form=form)

            payment = Payment(shop_order_id=shop_order_id, amount=amount,
                              currency=currency, description=description)
            db.session.add(payment)
            db.session.commit()

            return redirect(data['url'])
        elif currency == Currency.RUB.value:
            try:
                data = piastrix.invoice(amount=amount,
                                        currency=currency,
                                        shop_order_id=shop_order_id)
            except PiastrixApiException as err:
                flash('Something went wrong. Please try again later', 'danger')
                logging.warning(f"Failed to create invoice: {err}")
                return render_template('home.html', form=form)

            payment = Payment(shop_order_id=shop_order_id, amount=amount,
                              currency=currency, description=description)
            db.session.add(payment)
            db.session.commit()

            new_form = InvoiceMethodForm(data=data['data'])
            return render_template('invoice.html', form=new_form,
                                   url=data['url'], method=data['method'])

    return render_template('home.html', form=form)

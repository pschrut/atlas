from app.enums import NodeNames
from app.utils import sanitize_xml, convert_to_float, convert_date, get_type, get_month_range, get_month_description, format_float
from lxml import etree
from flask import request, jsonify
from flask_login import login_required, current_user
from app.models import Transaction, Period, User
from app import db

def process_period(period_code):
    period_query = Period.query.filter_by(user_id=current_user.id, code=period_code).first()

    if period_query is None:
        startDate = get_month_range(period_code)['first_day']
        endDate = get_month_range(period_code)['last_day']
        period_description = get_month_description(period_code)
        period = Period(code=period_code, description=period_description, startDate=startDate, endDate=endDate, user_id=current_user.id)
        db.session.add(period)
        db.session.commit()
    else:
        period = period_query

    return period

def process_movement(movement):
    value = movement.find(NodeNames.VALOR.value)

    if value is not None:
        if movement_exists(movement):
            return
        
        date = movement.find(NodeNames.FECHA.value).text
        description = movement.find(NodeNames.DESCRIPCION.value).text
        value = convert_to_float(value.text)
        transaction_type = get_type(value)
        period_code = convert_date(date)

        period = process_period(period_code)

        transaction = Transaction(period_id=period.id, user_id=current_user.id, date=date, description=description, value=abs(value), type=transaction_type, comments=None)
        db.session.add(transaction)
        db.session.commit()

def movement_exists(movement):
    date = movement.find(NodeNames.FECHA.value).text
    description = movement.find(NodeNames.DESCRIPCION.value).text
    value = format_float(convert_to_float(movement.find(NodeNames.VALOR.value).text))

    transaction = Transaction.query.filter(Transaction.user_id == current_user.id, Transaction.date == date, Transaction.description == description, Transaction.value == abs(value)).first()

    return transaction is not None

@login_required
def upload_transactions():
    try:
        files = request.files.getlist('file')
        counter = 0

        for file_storage in files:
            xml_content = sanitize_xml(file_storage)
            root = etree.fromstring(xml_content)

            for movement in root.findall(NodeNames.MOVIMIENTO.value):
                process_movement(movement)
                counter += 1
            
        return jsonify({ 'status': 'success', 'transactions_counter': counter }), 200
    except KeyError:
        return jsonify({'error': 'File not found in request'}), 400
    except etree.XMLSyntaxError as e:
        return jsonify({'error': 'Could not parse XML', 'details': str(e)}), 400

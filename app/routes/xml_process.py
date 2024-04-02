from app.enums import NodeNames
from app.utils import sanitize_xml, convert_to_float, convert_date, get_type, get_month_range, get_month_description, format_float
from lxml import etree
from flask import request, jsonify
from flask_login import login_required, current_user
from app.models import Transaction, Period, User
from app import db, app

def process_movement(movement):
    value = movement.find(NodeNames.VALOR.value)

    if value is not None:
        if movement_exists(movement):
            return
        
        date = movement.find(NodeNames.FECHA.value).text
        description = movement.find(NodeNames.DESCRIPCION.value).text
        value = convert_to_float(value.text)
        transaction_type = get_type(value)
        period_id = convert_date(date)

        period_query = Period.query.filter(Period.id == period_id).first()

        if period_query is None:
            startDate = get_month_range(period_id)['first_day']
            endDate = get_month_range(period_id)['last_day']
            period_description = get_month_description(period_id)
            period = Period(id=period_id, description=period_description, startDate=startDate, endDate=endDate)
            db.session.add(period)
            db.session.commit()

        transaction = Transaction(period_id=period_id, user_id=current_user.id, date=date, description=description, value=abs(value), type=transaction_type, comments=None)
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

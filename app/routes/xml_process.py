from app.enums import NodeNames
from app.utils import sanitize_xml, convert_to_float, convert_date, get_type, get_month_range
from lxml import etree
from flask import request, jsonify
from app.models import Transaction, Period, User
from app import db

def process_movement(movement):
    value = movement.find(NodeNames.VALOR.value)

    if value is not None:
        date = movement.find(NodeNames.FECHA.value).text
        description = movement.find(NodeNames.DESCRIPCION.value).text
        value = convert_to_float(value.text)
        transaction_type = get_type(value)
        period_id = convert_date(date)

        period_query = Period.query.filter(Period.id == period_id).first()

        if period_query is None:
            startDate = get_month_range(period_id)['first_day']
            endDate = get_month_range(period_id)['last_day']
            period = Period(id=period_id, description=None, startDate=startDate, endDate=endDate)
            db.session.add(period)
            db.session.commit()

        transaction = Transaction(period_id=period_id, user_id=1, date=date, description=description, value=abs(value), type=transaction_type, comments=None)
        db.session.add(transaction)
        db.session.commit()

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
            
        success_message = f"Success - {counter} transactions processed."
        return jsonify({ 'message': success_message }), 200
    except KeyError:
        return jsonify({'error': 'File not found in request'}), 400
    except etree.XMLSyntaxError as e:
        return jsonify({'error': 'Could not parse XML', 'details': str(e)}), 400
    
def test_endpoint():
    query = User.query.first()
    return jsonify({ 'message': query.id }), 200
from ..db import get_db_connection, close_db_connection
from ..enums import TransactionType, NodeNames
from ..utils import sanitize_xml, convert_to_float
from lxml import etree
from flask import request, jsonify

def process_movement(movement, cursor):
    value = movement.find(NodeNames.VALOR.value)

    if value is not None:
        date = movement.find(NodeNames.FECHA.value).text
        description = movement.find(NodeNames.DESCRIPCION.value).text
        value = convert_to_float(value.text)
        transaction_type = TransactionType.INCOME.value if float(value) < 0 else TransactionType.OUTCOME.value

        query = "INSERT INTO transactions (period_id, user_id, date, description, value, type, comments) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (1, 1, date, description, value, transaction_type, None))

def upload_transactions():
    try:
        file_storage = request.files['file']
        xml_content = sanitize_xml(file_storage)
        root = etree.fromstring(xml_content)
        counter = 0

        with get_db_connection() as db, db.cursor() as cursor:
            for movement in root.findall(NodeNames.MOVIMIENTO.value):
                process_movement(movement, cursor)
                counter += 1

            db.commit()

        close_db_connection(db)
        
        success_message = f"Success - {counter} transactions processed."
        return jsonify({ 'message': success_message }), 200
    except KeyError:
        return jsonify({'error': 'File not found in request'}), 400
    except etree.XMLSyntaxError as e:
        return jsonify({'error': 'Could not parse XML', 'details': str(e)}), 400
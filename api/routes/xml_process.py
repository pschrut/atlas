from api.db import get_db_connection, close_db_connection
from api.enums import NodeNames
from api.utils import sanitize_xml, convert_to_float, convert_date, get_type, get_month_range
from lxml import etree
from flask import request, jsonify

def process_movement(movement, cursor):
    value = movement.find(NodeNames.VALOR.value)

    if value is not None:
        date = movement.find(NodeNames.FECHA.value).text
        description = movement.find(NodeNames.DESCRIPCION.value).text
        value = convert_to_float(value.text)
        transaction_type = get_type(value)
        period_id = convert_date(date)

        cursor.execute('SELECT COUNT(id) FROM periods WHERE id = %s', (period_id,))
        period = cursor.fetchone()[0]

        if period == 0:
            startDate = get_month_range(period_id)['first_day']
            endDate = get_month_range(period_id)['last_day']
            cursor.execute('INSERT INTO periods (id, description, startDate, endDate) VALUES (%s, %s, %s, %s)', (period_id, None, startDate, endDate,))

        query = "INSERT INTO transactions (period_id, user_id, date, description, value, type, comments) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (period_id, 1, date, description, abs(value), transaction_type, None))

def upload_transactions():
    try:
        files = request.files.getlist('file')
        counter = 0

        for file_storage in files:
            xml_content = sanitize_xml(file_storage)
            root = etree.fromstring(xml_content)

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
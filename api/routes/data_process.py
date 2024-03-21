from api.db import get_db_connection, close_db_connection
from api.enums import TransactionType
from flask import jsonify, request

def transactions():
    with get_db_connection() as db, db.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT id, description, value, type, date FROM transactions")
        rows = cursor.fetchall()

        close_db_connection(db)

        return jsonify({ 'rows': rows }), 200

def balance():
    period_id = request.args.get('period_id')
    year = request.args.get('year')

    with get_db_connection() as db, db.cursor(dictionary=True) as cursor:
        query = 'SELECT value, type, comments FROM transactions'
        if period_id:
            query += f' WHERE period_id = {period_id}'
        elif year:
            query += f' WHERE period_id LIKE "%{year}"'

        cursor.execute(query)
        rows = cursor.fetchall()

        close_db_connection(db)

        balance_in, balance_out, investments_in, investments_out, others = 0, 0, 0, 0, 0

        for row in rows:
            if row['type'] == TransactionType.INCOME.value:
                balance_in += float(row['value'])
            elif row['type'] == TransactionType.OUTCOME.value:
                balance_out += float(row['value'])
            elif row['type'] == TransactionType.INVESTMENT_IN.value:
                investments_in += float(row['value'])
            elif row['type'] == TransactionType.INVESTMENT_OUT.value:
                investments_out += float(row['value'])
            else:
                others += float(row['value'])

        return jsonify({
            'balance_in': round(balance_in, 2),
            'balance_out': round(balance_out, 2),
            'io_balance': round(balance_in - balance_out, 2),
            'investments_in': round(investments_in, 2),
            'investments_out': round(investments_out, 2),
            'investments_balance': round(investments_in - investments_out, 2),
            'others': round(others, 2)
        }), 200

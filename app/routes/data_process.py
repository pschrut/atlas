from app.enums import TransactionType
from flask import jsonify, request
from app.models import Transaction
from app import db

def transactions():
    query = Transaction.query.all()
    transactions = [transaction.to_json() for transaction in query]

    return jsonify({ 'txs': transactions }), 200

def balance():
    period_id = request.args.get('period_id')
    year = request.args.get('year')

    query = Transaction.query

    if period_id:
        query = query.filter(Transaction.period_id == period_id)
    if year:
        query = query.filter(Transaction.period_id.like(f'%{year}'))

    transactions = query.all()

    balance_in, balance_out, investments_in, investments_out, others = 0, 0, 0, 0, 0
    for row in transactions:
        if row.type == TransactionType.INCOME.value:
            balance_in += float(row.value)
        elif row.type == TransactionType.OUTCOME.value:
            balance_out += float(row.value)
        elif row.type == TransactionType.INVESTMENT_IN.value:
            investments_in += float(row.value)
        elif row.type == TransactionType.INVESTMENT_OUT.value:
            investments_out += float(row.value)
        else:
            others += float(row.value)

    return jsonify({
        'balance_in': round(balance_in, 2),
        'balance_out': round(balance_out, 2),
        'io_balance': round(balance_in - balance_out, 2),
        'investments_in': round(investments_in, 2),
        'investments_out': round(investments_out, 2),
        'investments_balance': round(investments_in - investments_out, 2),
        'others': round(others, 2)
    }), 200

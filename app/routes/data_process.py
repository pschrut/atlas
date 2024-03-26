from app.enums import TransactionType
from flask import jsonify, request
from flask_login import login_required, current_user
from app.utils import round_dict_values
from app.models import Transaction

@login_required
def transactions():
    query = Transaction.query

    if request.args.get('period_id'):
        query = query.filter(Transaction.period_id == request.args.get('period_id'))
    if request.args.get('year'):
        query = query.filter(Transaction.period_id.like(f'%{request.args.get("year")}'))
    if request.args.get('type') and request.args.get('type') != TransactionType.ALL.value:
        query = query.filter(Transaction.type == request.args.get('type'))

    query = query.filter(Transaction.user_id == current_user.id).order_by(Transaction.date.asc())

    transactions = [transaction.to_json() for transaction in query]

    return jsonify({ 'txs': transactions }), 200

@login_required
def balance():
    period_id = request.args.get('period_id')
    year = request.args.get('year')

    query = Transaction.query

    if period_id:
        query = query.filter(Transaction.period_id == period_id)
    if year:
        query = query.filter(Transaction.period_id.like(f'%{year}'))

    query = query.filter(Transaction.user_id == current_user.id)

    transactions = query.all()

    balance_in, balance_out, investments_in, investments_out, others = 0, 0, 0, 0, 0
    for row in transactions:
        if row.type is TransactionType.INCOME.value:
            balance_in += float(row.value)
        elif row.type is TransactionType.OUTCOME.value:
            balance_out += float(row.value)
        elif row.type is TransactionType.INVESTMENT_IN.value:
            investments_in += float(row.value)
        elif row.type is TransactionType.INVESTMENT_OUT.value:
            investments_out += float(row.value)
        else:
            others += float(row.value)

    data = round_dict_values({
        'balance_in': balance_in,
        'balance_out': balance_out,
        'investments_in': investments_in,
        'investments_out': investments_out,
        'io_balance': balance_in - balance_out,
        'investments_balance': investments_in - investments_out,
        'others': others
    })

    return jsonify(data), 200

from enum import Enum

class TransactionType(Enum):
    OUTCOME = '1'
    INCOME = '2'
    INVESTMENT_IN = '3'
    INVESTMENT_OUT = '4'
    OTHER = '5'
    ALL = '6'

class NodeNames(Enum):
    MOVIMIENTO = 'Movimiento'
    VALOR = 'VALOR'
    FECHA = 'FECHA'
    DESCRIPCION = 'DESCRIPCION'

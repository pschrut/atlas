from enum import Enum

class TransactionType(Enum):
    INCOME = 1
    OUTCOME = 2
    OTHER = 3

class NodeNames(Enum):
    MOVIMIENTO = 'Movimiento'
    VALOR = 'VALOR'
    FECHA = 'FECHA'
    DESCRIPCION = 'DESCRIPCION'
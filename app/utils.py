from datetime import datetime
import calendar
from app.enums import TransactionType

def sanitize_xml(file_content):
    file_storage = file_content.read()
    xml_content = file_storage.decode('ISO-8859-1', errors = 'replace')
    xml_content = xml_content.replace('ï¿½', 'O')
    xml_content = xml_content.replace('Ó', 'O')

    return xml_content.encode('ISO-8859-1')

def convert_to_float(value):
    return float(value.replace(',', ''))

def convert_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%Y/%m/%d')
        formatted_date = date_obj.strftime('%m%y')
        return formatted_date
    except ValueError:
        return 'Invalid date format'
    
def get_type(value):
    converted_value = float(value)

    if converted_value > 100000000:
        return TransactionType.INVESTMENT_IN.value
    elif converted_value < -100000000:
        return TransactionType.INVESTMENT_OUT.value
    elif converted_value > 0:
        return TransactionType.INCOME.value
    elif converted_value < 0:
        return TransactionType.OUTCOME.value

    return TransactionType.OTHER.value

def get_month_range(period_id):
    month = int(period_id[:-2])
    year = 2000 + int(period_id[-2:])  # Assuming the years are in the format 'YY'

    num_days = calendar.monthrange(year, month)[1]
    first_day = f"{year}-{month:02d}-01"  # Zero-padded month
    last_day = f"{year}-{month:02d}-{num_days}"  # Zero-padded month

    return {'first_day': first_day, 'last_day': last_day}

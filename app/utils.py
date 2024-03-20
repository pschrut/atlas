def sanitize_xml(file_content):
    file_storage = file_content.read()
    xml_content = file_storage.decode('ISO-8859-1', errors='replace')
    xml_content = xml_content.replace('ï¿½', 'O')
    xml_content = xml_content.replace('Ó', 'O')

    return xml_content.encode('ISO-8859-1')

def convert_to_float(value):
    return float(value.replace(',', ''))
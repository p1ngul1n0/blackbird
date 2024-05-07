import hashlib
import config

def processInput(input, operation):
    if (operation == "hash-sha256"):
        email_bytes = input.encode('utf-8')
        retValue = hashlib.sha256(email_bytes).hexdigest()
        return retValue
    else:
        config.console.print(f" Invalid operation {input} [{operation}]")
    
def access_json_property(data, path_config):
    try:
        property_value = data
        # Percorre o caminho especificado
        for key in path_config:
            # Acessa o próximo nível usando a chave ou índice
            property_value = property_value[key]
        return property_value
    except:
        return False
    
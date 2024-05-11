import hashlib
import config


def processInput(input, operation):
    if operation == "hash-sha256":
        email_bytes = input.encode("utf-8")
        retValue = hashlib.sha256(email_bytes).hexdigest()
        return retValue
    else:
        config.console.print(f" Invalid operation {input} [{operation}]")

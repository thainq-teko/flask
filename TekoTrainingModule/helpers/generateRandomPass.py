import random
import string


# func for creating password
def generatePassword(length):
    numStr = ''.join(random.choice(string.digits) for _ in range(2))
    charStr = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(length - 2))
    return charStr[-6:-2] + numStr + charStr[-2:]
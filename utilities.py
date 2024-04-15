import string,random

def genAlphaNum(size):
    num=list(range(0,10))
    num.extend(string.ascii_uppercase)
    keyList = random.sample(num,size)
    key=""
    for i in keyList:
        key += str(i)
    return key



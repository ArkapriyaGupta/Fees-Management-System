import string,random

def genAlphaNum(size):
    num=list(range(0,10))
    num.extend(string.ascii_uppercase)
    keyList = random.sample(num,size)
    key=""
    for i in keyList:
        key += str(i)
    return key

errorList = {}
errorList["generalError"] = "Sorry! We ran into an error. Please try again."
errorList["duplicateUser"] = "Sorry! the user already exist. Please login."
errorList["saveError"] = "Some error occured in saving the data. Please try again."
errorList["inputError"] = "Could not fetch input. Please try again."
errorList["emptyInput"] = "One of the input field is empty. Please try again"
errorList["invalidRole"] = "You have selected an invalid/no role. Please try again"
errorList["saveError"] = "Some error occured in saving the data. Please try again."
errorList["invalidUser"] = "The user does not exist. Please try again."
errorList["invalidPassword"] = "The password is incorrect. Please try again."
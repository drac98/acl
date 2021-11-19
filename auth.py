import hashlib

# Access Control List
acl = {
    "data.csv":{
        "admin":['r','w'],
        "doctor":['r', 'w'], 
        "patient":['r'],
        "nurse":['r'],
        "receptionist":['r','w'],
        "laboratorian":['r']
        },

    "config.csv":{
        "admin":['r','w'], 
        "receptionist":['w']
        }
    
    }

# Sensitivity of each data record
fieldSensitivity = {
        "username":10, 
        "first":10, 
        "last":10, 
        "location":10, 
        "contact":10, 
        "sickness":6, 
        "drug":8, 
        "lab":7
    
    }

def login(username, password, config_rows):
    for row in config_rows:
        # MD5 hash of the password
        hash = hashlib.md5(password.encode())
        if username.lower()==row[0] and hash.hexdigest() == row[1]:
            return True
    return False

def getUsertype(username, config_rows):
    for row in config_rows:
        if(row[0]==username):
            return row[3] 

def getPermission(usertype, filename, access, acl):
    try:
        if (access in acl[filename][usertype.lower()] ):
            return True
    # Return False if user is not found
    except KeyError:
        return False

def isPermitted(username, password, config_rows, filename, access, acl):
    usertype = getUsertype(username, config_rows)
    return login(username, password, config_rows) and getPermission(usertype, filename, access, acl)

def getAllowedFields(usertype, fieldSensitivity, data_fields):
    if(usertype=="patient"):  privilege = 5
    elif(usertype=="receptionist"):  privilege = 10
    elif(usertype=="laboratorian"):  privilege = 7
    elif(usertype=="nurse"):  privilege = 8
    elif(usertype=="doctor"): privilege = 5
    elif(usertype=="admin"):  privilege = 0
    else: privilege = -1

    allowedFields = []

    for field, prv in fieldSensitivity.items():
        
        if prv>=privilege:
            allowedFields.append(data_fields.index(field))

    return allowedFields
from rwfiles import *
from auth import *

# csv file name
config = "config.csv"
data = "data.csv"
  
# Create lists to hold the field names and the rows of data
config_fields = []
config_rows = []
data_fields = []
data_rows = []

# Initialize the lists with custom defined fucntions  
config_fields, config_rows = readCSV(config)
data_fields, data_rows = readCSV(data)


if(__name__=="__main__"):

    while(True):
        authenticated = False
        print("Login to continue.")

        while(not authenticated):
            username = input("Enter username: ")
            password = input("Enter password: ")

            # Authenticate User
            authenticated = login(username, password, config_rows)
            if authenticated:
                usertype = getUsertype(username, config_rows)

                # Get user's access control details
                dataWrt_permission = getPermission(usertype, "data.csv", 'w', acl)
                dataRd_permission = getPermission(usertype, "data.csv", 'r', acl)
                isPermitted(username, password, config_rows, data, 'r', acl)

                configWrt_permissions = getPermission(usertype, "config.csv", 'w', acl)
                configRd_permissions = getPermission(usertype, "config.csv", 'r', acl)
                
                # Get indexes of the filed which the user has access to based on the sensitivity of data.
                allowedDataFields = getAllowedFields(usertype, fieldSensitivity, data_fields)

            else:
                print("Authentication Failed. Try again!")

        while (True):
            print("")
            print("List of operations")
            print("0: Logout")
            print("1: View records")
            print("2: Add record")
            print("3: View users")
            print("4: Create User")
            print("")

            # Get operation input
            operation = int(input("Select an Operation: ").strip())
            print("")

            # Conditional statements to execute the operation (Switch case)
            if operation==0:
                break
            elif operation==1:
                if dataRd_permission:
                    if (usertype=="patient"):
                        viewRecord(username, data_rows, allowedDataFields)
                    else:
                        username = input("Enter Patient username: ")
                        viewRecord(username, data_rows, allowedDataFields)
                else:
                    print("You do not have permission to view this patient record.")

            elif operation==2:
                if dataWrt_permission:
                    username = input("Enter Patient username: ")
                    first = input("First Name: ")
                    last = input("Last Name: ")
                    location = input("Location: ")
                    contact = input("contact: ")
                    sickness = input("Sickness Details: ")
                    drug = input("Drug Prescription: ")
                    lab = input("Lab Test Prescription: ")

                    writeRecord("data.csv", username, first, last, location, contact, sickness, drug, lab)

                    # Refresh data after write
                    data_fields, data_rows = readCSV(data)
                else:
                    print("You do not have permission to add patient records.")

            elif operation==3:
                if configRd_permissions:
                    username = input("Enter username to search: ")
                    viewUsers(username, config_rows)
                else:
                    print("You do not have permission to view user details.")

            elif operation==4:
                if configWrt_permissions:
                    username = input("Enter a username: ") 
                    password = input("Enter a password: ") 
                    usertype = input("Enter a usertype (staff/patient): ") 
                    privilege = input("Enter a privilege (patient/doctor/nurse/receptionist/admin): ") 

                    createUser("config.csv", username, password, usertype, privilege)

                    # Refresh config after write
                    config_fields, config_rows = readCSV(config)
                else:
                    print("You do not have permission to create users.")
                
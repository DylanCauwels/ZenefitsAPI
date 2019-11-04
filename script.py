# Dylan Cauwels
# Zenefits Begineer API
# 2-19-2018 -> 2-20-2018
import requests
import json
import sys
from pprint import pprint

class Employee:
    def  __init__(self, first_name, last_name, workPhone, workEmail, personalPhone, personalEmail):
        self.first_name = first_name
        self.last_name = last_name
        self.workPhone = workPhone
        self.workEmail = workEmail
        self.personalPhone = personalPhone
        self.personalEmail = personalEmail
        self.department = ""
        self.location = ""
        self.manager = ""
        self.title = ""

    def addDepartment(self, department):
        self.department = department

    def addLocation(self, location):
        self.location = location

    def addManager(self, manager):
        self.manager = manager

    def addTitle(self, title):
        self.title = title

    def printEmployee(self):
        print(self.first_name + " | " + self.last_name + " | " + self.department + " | " + self.location + " | " + self.manager)

    def checkForKeyword(self, keyword):
        lowerFirst = self.first_name.lower()
        lowerLast = self.last_name.lower()
        if(self.first_name.find(keyword) != -1 or self.last_name.find(keyword) != -1
            or self.department.find(keyword) != -1 or self.location.find(keyword)
            != -1 or  self.manager.find(keyword) != -1 or self.title.find(keyword)
            != -1 or self.location.find(keyword) != -1 or lowerFirst.find(keyword) != -1
            or lowerLast.find(keyword) != -1):
            return True
        return False



def inputNewKey():
    newKey = ""
    newKeyCheck = "0"
    while (newKey != newKeyCheck):
        newKey = raw_input("Input New Key Value: ")
        newKeyCheck = raw_input("Input New Key Value Again: ")
        if (newKey != newKeyCheck):
            print("MisMatching Keys, Try Again ")
    return newKey


key = '4ZUwULwgQTu8W4XUFMEd'
keyChoice = raw_input("Would you like to use a different key than the provided default? (Y/N): ")
keyChoice = keyChoice.strip()
keyChoice = keyChoice.lower()
if (keyChoice == 'y'):
    key = inputNewKey()
headers = {
    'Authorization': 'Bearer ' + key,
}
url = 'https://api.zenefits.com/core/people/'

listOfEmployees = []
response = requests.get(url, headers=headers)
sys.stdout.write("Loading: ")
sys.stdout.flush()
for x in response.json()['data']['data']:
    temporary = Employee(x['first_name'], x['last_name'], x['work_phone'], x['work_email'], x['personal_phone'],
         x['personal_email'])
    sys.stdout.write('#')
    sys.stdout.flush()
    locationURL = x['location']['url']
    if(x['title']):
        addTitle(x['title'])
    if (locationURL):
        locationResponse = requests.get(locationURL, headers=headers)
        location = locationResponse.json()['data']['name']
        temporary.addLocation(location)
    managerURL = x['manager']['url']
    if (managerURL):
        managerResponse = requests.get(managerURL, headers=headers)
        manager = managerResponse.json()['data']['first_name'] + " " + managerResponse.json()['data']['last_name']
        temporary.addManager(manager)
    departmentURL = x['department']['url']
    if(departmentURL):
        departmentResponse = requests.get(departmentURL, headers=headers)
        department = departmentResponse.json()['data']['name']
        temporary.addDepartment(department)
    listOfEmployees.append(temporary)
print("\nData Retrieved Succesfully \nType 'help' for list of valid commands")

while True:
    command = raw_input("\nWhat would you like to do?: ")
    command = command.strip()
    command = command.lower()
    if(command == 'help'):
        print("Commands: \nhelp \nlistall \nsearch \nend")
    elif(command == 'listall'):
        for x in listOfEmployees:
            x.printEmployee()
    elif(command == 'end'):
        print("Program Ending..")
        break
    elif(command == 'search'):
        item = raw_input("Item Wishing to be Searched: ")
        item = item.strip()
        foundEmployees = []
        for x in listOfEmployees:
            if (x.checkForKeyword(item)):
                x.printEmployee()
                foundEmployees.append(x)
        if(not foundEmployees):
            print("No Employees Found")
        else:
            choice = raw_input("Would you like Contact Information? (Y/N): ")
            choice = choice.strip()
            choice = choice.lower()
            if(choice == 'y'):
                for x in foundEmployees:
                    print("\n" + x.first_name + " " + x.last_name + ":")
                    if(x.workPhone):
                        print("Work Phone: " + x.workPhone)
                    if(x.workEmail):
                        print("Work E-mail: " + x.workEmail)
                    if(x.personalPhone):
                        print("Personal Phone: " + x.personalPhone)
                    if(x.personalEmail):
                        print("Personal E-mail: " + x.personalEmail)
    else:
        print("Invalid Command")

#curl -i https://api.zenefits.com/core/people -H "Authorization: Bearer 4ZUwULwgQTu8W4XUFMEd"

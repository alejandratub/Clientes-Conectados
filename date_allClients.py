
from os import write
import requests
import json
import csv
from datetime import datetime
import time

#Aruba Central API Gateway URL
base_url = ""

#Access token a nivel tenant
atoken=""

#Nombre del archivo que se va a generar
filename = "Client Count"


#Menu en consola
def menu():

    start_time = input("Enter start Time and Date for cosnult (dd/mm/yyyy hh/mm): ")
    print(start_time)
    end_time = input("Enter end Time and Date for cosnult (dd/mm/yyyy hh/mm): ")
    print(end_time)

    start_time_timestamp = time.mktime(datetime.strptime(start_time, "%d/%m/%Y %H:%M").timetuple())
    end_time_timestamp = time.mktime(datetime.strptime(end_time, "%d/%m/%Y %H:%M").timetuple())

    getByDate(filename, start_time_timestamp, end_time_timestamp, atoken)


#Funcion para generar archivo con reporte

def getByDate(filename, start_time_timestamp, end_time_timestamp, atoken):
    url = "/monitoring/v2/aps"
    fullurl = base_url + url
    print("Generating File")

    access_token= atoken

    parameters = {"access_token": access_token, 'limit':'1000'}

    respMonitoring = requests.get(fullurl,params=parameters)
    respuestaJsonAPs = respMonitoring.json()['aps']
    AccessPoints = []
    Groups = []
    AccessPoints_Groups = []
    

    #Add all AP information into lists for later use
    for row in respuestaJsonAPs:
            AccessPoints.append(str(row['serial']))
            Groups.append(str(row['group_name']))
            temp = []
            temp.append(str(row['name']))
            temp.append(str(row['serial']))
            temp.append(str(row['group_name']))
            AccessPoints_Groups.append(temp)

    #FIle Keys (Headers)
    FileKeys = []
    FileKeys.append('name')
    FileKeys.append('serial')
    FileKeys.append('group_name')
    FileKeys.append('client_count')
    FileKeys.append('timestamp')

    outputFile = open(filename+'.csv', 'a') #load csv file
    output = csv.writer(outputFile) #create a csv.write
    output.writerow(FileKeys)  # header row

    for ap in AccessPoints_Groups:
        print(ap[0])
        print(ap[1])
        print(ap[2])
        url = "/monitoring/v1/clients/count"
        fullurl = base_url + url

        access_token= atoken
        
        parameters = {"access_token": access_token, 'serial':ap[1],"from_timestamp": int(start_time_timestamp), "to_timestamp": int(end_time_timestamp)}

        respMonitoring = requests.get(fullurl,params=parameters)
        responseJsonClients = respMonitoring.json()['samples']

        for row in responseJsonClients:
                writeData = []
                dt_obj = datetime.fromtimestamp((row['timestamp']))
                outputFile = open(filename+'.csv', 'a') #load csv file
                output = csv.writer(outputFile) #create a csv.write
                writeData.append(ap[0])
                writeData.append(ap[1])
                writeData.append(ap[2])
                writeData.append((row['client_count']))
                writeData.append(dt_obj)
                output.writerow(writeData) #values row

    print("file complete")
if __name__ == "__main__":
    menu()
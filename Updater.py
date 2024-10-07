import requests
import time
import msvcrt
import os

ipList = []
keyList = []
nameList = []
updateState = False


def updateLists():
    global ipList
    global keyList
    global nameList

    with open(r'Files\printers.txt', 'r') as file:
        data = file.read()

    printers = data.split('\n')
    if printers[-1] == '':
        printers.pop()

    for x in range(len(printers)):
        ipList.append(printers[x].split(',')[0])
        keyList.append(printers[x].split(',')[1])
        nameList.append(printers[x].split(',')[2])

    print('Lists updated')


def getDataFromPrinter(ip, key):
    try:
        headers = {
            "Accept": "application/json",
            "Host": ip,
            "X-Api-Key": key
        }
        response = requests.request("GET", 'http://' + ip + '/api/job', headers=headers)
        #print(response.json())

        if response.status_code == 200:
            return response.json()
        else:
            return f"Request failed with status code: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"


def updateStatus():
    global updateState

    if updateState:
        return

    updateState = True
    printerReturn = []
    data = []
    for x in range(len(ipList)):
        printerReturn.append(getDataFromPrinter(ipList[x], keyList[x]))

    # print(printerReturn)

    for z in printerReturn:
        if type(z) is str:
            data.append(z)
        elif type(z) is dict:
            data.append(str(z.get('state')) + ';' + str(z.get('job').get('file').get('name')) + ';' + str(z.get('progress').get('completion')))

    with open(r'Files\temp.txt', 'w') as file:
        msvcrt.locking(file.fileno(), msvcrt.LK_NBLCK, os.path.getsize(r'Files\temp.txt'))
        for y in range(len(data)):
            file.write(nameList[y] + ';' + data[y] + '\n')
        msvcrt.locking(file.fileno(), msvcrt.LK_UNLCK, os.path.getsize(r'Files\temp.txt'))


    print('Status updated')
    updateState = False


def copyDatabase():
    names = []
    ips = []
    keys = []
    validPrinters = []

    with open(r'Files\database.txt', 'r') as file:
        data = file.read()

    printers = data.split('\n')
    if printers[-1] == '':
        printers.pop()

    for x in range(len(printers)):
        tempData = printers[x].split(',')
        names.append(tempData[1].strip())
        ips.append(tempData[3].split("'")[1].strip())
        keys.append(tempData[4].split("'")[1].strip())

    for y in range(len(names)):
        response = getDataFromPrinter(ips[y], keys[y])
        if response is not str:
            validPrinters.append(ips[y] + ',' + keys[y] + ',' + names[y])

    validPrinters = sorted(validPrinters, key=lambda x: int(x.split()[1].split("'")[0]))

    with open(r'Files\printers.txt', 'w') as file:
        for z in range(len(validPrinters)):
            file.write(validPrinters[z]+'\n')

    print('Database updated')

    # with open(r'Files\printers.txt', 'r') as file:
    # oldList = file.read()
    # file.write(oldList)


if __name__ == '__main__':
    # copyDatabase()
    # updateStatus()
    updateLists()
    # print(getDataFromPrinter('192.168.1.125', '897A6FD8D52F47919B5C2F09BBA6BF3D'))

    while True:
        updateStatus()
        time.sleep(30)
import json


def reFactor():
    with open(r'Files\oops.txt', 'r') as file:
        data = file.read()

    splitData = data.split(r'"Status updated"')
    for b in range(len(splitData)):
        tempData1 = splitData[b].split('[')
        tempData2 = splitData[b].split(']')
        if len(tempData1) > 1:
            splitData[b] = splitData[b].split('[')[1]
        elif len(tempData2) > 1:
            splitData[b] = splitData[b].split(']')[0]

    updateData = []
    for y in splitData:
        updateData.append(y.replace("\n", "").replace(" ", ""))

    printerData = []
    for z in updateData:
        printerData.append(z.split('},{'))

    with open(r'Files\oops2.txt', 'w') as file:
        for x in printerData:
            for a in x:
                tempData3 = a.replace('{"job"', '"job"').replace('"job"','{"job"').replace('"}]', '"') + '}'
                print(tempData3)
                tempData4 = json.loads(tempData3)
                tempData5 = tempData4["state"]
                tempData6 = tempData4["progress"]
                tempData7 = tempData4["job"]["file"]["name"]
                file.write(tempData5 + '  :  ' + tempData7 + '  :  ' + str(tempData6['printTimeLeft']) + '\n')
                #file.write(a + '\n')
            file.write('\n\n\n')


if __name__ == '__main__':
    reFactor()

    #json_string = '{"job":{"averagePrintTime":"None","estimatedPrintTime":"None","filament":"None","file":{"date":"None","display":"None","name":"None","origin":"None","path":"None","size":"None"},"lastPrintTime":"None","user":"None"},"progress":{"completion":"None","filepos":"None","printTime":"None","printTimeLeft":"None","printTimeLeftOrigin":"None"},"state":"Offline(Error:Connectionerror,seeTerminaltab)"}'
    #data_dict = json.loads(json_string)
    #print(data_dict)

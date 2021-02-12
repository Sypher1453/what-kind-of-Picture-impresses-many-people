import urllib.request
import csv
import time
import random

def saveParameter(filePath, picsName, params):
    datas = []
    i = picsName.split('/')[-1].split(".")[0]

    datas.append(params +  [i])


    with open(filePath + '/pP_data' + str(random.randint(0,10000)) + '.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)
        for data in datas:
            spamwriter.writerow(data)





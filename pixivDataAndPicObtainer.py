import urllib.request
import csv
import time
import random

params_alreadyKnown = [0, 0, 0, 0] # set your picture's statistical params which has been alreaady known On Pixiv
picsName = '' #put the picture path you selected to check

def saveParameter(filePath, picsName, params):
    datas = []
    i = picsName.split('/')[-1].split(".")[0]

    datas.append(params +  [i])


    with open(filePath + '/pP_data' + str(random.randint(0,10000)) + '.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)
        for data in datas:
            spamwriter.writerow(data)





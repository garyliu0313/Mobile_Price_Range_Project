import csv
import math
from sklearn.utils import resample
import sys


def loadCsv(filename):
    data = []
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            data.append(list(row))
    return data


def classCount(data):
    classes = {}
    for i in range(len(data)):
        entry = data[i]
        if (entry[-1] not in classes):
            classes[entry[-1]] = 0
        classes[entry[-1]] += 1
    return classes


def priorProbability(data, classes):
    prior = []
    for i in range(len(data[0])-1):
        attridict = {}
        for j in range(len(data)):
            entry = data[j][i]
            result = data[j][-1]
            if entry not in attridict:
                attridict[entry] = {}
            if result not in attridict[entry]:
                attridict[entry][result] = 0
            attridict[entry][result] += 1
        prior.append(attridict)
    for col in prior:
        for entries in col.values():
            for k, v in entries.items():
                entries[k] = v/classes[k]
    return prior


def predict(test, classes, data):
    prior = priorProbability(data[1:], classes)
    pred = []
    for item in test:
        temp = {}
        for key in classes.keys():
            temp[key] = 0
        for i in range(len(item)-1):
            key = item[i]
            for k in temp.keys():
                try:
                    temp[k] += math.log(prior[i][key][k])
                except:
                    pass
        for k in temp.keys():
            temp[k] += math.log(classes[k]/float(len(data)))
        maxv = float("-inf")
        maxk = ''
        for k, v in temp.items():
            if v > maxv:
                maxv = v
                maxk = k
        pred.append([maxk, str(item[-1])])
    return pred


def computeAccuracy(prediction):
    right = 0
    for item in prediction:
        if item[0] == item[1]:
            right += 1
    return right/float(len(prediction))


def bootstrap(train,test):

    classes = classCount(train)
    prediction = predict(test, classes, train)
    return computeAccuracy(prediction)



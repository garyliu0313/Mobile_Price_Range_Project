import bayes
import dtree_build
import math
import csv
import regression_tree
from sklearn.utils import resample
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pandas
train = []
test = []
col = ['battery_power','blue','clock_speed','dual_sim','fc','four_g','int_memory','m_dep','mobile_wt','n_cores','pc','px_height','px_width','ram','sc_h','sc_w','talk_time','three_g','touch_screen','wifi']

data = []

with open("processed.csv") as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        data.append(list(row))

rtree_data = pandas.read_csv("train.csv")
X = rtree_data.drop('price_range',axis=1)
Y = rtree_data['price_range']
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.33, random_state=101)
reg = LinearRegression()
reg=reg.fit(X_train,y_train)
b=reg.score(X_test,y_test)
from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors=10)
knn.fit(X_train,y_train)
print(knn.score(X_test,y_test))
#split trainning and testing dataset
train = resample(data[1:], replace=True, n_samples=int(len(data)))
for i in data[1:]:
    if i not in train:
        test.append(i)


dtree = dtree_build.buildtree(train,min_gain=0.001,min_samples=2)
rtree = regression_tree.buildtree(train, min_gain =0.001, min_samples = 2)
#dtree_build.printtree(dtree, " ", col)
naccuracy = bayes.bootstrap(train,test)
dcorrect = 0
output = [['inst/#', 'actual', 'predicted', 'probability']]
count = 0

#compute for dtree
for item in test:
    count += 1
    result = dtree_build.classify(item, dtree)
    total = 0
    max = 0
    str = ''
    for i, j in result.items():
        total += float(j.strip('%'))/100
        if float(j.strip('%'))/100 >= max:
            max = float(j.strip('%'))/100
            str = i
    if str == item[-1]:
        dcorrect += 1
    output.append([count, float(item[-1]), str, max / total])
rcorrect = 0

#compute for rtree
for item in test:
    result = int(float(regression_tree.classify(item, rtree)))
    if result == int(item[-1]):
        rcorrect += 1

with open("predicted.csv", "w") as new_csv:
    writer = csv.writer(new_csv)
    writer.writerows(output)
    print("Accuracy for rtree:",rcorrect/len(test))
    print("Accuracy for dtree:" , dcorrect / len(test))
    print("Accuracy for nbayes:" ,naccuracy,)

from flask import Blueprint, render_template, request
import dtree_build
from sklearn.utils import resample
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pandas
import csv
global dtree
train = []
test = []
col = ['battery_power','blue','clock_speed','dual_sim','fc','four_g','int_memory','m_dep','mobile_wt','n_cores','pc','px_height','px_width','ram','sc_h','sc_w','talk_time','three_g','touch_screen','wifi']

data = []

# with open("../../processed.csv") as csvfile:
#     readCSV = csv.reader(csvfile, delimiter=',')
#     for row in readCSV:
#         data.append(list(row))
# train = resample(data[1:], replace=True, n_samples=int(len(data)))
# for i in data[1:]:
#     if i not in train:
#         test.append(i)
# dtree = dtree_build.buildtree(train,min_gain=0.001,min_samples=3)
# dcorrect = 0
#compute for dtree
from sklearn.neighbors import KNeighborsClassifier

rtree_data = pandas.read_csv('train.csv')
X = rtree_data.drop('price_range',axis=1)
Y = rtree_data['price_range']
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.33, random_state=101)
reg = LinearRegression()
reg=reg.fit(X_train,y_train)
knn = KNeighborsClassifier(n_neighbors=10)
knn.fit(X_train,y_train)
import random
bp = Blueprint(__name__, __name__,
                        template_folder='templates')

@bp.route('/predict_price', methods = ['POST','GET'])
def show():
    if request.method == 'POST':
        if request.form.get('submit'):
            web = []
            for item in col:
                web.append(request.form.get(item))
            with open("buffer.csv","w") as ncsv:
                writer = csv.writer(ncsv)
                writer.writerows([col,web])
            reg_data = pandas.read_csv("buffer.csv")
            st = 0
            st=predict(reg_data)
            return st
    return render_template('predict_price.html')
def predict(web):
    max = 0
    st = ''
    # result = dtree_build.classify(web, dtree)
    # for i, j in result.items():
    #     if float(j.strip('%')) / 100 >= max:
    #         max = float(j.strip('%')) / 100
    b = knn.predict(web)
    a = b[0]
    if a == 0:
        st = 'Price is below 200$'
    elif a == 1:
        st = 'Price is below 500$'
    elif a == 2:
        st = 'Price is below 800$'
    elif a == 3:
        st = 'Price is below 1100$'
    return (st)
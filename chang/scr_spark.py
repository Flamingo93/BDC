import cPickle as pickle
from pyspark.ml.linalg import Vectors
from pyspark.ml.classification import LogisticRegression
from pyspark.sql import SparkSession

spark = SparkSession \
    .builder \
    .appName("Python Spark SQL basic example") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()


with open('feature_set_removelast4','rb') as f:
    feature_vector = pickle.load(f)
# print len(feature_vector)


def tr2dense(vector):
    d_vector = [vector[0], Vectors.dense(vector[1])]
    return d_vector

dense_vector = map(tr2dense, feature_vector)

training_df = spark.createDataFrame(dense_vector, ['label', 'features'])
# training_df.show()
lr = LogisticRegression(maxIter=10000, regParam=0,threshold=0.70,elasticNetParam=1)
lrModel = lr.fit(training_df)
print("Coefficients: " + str(lrModel.coefficients))
print("Intercept: " + str(lrModel.intercept))

# prediction = lrModel.transform(training_df)
# selected = prediction.select('label','features','probability','prediction').collect()
# # result_list = selected.filter(selected['prediction'] < 0.5)
# # result_id_list = result_lis.select['label','prediction'].collect()
#
# both_0 = 0
# label_0 = 0
# prediction_0 = 0
# for n in range(len(selected)):
#     if 0 == int(selected[n].prediction) and int(selected[n].label) ==0:
#         both_0 = both_0 + 1
#     if int(selected[n].label) == 0:
#         label_0 = label_0 + 1
#     if int(selected[n].prediction) == 0:
#         prediction_0 = prediction_0 + 1
# P = float(both_0)/float(prediction_0)
# R = float(both_0)/float(label_0)
# print 'predic_0:', prediction_0
# print 'label_0:', label_0
# print 'both_0:', both_0
# print 'P:', P
# print 'R:', R
# print 'F:', 5*P*R/(2*P+3*R)*100





with open('feature_test1_set_id','rb') as t:
    feature_test1_vector = pickle.load(t)


def tr2dense_test(vector):
    d_test_vector = [vector[0], Vectors.dense(vector[1])]
    return d_test_vector

dense_test1_vector = map(tr2dense_test, feature_test1_vector)
# print dense_test1_vector
test1_df = spark.createDataFrame(dense_test1_vector, ['id', 'features'])
test1_df.show()

prediction = lrModel.transform(test1_df)
selected = prediction.select('id','features','probability','prediction')
result_list = selected.filter(selected['prediction'] < 0.5)
result_id_list = result_list.select(result_list['id']).collect()
print result_id_list


def tr2strlist(row):
    str_id = str(row.id)
    return str_id

result_list_str = map(tr2strlist, result_id_list)
print len(result_list_str)


out_file = open('dsjtzs_txfzjh_preliminary1.txt','w')
for ele in result_list_str:
    print>>out_file, ele
out_file.close()


# with open('result_id_list','wb') as id_list:
#     pickle.dump(result_id_list, id_list)
# #

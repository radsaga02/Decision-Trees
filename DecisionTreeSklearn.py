from sklearn import tree
import sys
import pandas as pd
import numpy as np

def dummies(data,col):
    dummies = pd.get_dummies(data[col]).rename(columns=lambda x: col+'_' + str(x))
    data=pd.concat([data, dummies], axis=1)
    data=data.drop([col], axis=1)
    return data

trainingFile=sys.argv[1]
testFile=sys.argv[2]

df=pd.read_csv(trainingFile)
testData=pd.read_csv(testFile)

columns=df.columns
trainingData=df.iloc[:,:len(columns)-1]
allcols=columns[:len(columns)-1]
trainingdata=df.iloc[:,len(columns)-1:]
target=columns[len(columns)-1:]
for col in allcols:
    trainingData=dummies(trainingData,col)
trainingdata=dummies(trainingdata,target[0])
node = tree.DecisionTreeClassifier(criterion='entropy',min_samples_split=2,random_state=100000)
node = node.fit(trainingData, trainingdata)
tree.export_graphviz(node,out_file='tree.dot')
dt=testData
for col in allcols:
    testData=dummies(testData,col)
col_name=list(set(trainingData.columns)-set(testData.columns))
newdataframe=pd.DataFrame(0.0,index=np.arange(len(testData)),columns=col_name)
testData=pd.concat([testData,newdataframe], axis=1)
newTestData=pd.DataFrame(None,columns=[trainingData.columns])
for col in trainingData.columns:
    newTestData[col]=testData[col]
res=pd.DataFrame(node.predict(newTestData),columns=trainingdata.columns)
result=pd.DataFrame(columns=[target])
for row in range(0,len(dt)):
    for col in trainingdata:
        if res.loc[row,col]==1:
            result.loc[row,target]=col.split('_')[1]
print("The output is \n")
print(pd.concat([dt,result],axis=1))



    
    


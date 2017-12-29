# -*- coding: utf-8 -*-
import pandas as pd
import math
from collections import defaultdict
import sys

class Decision:
    
    def __init__(self, rootNode = None, branch = defaultdict(), outcome = [], level = 0, label = None):
        self.rootNode = rootNode
        self.branch = branch
        self.outcome = outcome
        self.level = level  
        self.label = label
    
    def entropy(self,column):  
        nor=(len(column))
        if nor<=1:
            return 0
        a=column.value_counts()
        prob=a[0]/nor
        if prob==1 or prob==0:
            return 0
        e=(-1)*prob*math.log(prob,2)-((1-prob)*math.log((1-prob),2))
        return (e)
    
    def classifier(self,dataframe):
        label = self.label
        nor=(len(dataframe[label]))
        branchNode = defaultdict(None)
        
        #calulating entropy of whole data set
        e1=self.entropy(dataframe[label])
        
        #print ("================== \nEntropy of new data set: ",e1)
        
        col_name=dataframe.columns
 
        lst1=[]
        for c in col_name:
            if c == label:
                break
            df1=dataframe[[c,label]]
            #print (df1)
            df1_unq=df1[c].unique()
            
            #If there is only 1 unique value then we have to stop; since 
            #the data set s pure and entropy is zero
            #we have to stop when there is only one record in the dataset : terminal node
                        
            lst=[]
            for x in df1_unq:
                df2=(df1.loc[df1[c] == x])
                totalsize=len(df2[c])
                p=totalsize/nor
                e2=p*self.entropy(df2[label])
                lst.append(e2)
            ig1=e1-sum(lst)
            lst1.append(ig1)
            
        #print (lst1)
        max_ig=max(lst1)
        #print ("Max_IG:"+str(max_ig))
        root_node=dataframe.columns[(lst1.index(max(lst1)))]    
        rootNode = root_node
        #print ("================= \nNew node is : ",root_node)
        outcome = dataframe[label].unique()      
        df3_unq=dataframe[root_node].unique()
        if max_ig>0 :    
            for u in df3_unq:
               #print("============================ << Branch >> ========================") 
               df3 =(dataframe.loc[dataframe[root_node] == u])
               #print(df3)
               #print(len(df3.Enjoy.unique()))
               if len(df3)>=1:
                   branchNode[u] = self.classifier(df3)
            #print("================= Level:  ends ===============") 
            return Decision(rootNode, branchNode, outcome)
        else :
            #print(">>> Terminal Node", root_node,"~~~~~~~~~~~~~~~~")
            return Decision(label, None, outcome)
    
        
    def callClassifier(self, data):  
        df=pd.DataFrame(data)
        self.label = df.columns[len(df.columns)-1]
        self.rootNode = self.classifier(df)
        self.level = self.calcHeight(self.rootNode)
        
        
    def calcHeight(self,rootNode):
        if rootNode.branch == None or rootNode == None:
            return 1
        else:
            height = 1 + max(self.calcHeight(rootNode.branch[u]) for u in rootNode.branch.keys())
        return height
    
    
    def getTree(self, node = None):
        height  =self.level
        if node == None:
            node = self.rootNode
        for i in range (1, height+1):
            print("LEVEL "+ str(i) +": " +"["+ self.getLevel(node, i))
            print('\n')
            
    def getLevel(self, node, level):
        label = self.label
        tmpBranch = node.branch
        if level == 1 and node.branch != None:
            output = str(node.rootNode)
        elif level == 1:
            output = label+ '{' + str(node.outcome[0]) + '}'
        else:
            output = '['
            if tmpBranch != None:
                for b in tmpBranch:
                    if b != None:
                        n = self.getLevel(tmpBranch[b], level-1)
                        if (level == 2):
                            output += str(b) +'->'
                        output += str(n) + '\t'
        output +=']'              
        return output
        
    def getResult(self, testData,  node = None):
        testDf = pd.DataFrame(testData)   
        if node == None:
            node = self.rootNode
        testAttr = testDf[node.rootNode]
        testBranch = node.branch[testAttr[0]]
        if(testBranch.branch != None):
            self.getResult(testData, testBranch)
        elif testBranch.rootNode == self.label:
            label = testBranch.outcome[0]
            print ('Test case is: \n\n',dftest,'\n\nThe result is: ', self.label,': ',label)
        else:
            print('Test case is: \n\n',dftest,'\n\nThe result is: ',self.label,': None')
            
        
       
def main():
    trainFile = sys.argv[1]
    testFile = sys.argv[2]
    
    trainData=pd.read_csv(trainFile)
    testData = pd.read_csv(testFile)
    global dftest
    dftest=pd.DataFrame(testData)
    tree = Decision()
    tree.callClassifier(trainData)
    tree.getTree()
    tree.getResult(testData)
    
if __name__ == '__main__':
    main()
     




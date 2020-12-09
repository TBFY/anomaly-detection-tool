
'''
On preliminarily created set of data stored in a file, creates a decision tree object; tree object shematically saved in a png image.
'''

import pandas as pd

class DecisionTreeClass:

    def __init__(self, conf, shared):

        self.conf = conf
        self.sharedMethods = shared

        # config vars
        # config vars

        self._dataSourceFilePath    = self.conf.tenderDataFVPath
        self._dataSourceFileName    = ''
        self._decisionTreeCriterium = 'gini'
        self._decisionTreeMaxDepth  = -1
        self._testDataSampleShare = 0.3

        # data storage variables
        # data storage variables

        self.tenderData = {}
        self.selectedTenderData = {}
        self.features2include = []
        self.feature2explore = ''
        self.featureSet = []
        self.mjuFeaturesInEnglish = {}
        self.features2includeEn = []
        self.feature2exploreEn = ''
        self.featureSetEn = []

        self.x_train, self.y_train = [], []
        self.x_test, self.y_test = [], []

        # results variables
        # results variables

        self._dataStorageFilePath = self.conf.tenderDataResultsPath + 'dTree/'
        self._dataStorageFileName = 'dt_schema'
        self.prediction_accuracy = 0.0

    def createDecisionTree(self, dTreeConfig):
        '''
        Function takes in data stored in self._dataSourceFilePath + self._dataSourceFileName
        creates a decision tree schema and stores it in self._resultsStoreageFilePath = '../data/data2Web/'

        :param dTreeConfig: dict containing config params for the script
        :return: void
        '''

        # import params
        # import params

        self._dataSourceFilePath = dTreeConfig['dataSourceFilePath'] if 'dataSourceFilePath' in dTreeConfig else self._dataSourceFilePath
        self._dataSourceFileName = dTreeConfig['dataSourceFileName'] if 'dataSourceFileName' in dTreeConfig else self._dataSourceFileName
        self._dataStorageFilePath = dTreeConfig['dataStorageFilePath'] if 'dataStorageFilePath' in dTreeConfig else self._dataStorageFilePath
        self._dataStorageFileName = dTreeConfig['dataStorageFileName'] if 'dataStorageFileName' in dTreeConfig else self._dataStorageFileName
        self._decisionTreeCriterium = dTreeConfig['criterion'] if 'criterion' in dTreeConfig else self._decisionTreeCriterium
        self._decisionTreeMaxDepth = dTreeConfig['max_depth'] if 'max_depth' in dTreeConfig else self._decisionTreeMaxDepth
        self._testDataSampleShare = dTreeConfig['test_data_sample'] if 'test_data_sample' in dTreeConfig else self._testDataSampleShare
        self.features2include = dTreeConfig['features2include'] if 'features2include' in dTreeConfig else self.features2include
        self.feature2explore = dTreeConfig['features2explore']

        # get features translations in English
        # get features translations in English

        self.mjuFeaturesInEnglish = self.conf.sharedCommon.getMJUFVEnglishTranslator()

        # translate features
        # translate features

        if self.feature2explore in self.mjuFeaturesInEnglish:
            self.feature2exploreEn = self.mjuFeaturesInEnglish[self.feature2explore]

        for featureName in self.features2include:
            if featureName in self.mjuFeaturesInEnglish:
                self.features2includeEn.append(self.mjuFeaturesInEnglish[featureName])
            else:
                print('error')
                self.features2includeEn.append(featureName)

        # move self.feature2explore to the end of the list
        # move self.feature2explore to the end of the list

        if self.feature2explore in self.features2include:
            self.features2include.remove(self.feature2explore)
            self.features2includeEn.remove(self.feature2exploreEn)

        self.featureSet = self.features2include.copy()
        self.features2include.append(self.feature2explore)

        self.featureSetEn = self.features2includeEn.copy()
        self.features2includeEn.append(self.feature2exploreEn)


        # calculate decision tree, assess accuracy & save schema into png image
        # calculate decision tree, assess accuracy & save schema into png image

        classifierObj = self.getDecisionTreeClassifier()
        self.calculatePredictionAccuracy(classifierObj)
        self.saveDecisionTree2JSON(classifierObj)
        self.saveDecisionTree2Image(classifierObj)

        return 0

    def getDecisionTreeClassifier(self):
        '''
        function creates and returns decision tree classifier object

        :return: decision tree classifier object
        '''

        # first read all feature vectors
        # first read all feature vectors

        self.tenderData = self.conf.sharedCommon.readDataFile2Dict(self._dataSourceFilePath + self._dataSourceFileName, "\t")
        self.tenderData['headEn'] = []

        # translate tender data 2 English
        # translate tender data 2 English

        for featureName in self.tenderData['head']:
            if featureName in self.mjuFeaturesInEnglish:
                self.tenderData['headEn'].append(self.mjuFeaturesInEnglish[featureName])
            else:
                #print('error', featureName)
                self.tenderData['headEn'].append(featureName)

        # load necessary libraries
        # load necessary libraries

        from sklearn.tree import DecisionTreeClassifier  # Import Decision Tree Classifier
        from sklearn.model_selection import train_test_split  # Import train_test_split function

        pima = pd.read_csv(self._dataSourceFilePath + self._dataSourceFileName, header=0, names=self.tenderData['headEn'], usecols=self.tenderData['headEn'], sep='\t')
        pima.columns = self.tenderData['headEn']
        #print(pima.head())

        # old approach
        # pima = pd.DataFrame(self.selectedTenderData['data'])
        # pima.columns = self.selectedTenderData['head']

        x = pima[self.featureSetEn]
        y = self.binariseVector(getattr(pima, self.feature2exploreEn))
        #print(x)
        #print(y)

        # split dataset into training set and test set
        # split dataset into training set and test set

        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(x, y, test_size=self._testDataSampleShare, random_state=1)  # 70% training and 30% test

        # create decision tree classifer object
        # create decision tree classifer object

        if self._decisionTreeMaxDepth < 0:
            clf = DecisionTreeClassifier(criterion=self._decisionTreeCriterium)
        else:
            clf = DecisionTreeClassifier(criterion=self._decisionTreeCriterium, max_depth=self._decisionTreeMaxDepth)

        # returned trained decision tree classifer
        # returned trained decision tree classifer

        return clf.fit(self.x_train, self.y_train)

    def calculatePredictionAccuracy(self, clf):
        '''
        function takes in graf object, data for prediction calculation and data to asses prediction accuracy
        and calculates prediction accuracy of decision tree object

        :param clf: decision tree classifier object
        :param X_test_data: data to be tested
        :param Y_test_data: data for test verification
        :return:
        '''

        # import necessary libraries
        # import necessary libraries

        from sklearn import metrics  # Import scikit-learn metrics module for accuracy calculation

        # Predict the response for test dataset
        # Predict the response for test dataset

        y_predicted = clf.predict(self.x_test)

        # compare predicted data to actual data
        # compare predicted data to actual data

        self.prediction_accuracy = metrics.accuracy_score(self.y_test, y_predicted)

        return None

    def convertDecisionTreeJSON(self, treeDict, treeNode):
        '''
        function creates a decision tree structure given by treeDict from node treeNode

        return tree structure dictionary
        '''

        # get current node
        # get current node

        node = treeDict['tree_']['nodes'][treeNode]
        node_v = treeDict['tree_']['values'][treeNode]

        # init return tree
        # init return tree

        returnTreeDict = {}
        returnTreeDict['name'] = []
        returnTreeDict['name'].append('all bids: ' + str(node[5]))
        returnTreeDict['name'].append('competitive bids: ' + str(int(node_v[0][1])))
        returnTreeDict['name'].append('feature: ' + self.features2includeEn[node[2]])
        returnTreeDict['name'].append('split at: ' + str(str('{0:.2f}'.format(node[3]))))

        # append left node tree
        # append left node tree

        leftNode = node[0]
        rightNode = node[1]
        if leftNode < 0 or rightNode < 0:
            return returnTreeDict

        leftNodeDict = {}
        if leftNode > 0:
            leftNodeDict = self.convertDecisionTreeJSON(treeDict, leftNode)

        if len(leftNodeDict) > 0:
            # init only if children exist
            returnTreeDict['children'] = []
            returnTreeDict['children'].append(leftNodeDict)

        # append right node tree
        # append right node tree

        rightNodeDict = {}
        if leftNode > 0:
            rightNodeDict = self.convertDecisionTreeJSON(treeDict, rightNode)

        if len(leftNodeDict) > 0 and len(rightNodeDict):
            returnTreeDict['children'].append(rightNodeDict)

        return returnTreeDict

    def saveDecisionTree2JSON(self, clf):
        '''
        function stores decision tree classifier into a json file

        return None
        '''

        # first, save classifier structure to json
        # first, save classifier structure to json

        import sklearn_json as skljson
        filename = self._dataStorageFilePath + self._dataStorageFileName + '-structure.json'
        skljson.to_json(clf, filename)

        # then, convert structure to desired format
        # then, convert structure to desired format

        import json
        with open(filename) as f:
            treeDict = json.load(f)

        finalTreeDict = self.convertDecisionTreeJSON(treeDict, 0)

        # and save final format to file
        # and save final format to file

        filenameOut = self._dataStorageFilePath + self._dataStorageFileName + '.json'
        with open(filenameOut, 'w') as outfile:
            json.dump(finalTreeDict, outfile)

        '''        
        # print("children_left")
        # print(clf.tree_.children_left)
        # print("children_right")
        # print(clf.tree_.children_right)
        # print("feature")
        # #print(clf.tree_.feature)
        # print("threshold")
        # #print(clf.tree_.threshold)
        # print("value")
        # #print(clf.tree_.value)
        '''

        return None

    def saveDecisionTree2Image(self, clf):
        '''
        function saves calculated tree into a png file

        IMPORTANT: in order to run this function this packages are required:
        (-) graphviz
        (-) pydotplus

        :return: None
        '''

        # import necessary libraries
        # import necessary libraries

        from sklearn.externals.six import StringIO
        from IPython.display import Image
        from sklearn.tree import export_graphviz
        import pydotplus

        dot_data = StringIO()
        export_graphviz(clf, out_file=dot_data, filled=True, rounded=True, special_characters=True,feature_names=self.featureSetEn, class_names=['0', '1'])
        graph = pydotplus.graph_from_dot_data(dot_data.getvalue())

        #max_depth = 0 if self._decisionTreeMaxDepth < 0 else self._decisionTreeMaxDepth
        #filename = self._dataStorageFilePath + self._dataStorageFileName + '-' + self._decisionTreeCriterium + '-' + str(max_depth) + '.png'
        filename = self._dataStorageFilePath + self._dataStorageFileName + '.png'
        graph.write_png(filename)
        Image(graph.create_png())

        return None

    def binariseVector(self, vector):
        '''
        function convertss vector into a vector with binary values

        :param vector: <class 'pandas.core.series.Series'>
        :return: <class 'pandas.core.series.Series'>
        '''

        binarisedList = []
        for index, value in enumerate(vector):
            binarisedList.append(self.binariseValue(value))
            #vector.replace(to_replace=index, value=self.binariseValue(value))
            #print(index, value, ' => ', vector[index])

        return pd.Series(binarisedList)


    def binariseValue(self, value):
        '''
        function binarises value in ordrer to create binary decision tree

        WARNING! THIS FUNCTION NEEDS TO BE SET MANUALLY!

        :return: 0 or 1
        '''

        if self.feature2explore == 'SkupnaPonudba':
            if value == '2':
                return 1
            else:
                return 0
        elif self.feature2explore == 'StPrejetihPonudb':
            if value == 0 or value == 1:
                return 0
            else:
                return 1

        return 0


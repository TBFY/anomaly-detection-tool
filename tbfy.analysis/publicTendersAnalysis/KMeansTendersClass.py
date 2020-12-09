
'''
On preliminarily created set of data stored in a file, performs various statistical calculations
'''

class KMeansTendersClass:

    def __init__(self, conf, shared):

        self.conf = conf
        self.sharedMethods = shared

        # config vars
        # config vars

        self._dataSourceFilePath    = conf.tenderDataFVPath
        self._dataSourceFileName    = ''
        self._includeFieldsList = []
        self._numOfClusters = -1
        self._fileAppendix = ''

        # data storage variables
        # data storage variables

        self.tenderData = {}
        self.tenderDataFiltered = {}
        self.tenderDataNormVectors = []

        # results variables
        # results variables

        self._dataStorageFilePath = conf.tenderDataResultsPath + 'kMeans/'
        self._selectedDataset = ''
        self._filePrependix = ''

        self.sizeVsDealDict = {}

    def readDataFile(self, statsConfig):
        '''
        Function takes in data stored in self._dataSourceFilePath + self._dataSourceFileName
        and performs various statistical calculations

        :param statsConfig: dict containing config params for the script
        :return: void
        '''

        # import params
        # import params

        self._dataSourceFilePath            = statsConfig['dataSourceFilePath'] if 'dataSourceFilePath' in statsConfig else self._dataSourceFilePath
        self._dataSourceFileName            = statsConfig['dataSourceFileName'] if 'dataSourceFileName' in statsConfig else self._dataSourceFileName
        self._dataStorageFilePath           = statsConfig['dataStorageFilePath'] if 'dataStorageFilePath' in statsConfig else self._dataStorageFilePath
        self._selectedDataset                 = statsConfig['selectedDataset'] if 'selectedDataset' in statsConfig else self._selectedDataset
        self._includeFieldsList             = statsConfig['includeFieldsList'] if 'includeFieldsList' in statsConfig else self._includeFieldsList
        self._numOfClusters                 = statsConfig['numOfClusters'] if 'numOfClusters' in statsConfig else self._numOfClusters
        self._fileAppendix                  = statsConfig['fileAppendix'] if 'fileAppendix' in statsConfig else self._fileAppendix

        clearOldResults = statsConfig['clearOldResults'] if 'clearOldResults' in statsConfig else False

        # file _filePrependix is equal to _selectedDataset if _fileAppendix == ''
        # file _filePrependix is equal to _selectedDataset if _fileAppendix == ''

        if len(self._fileAppendix) == 0:
            self._filePrependix = self._selectedDataset + '-'

        # read data
        # read data

        self.tenderData = self.conf.sharedCommon.readDataFile2Dict(self._dataSourceFilePath + self._dataSourceFileName, "\t")

        # filter unique values out - THIS NEEDS TO BE REWRITTEN
        # filter unique values out - THIS NEEDS TO BE REWRITTEN

        self.filterUniqueDataOut(self._includeFieldsList)

        # standardize data in order to execute an efficient comparison
        # standardize data in order to execute an efficient comparison

        self.standardizeDataBeforeAnalysis()

        # delete all existing files in dir
        # delete all existing files in dir

        if clearOldResults:
            delteFilesList = [f for f in self.conf.os.listdir(self._dataStorageFilePath) if self.conf.os.path.isfile(self.conf.os.path.join(self._dataStorageFilePath, f))]
            for file in delteFilesList:
                fullFileName = self.conf.os.path.join(self._dataStorageFilePath, file)
                self.conf.os.remove(fullFileName)

        return

    def filterUniqueDataOut(self, parameters2Filter):
        '''
        functions filters data according to parameters on parameters2Filter list (discarding unwanted data)

        :return: void
        '''

        # identify data to be retained
        # identify data to be retained

        includeIndexList = []
        for key in parameters2Filter:
            includeIndexList.append(self.tenderData['head'].index(key))

        includeIndexList.sort()

        # create filtered data var
        # create filtered data var

        self.tenderDataFiltered = {}
        self.tenderDataFiltered['head'] = []
        self.tenderDataFiltered['data'] = []

        for index in includeIndexList:
            self.tenderDataFiltered['head'].append(self.tenderData['head'][index])

        for row in self.tenderData['data']:
            curr_row = []
            for index in includeIndexList:
                curr_row.append(row[index])
            self.tenderDataFiltered['data'].append(curr_row)

        return

    def standardizeDataBeforeAnalysis(self):
        '''
        function standardizes data to a range between 0 and 1

        :return: void
        '''

        maxValueList = []
        minValueList = []

        for dataVector in self.tenderDataFiltered['data']:

            # convert to floats
            # convert to floats

            dataVectorFloat = [self.returnFloat(val) for val in dataVector]
            self.tenderDataNormVectors.append(dataVectorFloat)

            # init max and min value vectors
            # init max and min value vectors

            if len(maxValueList) == 0:
                minValueList = dataVectorFloat.copy()
                maxValueList = dataVectorFloat.copy()
                continue

            # update min and max vectors
            # update min and max vectors

            for i,val in enumerate(dataVectorFloat):
                val_min = minValueList[i]
                val_max = maxValueList[i]
                if val < val_min:
                    minValueList[i] = val
                if val > val_max:
                    maxValueList[i] = val

        # having minValueList & maxValueList, normalize self.tenderDataNormVectors
        # having minValueList & maxValueList, normalize self.tenderDataNormVectors

        for i,vector in enumerate(self.tenderDataNormVectors):

            for j,val in enumerate(vector):
                val_min = minValueList[j]
                val_max = maxValueList[j]
                if val_max < 0.000001:
                    # do something with val_max = 0
                    self.tenderDataNormVectors[i][j] = 0.0
                else:
                    self.tenderDataNormVectors[i][j] = (self.tenderDataNormVectors[i][j] - val_min) / val_max

        return

    def analyseClusterTenderVectors(self):
        '''
        function analyses the ratio of tender sum / bidder employee;

        :return: void
        '''

        # is there enough data?
        # is there enough data?

        if len(self.tenderDataNormVectors) < 200:
            return None

        # first, transpose the array of vectors and align it to method requirements
        # first, transpose the array of vectors and align it to method requirements

        transposedVectors = list(map(list, zip(*self.tenderDataNormVectors)))

        data2Analyse = {}
        for i,key in enumerate(self.tenderDataFiltered['head']):
            data2Analyse[key] = transposedVectors[i]

        # import libraries
        # import libraries

        from pandas import DataFrame
        from sklearn.cluster import KMeans

        # identify number of clusters
        # identify number of clusters

        df = DataFrame(data2Analyse, columns=self.tenderDataFiltered['head'])

        if self._numOfClusters > 0:
            optimalK_log = self._numOfClusters
        else:
            # get kmeans inertia for various k value
            # get kmeans inertia for various k value

            kmeansCostList = []
            kmeansXvalues = []
            kMeansMinCentroids = 1
            kMeansMaxCentroids = 20
            for i in range(kMeansMinCentroids, kMeansMaxCentroids):
                #print('kMeans cluster n. ', i)
                kmeans = KMeans(n_clusters=i).fit(df)
                #centroids = kmeans.cluster_centers_
                kmeansCostList.append(kmeans.inertia_)
                kmeansXvalues.append(i)

            # defining optimal k: the intersection if the linear regression curve of first and last 5 points should get a good approximation for the optimalK
            # defining optimal k: the intersection if the linear regression curve of first and last 5 points should get a good approximation for the optimalK

            import math
            kmeansCostList_log = [math.log(x) for x in kmeansCostList if x > 0.0]

            optimalK = round(self.calculateOptimalKneeValue(kmeansCostList))
            optimalK_log = round(self.calculateOptimalKneeValue(kmeansCostList_log, 5, 'log'))

            # save gain values to file
            # save gain values to file

            gainValuesDict = {}
            gainValuesDict['head'] = ['n_clusters', 'gain']
            gainValuesDict['data'] = []
            i = 1
            for value in kmeansCostList:
                curr_list = [str(i), str(value)]
                gainValuesDict['data'].append(curr_list)
                i += 1

            fileName = self._dataStorageFilePath + self._filePrependix + 'cluster-gain-values' + self._fileAppendix + '.tsv'
            self.conf.sharedCommon.sendDict2Output(gainValuesDict, fileName)

            gainValuesLogDict = {}
            gainValuesLogDict['head'] = ['n_clusters', 'gain']
            gainValuesLogDict['data'] = []
            i = 1
            for value in kmeansCostList_log:
                curr_list = [str(i), str(value)]
                gainValuesLogDict['data'].append(curr_list)
                i += 1

            fileName = self._dataStorageFilePath + self._filePrependix + 'cluster-gain-values-log' + self._fileAppendix + '.tsv'
            self.conf.sharedCommon.sendDict2Output(gainValuesLogDict, fileName)

        # optimalK is defined, create clusters
        # optimalK is defined, create clusters

        kmeans = KMeans(n_clusters=optimalK_log).fit(df)
        kmeans_centroids = kmeans.cluster_centers_

        # organise vectors by centorid group
        # organise vectors by centorid group

        # intit cluster members variable
        # intit cluster members variable

        kmeansClustersDistancesDict = {}
        for i in range(len(kmeans_centroids)):
            kmeansClustersDistancesDict[i] = []

        # fill cluster members variable with data: for every vector calculate distance from corresponding centroid
        # fill cluster members variable with data: for every vector calculate distance from corresponding centroid

        clusterLabelsList = list(kmeans.labels_)

        for index, vec in enumerate(self.tenderDataNormVectors):
            # get centroid vector
            centroid_n = clusterLabelsList[index]
            centroid_vec = kmeans_centroids[centroid_n]
            # get cerrent vector
            vec_array = self.conf.numpy.asarray(vec)
            # get distance
            distance = self.conf.numpy.linalg.norm(vec_array - centroid_vec)
            # save data
            row = [index, distance]
            kmeansClustersDistancesDict[centroid_n].append(row)

        # sort kmeansClustersDistancesDict groups by distance value
        # sort kmeansClustersDistancesDict groups by distance value

        for n, curr_list in kmeansClustersDistancesDict.items():
            curr_list.sort(key=lambda x: x[1])
            kmeansClustersDistancesDict[n] = curr_list

        # for every cluster: save 10% most deviating results (the closests and most distant) into a two separate files
        # for every cluster: save 10% most deviating results (the closests and most distant) into a two separate files

        devShare = 0.10
        for n, curr_list in kmeansClustersDistancesDict.items():
            # most distant vectors
            devFurtherest2Save = {}
            devFurtherest2Save['head'] = self.tenderData['head'].copy()
            devFurtherest2Save['data'] = []
            rangeFrom = 0
            rangeTo = int(devShare * len(curr_list))
            for i in range(rangeFrom, rangeTo):
                tmp_index = curr_list[i]
                vector_list = self.tenderData['data'][tmp_index[0]]
                devFurtherest2Save['data'].append(vector_list)

            # MJU data: add company names to dict
            # MJU data: add company names to dict

            if 'NarocnikMaticna' in devFurtherest2Save['head']:
                fieldsDict = {'NarocnikMaticna': 'NarocnikNaziv', 'PonudnikMaticna': 'PonudnikNaziv'}
                devFurtherest2Save = self.sharedMethods.appendMJUOrganizationNames2Dict(devFurtherest2Save, fieldsDict)

            # save to file
            # save to file

            fileName = self._dataStorageFilePath + self._filePrependix + str(n) + '-cluster-closest-deviations' + self._fileAppendix + '.tsv'
            self.conf.sharedCommon.sendDict2Output(devFurtherest2Save, fileName)

            # closest vectors
            devClosest2Save = {}
            devClosest2Save['head'] = self.tenderData['head'].copy()
            devClosest2Save['data'] = []
            rangeFrom = len(curr_list) - int(devShare * len(curr_list))
            rangeTo = len(curr_list)
            for i in range(rangeFrom, rangeTo):
                tmp_index = curr_list[i]
                vector_list = self.tenderData['data'][tmp_index[0]]
                devClosest2Save['data'].append(vector_list)

            # add company names to dict
            # add company names to dict

            if 'NarocnikMaticna' in devClosest2Save['head']:
                fieldsDict = {'NarocnikMaticna': 'NarocnikNaziv', 'PonudnikMaticna': 'PonudnikNaziv'}
                devClosest2Save = self.sharedMethods.appendMJUOrganizationNames2Dict(devClosest2Save, fieldsDict)

            # save to file
            # save to file

            fileName = self._dataStorageFilePath + self._filePrependix + str(n) + '-cluster-closest-deviations' + self._fileAppendix + '.tsv'
            self.conf.sharedCommon.sendDict2Output(devClosest2Save, fileName)

        # save centroids data to file
        # save centroids data to file

        kmeansCentroidsDict = {}
        kmeansCentroidsDict['head'] = ['centroid_n', 'num_of_elements', 'data_source'] + self.tenderDataFiltered['head']
        kmeansCentroidsDict['data'] = []
        i = 0
        for row in kmeans_centroids:
            num_of_centroid_members = len(kmeansClustersDistancesDict[i])
            curr_row = [str(i), str(num_of_centroid_members), str(self._selectedDataset)]
            curr_list = list(row)
            for v in curr_list:
                curr_row.append(str(v))

            kmeansCentroidsDict['data'].append(curr_row)
            i += 1

        fileName = self._dataStorageFilePath + self._filePrependix + 'centroids-coordinates' + self._fileAppendix + '.tsv'
        self.conf.sharedCommon.sendDict2Output(kmeansCentroidsDict, fileName)

        '''
        # save optimal k into a plot
        # save optimal k into a plot

        import matplotlib.pyplot as plt
        plt.axvline(x=optimalK_log)
        #plt.plot(kmeansCostList_log, 'ro')
        plt.scatter(kmeansXvalues, kmeansCostList_log)
        #plt.plot(kmeansCostList_log, 'ro')
        self.conf.plt.title("Search for optimal num of clusters")
        self.conf.plt.xlabel("Num of clusters")
        self.conf.plt.ylabel("kMeans inertia, log scale")
        self.conf.plt.savefig(self._dataStorageFilePath + 'tender-kmeans-optimal-k-log.png')
        plt.clf()
        # plt.show()

        plt.axvline(x=optimalK)
        #plt.plot(kmeansCostList_log, 'ro')
        plt.scatter(kmeansXvalues, kmeansCostList)
        #plt.plot(kmeansCostList_log, 'ro')
        self.conf.plt.title("Search for optimal num of clusters")
        self.conf.plt.xlabel("Num of clusters")
        self.conf.plt.ylabel("kMeans inertia, log scale")
        self.conf.plt.savefig(self._dataStorageFilePath + 'tender-kmeans-optimal-k.png')
        plt.clf()
        '''

        return

    def returnFloat(self, value):
        '''
        function returns float value derived from string value;
        when value cannot be converted into float, return 0.0

        :param value: string
        :return: float
        '''

        try:
            floatValue = float(value)
        except:
            # in order to avoid division by zero or logarithm singularities, return 0.1 instead of 0.0
            floatValue = 0.1

        return floatValue

    def calculateOptimalKneeValue(self, valueList, margin = 5, dataLabel = ''):
        '''
        function calculates linear regression curve out of first margin (default 5) points; the same repeats for
        last margin (default 5) points; the intersection of two linear curves gives a point, where curve breaks 
        
        :param valueList: list
        :param margin: int
        :return: int
        '''

        # prepare data
        # prepare data

        beginningLength = margin - 1
        beginningList = valueList[:beginningLength]
        tailLength = margin + 2
        tailList = valueList[len(valueList) - tailLength:]

        import numpy as np

        xBegList = list(range(1, beginningLength + 1))
        xBegArray = np.asarray(xBegList)
        beginningArray = np.asarray(beginningList)

        xTailList = list(range(1, tailLength + 1))
        xTailArray = np.asarray(xTailList)
        tailArray = np.asarray(tailList)

        # first linear regression
        # first linear regression

        from sklearn import linear_model

        # linear regression equals to y = kx + n where:
        # k = regressionObj.coef_
        # n = regressionObj.intercept_

        regressionObj1 = linear_model.LinearRegression()
        regressionObj1.fit(xBegArray.reshape(-1, 1), beginningArray)
        #print('regression 1: ', regressionObj1.coef_, "x + ", regressionObj1.intercept_)

        regressionObj2 = linear_model.LinearRegression()
        regressionObj2.fit(xTailArray.reshape(-1, 1), tailArray)
        #print('regression 2: ', regressionObj2.coef_, "x + ", regressionObj2.intercept_)

        # getting intersection x
        # getting intersection x

        x = (regressionObj2.intercept_ - regressionObj1.intercept_) / (regressionObj1.coef_ - regressionObj2.coef_)

        if x > 1 and x < len(valueList):
            optimalN = float(x)
        else:
            optimalN = len(valueList) / 2

        # save regression curves data 2 file
        # save regression curves data 2 file

        regressionCurveDict = {}
        regressionCurveDict['head'] = ['curve-id', 'k', 'n', 'intersection_n']
        regressionCurveDict['data'] = []

        dataLList = ['left', str(regressionObj1.coef_[0]), str(regressionObj1.intercept_), str(round(optimalN))]
        dataRList = ['right', str(regressionObj2.coef_[0]), str(regressionObj2.intercept_), str(round(optimalN))]
        regressionCurveDict['data'].append(dataLList)
        regressionCurveDict['data'].append(dataRList)

        if len(dataLabel) > 0:
            dataLabel = '-' + dataLabel

        fileName = self._dataStorageFilePath + self._filePrependix + 'regression-curves-data' + dataLabel + self._fileAppendix + '.tsv'
        self.conf.sharedCommon.sendDict2Output(regressionCurveDict, fileName)

        # return value
        # return value

        return optimalN


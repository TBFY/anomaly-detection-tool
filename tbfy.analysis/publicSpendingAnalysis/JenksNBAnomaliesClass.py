import jenkspy
import statistics

class JenksNBAnomaliesClass:

    def __init__(self, conf, shared):

        self.conf = conf
        self.shared = shared
        self.sharedAnalysis = None

        # define data source / destination
        # define data source / destination

        self.dataSourceFilePath = ''
        self.dataSourceFileName = ''

        self.saveAnomaliesFilePath = self.conf.transactionsDataResultsPath + 'jenks/'
        self.saveAnomaliesFileName = 'jenks-CAT.tsv'

        # define transactions data storage variables
        # define transactions data storage variables

        self.transactionsData = {}
        self.transactionsDataSums = {}
        self.transactionsDataSumsClassified = {}

        # JenksNB storage variables
        # JenksNB storage variables

        self._breaksDeviationFit = 0.2
        self.dataBreaksList = []
        self.dataClusteredList = []
        self.dataBreaksClassifiedList = {}
        self.dataClusteredClassifiedList = {}

        # anomalies storage vars
        # anomalies storage vars

        self.storageDataFilePath = '../data/data2Web/'
        self.anomalyInStdDev = 1.0

        self.anomaliesDict = {}
        self.anomaliesClassifiedDict = {}

    def findAnomaliesThroughJenksNaturalBreaks(self):
        '''
        function clusters data from data sources and finds natural breaks

        :return: None
        '''

        # read data file
        # read data file

        self.readTransactionsFileData(self.dataSourceFilePath + self.dataSourceFileName)

        # break whole list into optimal number of clusters
        # break whole list into optimal number of clusters

        self.dataBreaksList = self.getDataClustersBoundaries(list(self.transactionsDataSums.values()))
        self.dataClusteredList = self.breakData2Clusters(self.transactionsDataSums, self.dataBreaksList)

        # break classified data into clusters
        # break classified data into clusters

        for classifier in self.transactionsDataSumsClassified:
            self.dataClusteredClassifiedList[classifier] = {}
            self.dataBreaksClassifiedList[classifier] = self.getDataClustersBoundaries(list(self.transactionsDataSumsClassified[classifier].values()))
            if len(self.dataBreaksClassifiedList[classifier]) > 0:
                self.dataClusteredClassifiedList[classifier] = self.breakData2Clusters(self.transactionsDataSumsClassified[classifier], self.dataBreaksClassifiedList[classifier])

        # find anomalous values in clusters: select highetst standard deviations from cluster average
        # find anomalous values in clusters: select highetst standard deviations from cluster average

        self.anomaliesDict = self.createAnomaliesList(self.dataClusteredList)
        for classifier in self.dataClusteredClassifiedList:
            self.anomaliesClassifiedDict[classifier] = self.createAnomaliesList(self.dataClusteredClassifiedList[classifier])

        return None

    def getDataClustersBoundaries(self, dataList):
        '''
        function breaks list dataList into optimal number of clusters

        :param dataList: list
        :return: list of floats determining boundaries between clusters
        '''

        initialNumOfBreaks = 2

        # no data - no breaks
        # no data - no breaks

        if len(dataList) < initialNumOfBreaks + 1:
            return []

        # get optimal breaks based on deviation criteria
        # get optimal breaks based on deviation criteria

        numOfBreaksList = self.getOptimalNumberOfBreaks(dataList, self._breaksDeviationFit, initialNumOfBreaks)

        # sometimes deviation criteria is not met, so another search, with new deviation needs to be executed
        # sometimes deviation criteria is not met, so another search, with new deviation needs to be executed

        if(numOfBreaksList[1] < self._breaksDeviationFit):
            newDeviationFit = float(int(100.0 * numOfBreaksList[1] - 2)) / 100.0
            numOfBreaksList = self.getOptimalNumberOfBreaks(dataList, newDeviationFit, initialNumOfBreaks)

        # num of breaks cannot exceed number of data or minimal required breaks
        # num of breaks cannot exceed number of data or minimal required breaks

        if len(dataList) < numOfBreaksList[0] + 1:
            return []

        if numOfBreaksList[0] < initialNumOfBreaks:
            return []

        # all's good - get Jenks Natural Breaks
        # all's good - get Jenks Natural Breaks

        return jenkspy.jenks_breaks(dataList, numOfBreaksList[0])

    def getOptimalNumberOfBreaks(self, dataList, deviationFit, initialNumOfBreaks):
        '''
        function returns the optimal number of breaks and an achieved deviation fit

        :param dataList: list of data to be clusterd
        :param deviationFit: float / allowed deviation
        :param initialNumOfBreaks: int / mininal number of breaks

        :return: two parameter list: [optimal-number-of-breaks, variance]
        '''

        variancefit = 0.0
        variancefit_prev = -1.0
        numOfBreaks = initialNumOfBreaks
        while variancefit < deviationFit:

            if len(dataList) < numOfBreaks + 1:
                return [numOfBreaks - 1, 1.00]

            variancefit = self.goodness_of_variance_fit(dataList, numOfBreaks)

            # prevent endless loop as deviationFit can't be reached
            # prevent endless loop as deviationFit can't be reached

            if (abs(variancefit - variancefit_prev) < 0.001): break
            else:
                variancefit_prev = variancefit
                numOfBreaks += 1

        #print(numOfBreaks, variancefit)
        return [numOfBreaks, variancefit]

    def goodness_of_variance_fit(self, dataList, numOfBreaks):
        '''
        function returns variance, based on provided datalist and number of breaks; in other words,
        function returns how well data fit in a given number of clusters / breaks

        :param dataList: list
        :param numOfBreaks: int
        :return: float
        '''

        # get the break points
        breaksList = jenkspy.jenks_breaks(dataList, numOfBreaks)

        # list that that tells to which cluster value from dataList is assigned
        dataClassified = self.conf.numpy.array([self.assignValueClusterId(element, breaksList) for element in dataList])

        # num of clusters
        numOfClusters = max(dataClassified)

        # nested list of cluster indices
        zone_indices = [[idx for idx, val in enumerate(dataClassified) if zone + 1 == val] for zone in range(numOfClusters)]

        # sum of squared deviations from dataList mean
        sqDevSum = self.conf.numpy.sum((dataList - self.conf.numpy.mean(dataList)) ** 2)

        # sorted polygon stats
        dataClustersList = [self.conf.numpy.array([dataList[index] for index in zone]) for zone in zone_indices]

        # sum of squared deviations of class means
        sqDevClassSum = sum([self.conf.numpy.sum((dataCluster - dataCluster.mean()) ** 2) for dataCluster in dataClustersList])

        # goodness of variance fit
        return (sqDevSum - sqDevClassSum) / sqDevSum

    def assignValueClusterId(self, value, breaks):
        '''
        function assigns given value cluster ID; in other words, it tells in which cluster value belongs to

        :param value: float
        :param breaks: a list of boundaries beteeen clusters
        :return: int / cluster id
        '''

        for i in range(1, len(breaks)):
            if value < breaks[i]:
                return i

        return len(breaks) - 1

    def breakData2Clusters(self, dataDict, breaksList):
        '''
        clusters dataDict into vclusters according boundasries defined in breaksList

        :param dataDict: dictionary of values
        :param breaksList: list of floats / boundaries between clusters
        :return: dictionary of clusters
        '''

        dataList = list(dataDict.values())
        dataKeys = list(dataDict.keys())

        # save data clusters
        # save data clusters

        tmp_dataClassified = self.conf.numpy.array([self.assignValueClusterId(element, breaksList) for element in dataList])
        numOfClusters = max(tmp_dataClassified)
        zone_indices = [[idx for idx, val in enumerate(tmp_dataClassified) if zone + 1 == val] for zone in range(numOfClusters)]

        clustersDict = []
        for zone in zone_indices:
            zone_dict = {}
            for index in zone:
                zone_dict[dataKeys[index]] = dataList[index]

            #print(zone_dict)
            clustersDict.append(zone_dict)

        return clustersDict

    def createAnomaliesList(self, clusterDictsList):
        '''
        function takes in a dictionary of values and returns and list of values, sorted the deviation of a value from
        the cluster average value (normalized by average value)

        :param clusterDictsList: dictionary of values where anomalies are looked for
        :return: dictionary sorted from highest to lowest deviation from cluster average value
        '''

        # no data no funny
        # no data no funny

        if(len(clusterDictsList) == 0):
            return {}

        # analyse every cluster separately
        # analyse every cluster separately

        deviationList = {}
        for cluster in clusterDictsList:
            if len(cluster) < 2:
                return {}

            tmp_dataList = cluster.values()
            mean = statistics.mean(tmp_dataList)
            stdev = statistics.stdev(tmp_dataList)

            for maticna in cluster:
                tmp_deviation = abs(cluster[maticna] - mean) / stdev
                if tmp_deviation > self.anomalyInStdDev:
                    deviationList[maticna] = tmp_deviation

        deviationListOrdered = {k: v for k, v in sorted(deviationList.items(), key=lambda x: x[1], reverse=True)}
        return deviationListOrdered

    def readTransactionsFileData(self, filePath):
        '''
        function reads source file local variables in format:
            publicCompanyId :: privateCompanyId :: [transactions]

        :param filePath: full file path to the data source to be read
        :return: None
        '''

        # abort, if data laready loaded
        # abort, if data laready loaded

        if (len(self.transactionsData) > 0 and len(self.transactionsDataSums) > 0):
            return None

        # read data source line by line
        # read data source line by line

        line_num = 0
        for line in open(filePath):

            # skip first line
            # skip first line

            line_num = line_num + 1
            if line_num == 1:
                continue

            # split line into list
            # split line into list

            tmp_list = line.rstrip('\n').split("\t")

            # init dictionary
            # init dictionary

            maticna_public = tmp_list[0]
            maticna_private = tmp_list[1]
            company_classifier = tmp_list[2]
            num_of_sums = len(tmp_list) - 3

            if company_classifier not in self.transactionsData.keys():
                self.transactionsData[company_classifier] = {}
                self.transactionsDataSumsClassified[company_classifier] = {}
            if maticna_public not in self.transactionsData[company_classifier].keys():
                self.transactionsData[company_classifier][maticna_public] = {}
            if maticna_private not in self.transactionsData[company_classifier][maticna_public].keys():
                self.transactionsData[company_classifier][maticna_public][maticna_private] = [float(0.0)] * num_of_sums
                self.transactionsDataSums[maticna_private] = 0.0
                self.transactionsDataSumsClassified[company_classifier][maticna_private] = 0.0

            # import transactions and their sums
            # import transactions and their sums

            i = 0
            tmp_sum = 0.0
            while (i < num_of_sums):
                self.transactionsData[company_classifier][maticna_public][maticna_private][i] = float(tmp_list[i + 3])
                tmp_sum = tmp_sum + float(tmp_list[i + 3])
                i = i + 1

            self.transactionsDataSums[maticna_private] = self.transactionsDataSums[maticna_private] + tmp_sum
            self.transactionsDataSumsClassified[company_classifier][maticna_private] = self.transactionsDataSumsClassified[company_classifier][maticna_private] + tmp_sum

        return None

    def saveAnomalies2File(self):
        '''
        function saves calculated anomalies to file

        :return: None
        '''

        # convert anomalies to format ready to be written into file
        # convert anomalies to format ready to be written into file

        data2FileDict = {}
        data2FileDict['head'] = ['companyId', 'deviation']
        data2FileDict['data'] = []

        for key, value in self.anomaliesDict.items():
            data2FileDict['data'].append([key, str(value)])

        # enrich data
        # enrich data

        fieldsDict = {'companyId': 'company_name'}
        data2FileDict = self.sharedAnalysis.appendAjpesOrganizationNames2Dict(data2FileDict, fieldsDict)

        # save to file
        # save to file

        fullFilePath = self.saveAnomaliesFilePath
        fullFilePath += self.saveAnomaliesFileName.replace('-CAT', '')
        self.conf.sharedCommon.sendDict2Output(data2FileDict, fullFilePath)

        # repeat process for each classified dataset
        # repeat process for each classified dataset

        for classifier in self.anomaliesClassifiedDict:

            data2FileDict = {}
            data2FileDict['head'] = ['companyId', 'deviation']
            data2FileDict['data'] = []

            for key, value in self.anomaliesClassifiedDict[classifier].items():
                data2FileDict['data'].append([key, str(value)])

            # enrich data
            # enrich data

            fieldsDict = {'companyId': 'company_name'}
            data2FileDict = self.sharedAnalysis.appendAjpesOrganizationNames2Dict(data2FileDict, fieldsDict)

            # save to file
            # save to file

            fullFilePath = self.saveAnomaliesFilePath
            fullFilePath += self.saveAnomaliesFileName.replace('CAT', classifier)
            self.conf.sharedCommon.sendDict2Output(data2FileDict, fullFilePath)

        return None

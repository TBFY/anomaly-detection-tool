
'''
On preliminarily created set of data stored in a file, class methods perform various statistical calculations
'''

class RatiosTendersClass:

    def __init__(self, conf, shared):

        self.conf = conf
        self.sharedMethods = shared

        # config vars
        # config vars

        self._dataSourceFilePath    = self.conf.tenderDataFVPath
        self._dataSourceFileName    = ''
        self._dataSourceType = ''
        self._ratioCategoryDir = ''
        self._fields2Store = ''

        # data storage variables
        # data storage variables

        self.featureVectorData = {}

        # results variables
        # results variables

        self._dataStorageFilePath = ''
        self._dataStorageFileName = ''

        self.sizeVsDealDict = {}

    def readDataFile(self, ratiosConfig):
        '''
        Function takes in data stored in self._dataSourceFilePath + self._dataSourceFileName
        and performs various statistical calculations

        :param ratiosConfig: dict containing config params for the script
        :return: None
        '''

        # import params
        # import params

        self._dataSourceFilePath = ratiosConfig['dataSourceFilePath'] if 'dataSourceFilePath' in ratiosConfig else self._dataSourceFilePath
        self._dataSourceFileName = ratiosConfig['dataSourceFileName'] if 'dataSourceFileName' in ratiosConfig else self._dataSourceFileName
        self._dataStorageFilePath = ratiosConfig['dataStorageFilePath'] if 'dataStorageFilePath' in ratiosConfig else self._dataStorageFilePath
        self._dataStorageFileName = ratiosConfig['dataStorageFileName'] if 'dataStorageFileName' in ratiosConfig else self._dataStorageFileName
        self._ratioCategoryDir = ratiosConfig['ratioCategoryDir'] if 'ratioCategoryDir' in ratiosConfig else self._dataStorageFileName
        self._dataSourceType = ratiosConfig['dataSourceType'] if 'dataSourceType' in ratiosConfig else self._dataSourceType
        self._fields2Store = ratiosConfig['fields2Store'] if 'fields2Store' in ratiosConfig else self._dataSourceType

        # create full data storage path
        # create full data storage path

        self._dataStorageFilePath = self.conf.os.path.join(self._dataStorageFilePath, self._ratioCategoryDir + '/')
        if not self.conf.os.path.isdir(self._dataStorageFilePath):
            self.conf.os.makedirs(self._dataStorageFilePath)

        # read data
        # read data

        self.featureVectorData = self.conf.sharedCommon.readDataFile2Dict(self._dataSourceFilePath + self._dataSourceFileName, "\t")

        return None

    def removeZeroValuesRecords(self, dictionary, denominatorKey):
        '''
        functions remobves all records in dictionary with denominatorKey = 0

        :param dictionary: dictionary
        :param denominatorKey: name of the filed that needs to be bigger than 0
        :return: dictionary with removed records
        '''

        # init new dictionary
        # init new dictionary

        returnDict = {}
        returnDict['head'] = dictionary['head'].copy()
        returnDict['data'] = []

        # select valid records
        # select valid records

        denominatorKey_n = returnDict['head'].index(denominatorKey)
        for vector in dictionary['data']:
            if float(vector[denominatorKey_n]) < 0.01:
                continue
            # add valid record
            returnDict['data'].append(vector)

        return returnDict

    def analyseSizeVsDealRatioByTender(self, buyerIdKey_string, bidderIdKey_string, numeratorKey, denominatorKey):
        '''
        function calculates [tender-sum / bidder-employee-num] ratio for every tender

        :return: None
        '''

        # step 0: remove 0 employees records
        # step 0: remove 0 employees records

        self.featureVectorData = self.removeZeroValuesRecords(self.featureVectorData, denominatorKey)
        self.featureVectorData = self.removeZeroValuesRecords(self.featureVectorData, numeratorKey)

        # step 1: calculate all ratios and sort from highest to lowest ratio
        # step 1: calculate all ratios and sort from highest to lowest ratio

        tenderValuesRatioList = []
        denominatorKey_n = self.featureVectorData['head'].index(denominatorKey)
        numeratorKey_n = self.featureVectorData['head'].index(numeratorKey)
        for dataList in self.featureVectorData['data']:
            denominatorValue = float(dataList[denominatorKey_n])
            # store data
            tenderValue = float(dataList[numeratorKey_n])
            tenderValuesRatioList.append(tenderValue/denominatorValue)

        # sort ratios
        # sort ratios

        reorderedIndexList = [reorderedIndexList[0] for reorderedIndexList in sorted(enumerate(tenderValuesRatioList), key=lambda i: i[1])]
        reorderedIndexList.reverse()

        # calculate all necessary points logs etc.
        # calculate all necessary points logs etc.

        import math
        import statistics

        xValues = []
        xLogValues = []
        for index in reorderedIndexList:
            # avoid zero to be passed to logarithm
            value = tenderValuesRatioList[index] + 0.001
            value_log = math.log(value)
            # assemble lists
            xValues.append(value)
            xLogValues.append(value_log)

        # save data to file: split list into 1000 points and average value for every point subset
        # save data to file: split list into 1000 points and average value for every point subset

        subsetSize = math.ceil(len(xValues) / 200)

        i = 0
        yGraphPointsList = []
        x = 1
        while i < len(xValues):
            tmp_subset = xLogValues[i:i + subsetSize]
            mean_value = statistics.mean(tmp_subset)
            yGraphPointsList.append([str(x), str(mean_value)])
            i += subsetSize
            x += 1

        # save aggregated and averaged values to file
        # save aggregated and averaged values to file

        graphValuesDict = {}
        graphValuesDict['head'] = ['x_value', 'y_value']
        graphValuesDict['data'] = yGraphPointsList
        graphValuesFileName = self._dataStorageFilePath + self._dataStorageFileName + '-data-values.tsv'
        self.conf.sharedCommon.sendDict2Output(graphValuesDict, graphValuesFileName)

        # linear fit on xLogValues; 7% of initial and final data are removed as considered extreme deviations
        # linear fit on xLogValues; 7% of initial and final data are removed as considered xetreme deviations

        numOfDeviationvalues = int(0.07 * len(xLogValues))
        if numOfDeviationvalues < 2:
            numOfDeviationvalues = int(0.3 * len(xLogValues))

        if numOfDeviationvalues > 0:
            linearReegressiondataList_Y = xLogValues[:-numOfDeviationvalues]
            linearReegressiondataList_Y = linearReegressiondataList_Y[numOfDeviationvalues:]
            linearReegressiondataList_X = self.conf.numpy.arange(numOfDeviationvalues, len(linearReegressiondataList_Y) + numOfDeviationvalues).reshape(-1,1)

            from sklearn import datasets, linear_model

            regressionObj = linear_model.LinearRegression()
            regressionObj.fit(linearReegressiondataList_X, linearReegressiondataList_Y)

        # save linear fit to file
        # save linear fit to file

        linearFit = {}
        linearFit['head'] = ['k', 'n']
        #print(str(regressionObj.coef_[0]), str(regressionObj.intercept_))
        linearFit['data'] = []
        if numOfDeviationvalues > 0:
            linearFit['data'].append([str(regressionObj.coef_[0]), str(regressionObj.intercept_)])
        else:
            linearFit['data'].append(['0', '0'])
        linearFitFileName = self._dataStorageFilePath + self._dataStorageFileName + '-linear-fit.tsv'
        self.conf.sharedCommon.sendDict2Output(linearFit, linearFitFileName)

        # save anomalies into file
        # save anomalies into file

        deviationsPosDict = {}
        deviationsPosDict['head'] = list(self._fields2Store.keys())
        deviationsPosDict['data'] = []
        deviationsNegDict = {}
        deviationsNegDict['head'] = list(self._fields2Store.keys())
        deviationsNegDict['data'] = []

        indexList2AccessValues = []
        for key,value in self._fields2Store.items():
            # skip numericals
            if key == 'x_val' or key == 'y_value':
                continue
            # add value index
            index_n = self.featureVectorData['head'].index(value)
            indexList2AccessValues.append(index_n)

        valueListLength = len(reorderedIndexList)
        i = 0
        while i < numOfDeviationvalues:
            i += 1

            # create positive deviation record
            # create positive deviation record

            x_value = str(i)
            y_value = str(xLogValues[i])

            index = reorderedIndexList[i]
            row = self.featureVectorData['data'][index]
            tmp_vector = [x_value, y_value]
            for curr_index in indexList2AccessValues:
                tmp_vector.append(row[curr_index])

            deviationsPosDict['data'].append(tmp_vector)

            # create negative deviation record
            # create negative deviation record

            index_n = valueListLength - numOfDeviationvalues + i - 1
            x_value = str(i)
            y_value = str(xLogValues[index_n])

            index = reorderedIndexList[index_n]
            row = self.featureVectorData['data'][index]

            tmp_vector = [x_value, y_value]
            for curr_index in indexList2AccessValues:
                tmp_vector.append(row[curr_index])

            deviationsNegDict['data'].insert(0, tmp_vector)

        # enrich analysis data
        # enrich analysis data

        if self._dataSourceType == 'mju':
            fieldsDict = {'buyerId': 'buyerName', 'bidderId': 'bidderName'}
            deviationsPosDict = self.sharedMethods.appendMJUOrganizationNames2Dict(deviationsPosDict, fieldsDict)
            deviationsNegDict = self.sharedMethods.appendMJUOrganizationNames2Dict(deviationsNegDict, fieldsDict)
        else:
            # add currency names to file
            fieldsList = []
            fieldsDict = {}
            fieldsDict['dataColumnName'] = 'currency'
            fieldsDict['mapFileId'] = 'currency'
            fieldsDict['newColumnName'] = 'currency_name'
            fieldsList.append(fieldsDict)
            deviationsPosDict = self.sharedMethods.appendTBFYKGFieldMapValue(deviationsPosDict, fieldsList)
            deviationsNegDict = self.sharedMethods.appendTBFYKGFieldMapValue(deviationsNegDict, fieldsList)

        # save deviations to file
        # save deviations to file

        deviationsFileName = self._dataStorageFilePath + self._dataStorageFileName + '-pos-deviations.tsv'
        self.conf.sharedCommon.sendDict2Output(deviationsPosDict, deviationsFileName)

        deviationsFileName = self._dataStorageFilePath + self._dataStorageFileName + '-neg-deviations.tsv'
        self.conf.sharedCommon.sendDict2Output(deviationsNegDict, deviationsFileName)

        return None

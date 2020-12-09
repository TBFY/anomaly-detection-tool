
'''
This class performs various distribution comparisons. The initial idea of creating a general comparison of
overall distribution to the distribution for a given company for a given value by applying a Kolmogorov-Smirnov distance
was rejected as individual companies didin't encompass big enough sample size to obtain relevant individual distribution.

Instead, a set of simplified custom analysis for various variables were developed:

(1) Examining number of offers. Logic behind calculating anomaly value:
    - first create a list with three elements: [0, 0, 0]
    - then iterate through tenders:
        (.) if tender received one offer, increase first value [0, 0, 0] => [1, 0, 0]
        (.) if tender received two offers, increase second value [0, 0, 0] => [0, 1, 0]
        (.) if tender received three offers or more, increase third value [0, 0, 0] => [0, 0, 1]
    - then, values in [x, y, z] are normalized (divided by num of tenders) for condition: (x + y + z) = 1 (or 100%) holds
    - repeat procedure for every company's tenders
    - now one is able to compare every company's [x_i, y_i, z_i] distribution to overall distribution [x, y, z] with formula (for more details check "calculateDeltaValueNumOfOffers" function):
        anomaly = (x_i - x) + 0.1 * (y_i - y) + (z_i - z)
    - companies having [1, 0, 0] distribution are the most anomalous (minimum), while companies with [0, 0, 1] are among most healthy companies (maximum)

(2) Examining assessed and approved budget values. Logic behind calculating anomaly value:
    - first, calculate all differences between assessed and final tender value
    - the differences should be distributed according normal distribution
    - normalize normal distribution (in order to make it comparable to other normalized distributions)
    - calculate standard deviation of a normalized distribution
    - then repeat the process for every company's tenders
    - at this point, one should have a benchmark (std deviation of a normal distribution for all tender differneces) and a value to compare to benchmark - single company's standard deviation
    - the two values are then substracted.
As we are calculating distributions for all tenders as well as groups of tenders according their CPV, the idea is to make this diferences comparable over various groups.
This can be done in two ways:
    - First approach:
        (.) the differences are divided by the value of the benchmark:
            * 0 => ideal company's behaviour
            * 1 => company's assessed values always exactly macth final tender value, which is a suspicious behaviour
            * negative values => the more values are negative the more the company's tenders were misassessed
    - Second approach:
        (.) the differences are stripped of their internal mean value:
            mean = mean value of given differences
            new-difference = (difference - mean) / mean
The differnece between the two:
- is a diferent x scale
- in case of few featurevectors, the second method is can significantly exceed value 1.
'''

import statistics

class DistributionsTendersClass:

    def __init__(self, conf, shared):

        self.conf = conf
        self.sharedMethods = shared

        # config vars
        # config vars

        self._dataSourceFilePath = self.conf.tenderDataFVPath
        self._dataSourceFileName = ''
        self._dataStorageFilePath = ''
        self._dataStorageFileName = ''

        self._variableFieldName = ''
        self._companyIdFieldName = ''
        self._cpvFieldName = ''
        self._distributonCategoryDir = ''
        self._dataSourceType = ''

        # method specific variables - budget distribution
        # method specific variables - budget distribution

        # possible values:
        #   * 'norm-to-benchmark'
        #   * 'norm-to-mean'

        self.budgetAssessAnomalousValueMethod = 'norm-to-mean'

        # data storage variables
        # data storage variables

        self.featureVectorData = {}
        self.featureVectorDataByCompanyId = {}
        self.commonValueDistribution = []
        self.commonDistributionMaxValue = 0.0
        self.commonDistributionMinValue = 0.0

        self.featureVectorDataClassified = {}
        self.featureVectorDataByCompanyIdClassified = {}
        self.commonValueDistributionClassified = {}

        # results
        # results

        self.resultsDict = {}
        self.resultsClassifiedDict = {}

        # monitoring variable
        # monitoring variable

        self.printData = False

    def setAnalysisParameters(self, distributionConfig):
        '''
        Function gets parameters, determining this analysis

        :param distributionConfig: dict containing config params for analysis
        :return: None
        '''

        # import params
        # import params

        self._dataSourceFilePath = distributionConfig['dataSourceFilePath'] if 'dataSourceFilePath' in distributionConfig else self._dataSourceFilePath
        self._dataSourceFileName = distributionConfig['dataSourceFileName'] if 'dataSourceFileName' in distributionConfig else self._dataSourceFileName
        self._dataStorageFilePath = distributionConfig['dataStorageFilePath'] if 'dataStorageFilePath' in distributionConfig else self._dataStorageFilePath
        self._dataStorageFileName = distributionConfig['dataStorageFileName'] if 'dataStorageFileName' in distributionConfig else self._dataStorageFileName
        self._distributonCategoryDir = distributionConfig['distributonCategoryDir'] if 'distributonCategoryDir' in distributionConfig else self._distributonCategoryDir
        self._cpvFieldName = distributionConfig['cpvFieldName'] if 'cpvFieldName' in distributionConfig else self._cpvFieldName

        self._variableFieldName = distributionConfig['variableFieldName'] if 'variableFieldName' in distributionConfig else self._variableFieldName
        self._companyIdFieldName = distributionConfig['companyIdFieldName'] if 'companyIdFieldName' in distributionConfig else self._companyIdFieldName
        self._dataSourceType = distributionConfig['dataSourceType'] if 'dataSourceType' in distributionConfig else self._dataSourceType

        # if not yet existing, create full data storage path
        # if not yet existing, create full data storage path

        self._dataStorageFilePath = self.conf.os.path.join(self._dataStorageFilePath, self._distributonCategoryDir + '/')

        if not self.conf.os.path.isdir(self._dataStorageFilePath):
            self.conf.os.makedirs(self._dataStorageFilePath)

        return None

    def compareData2CommonDistribution(self):
        '''
        This is main function for distributions analysis.

        :return: None
        '''

        #print(self._distributonCategoryDir)

        # read feature vector file data
        # read feature vector file data

        self.readFVDataFile()

        # create common distribution histogram
        # create common distribution histogram

        self.commonValueDistribution = self.createValueDistribution(self.featureVectorData['data'])

        for cpvCode,vectorList in self.featureVectorDataClassified.items():
            if len(vectorList) < 2:
                continue

            self.commonValueDistributionClassified[cpvCode] = self.createValueDistribution(vectorList)

        # compare every company distribution to common distribution and identify greatests anomalies
        # compare every company distribution to common distribution and identify greatests anomalies

        self.resultsDict = self.compareComanyDistribution2CommonDistribution(self.featureVectorDataByCompanyId, self.commonValueDistribution)

        for cpvCode,classifiedByCompanyId in self.featureVectorDataByCompanyIdClassified.items():
            distribution = self.commonValueDistributionClassified[cpvCode]
            self.resultsClassifiedDict[cpvCode] = self.compareComanyDistribution2CommonDistribution(classifiedByCompanyId, distribution)

        # manipulate results
        # manipulate results

        self.resultsDict = self.manipulateResults(self.resultsDict, self.commonValueDistribution)

        for cpvCode, resultsDict in self.resultsClassifiedDict.items():
            # problem v manipulateResults funkciji
            self.resultsClassifiedDict[cpvCode] = self.manipulateResults(resultsDict, self.commonValueDistributionClassified[cpvCode])

        #print(self.resultsClassifiedDict['30'])

        # save anomalies to file
        # save anomalies to file

        self.saveAnomalies2File(self.commonValueDistribution, self.resultsDict)

        for cpvCode, resultsDict in self.resultsClassifiedDict.items():
            distribution = self.commonValueDistributionClassified[cpvCode]
            self.saveAnomalies2File(distribution, resultsDict, cpvCode)

        return None

    def readFVDataFile(self):
        '''
        Function reads feature vector data file into self.featureVectorData variable

        :return:
        '''

        # read feature vecor data file
        # read feature vecor data file

        self.featureVectorData = self.conf.sharedCommon.readDataFile2Dict(self._dataSourceFilePath + self._dataSourceFileName, "\t")

        # organize data by company ID
        # organize data by company ID

        self.featureVectorDataByCompanyId = {}
        companyId_index = self.featureVectorData['head'].index(self._companyIdFieldName)
        for row in self.featureVectorData['data']:
            companyId = row[companyId_index]
            if companyId not in self.featureVectorDataByCompanyId:
                self.featureVectorDataByCompanyId[companyId] = []

            self.featureVectorDataByCompanyId[companyId].append(row)

        # classify file data by cpv code
        # classify file data by cpv code

        cpv_index = self.featureVectorData['head'].index(self._cpvFieldName)
        for row in self.featureVectorData['data']:
            cpvNum = str(row[cpv_index])
            if len(cpvNum) == 1:
                cpvNum = '0' + cpvNum

            if cpvNum not in self.featureVectorDataClassified:
                self.featureVectorDataClassified[cpvNum] = []

            self.featureVectorDataClassified[cpvNum].append(row)

        # organize classified data by cpv and company ID
        # organize classified data by cpv and company ID

        self.featureVectorDataByCompanyIdClassified = {}
        companyId_index = self.featureVectorData['head'].index(self._companyIdFieldName)
        for row in self.featureVectorData['data']:
            cpvNum = str(row[cpv_index])
            if len(cpvNum) == 1:
                cpvNum = '0' + cpvNum

            if cpvNum not in self.featureVectorDataByCompanyIdClassified:
                self.featureVectorDataByCompanyIdClassified[cpvNum] = {}

            companyId = row[companyId_index]
            if companyId not in self.featureVectorDataByCompanyIdClassified[cpvNum]:
                self.featureVectorDataByCompanyIdClassified[cpvNum][companyId] = []

            self.featureVectorDataByCompanyIdClassified[cpvNum][companyId].append(row)

        return None

    def createValueDistribution(self, rowList):
        '''

        :param rowList: list of feature vectors containing value
        :return: custom distribution list
        '''

        # custom distributions are variable-custom made
        # custom distributions are variable-custom made

        if self._variableFieldName == 'StPrejetihPonudb':
            valueList = self.returnValueListNumOfOffers(rowList)
            return self.createValueDistributionNumOfOffers(valueList)
        elif self._variableFieldName == 'OcenjenaVrednostSorazmerno,KoncnaVrednostSorazmerno':
            valueList = self.returnValueListBudgetAssessment(rowList)
            return self.createValueDistributionBudgetAssessment(valueList)
        else:
            # here new variableList list functions
            return []

    def compareComanyDistribution2CommonDistribution(self, dataByCompanyId, commonDistribution):
        '''
        This function compares company's distribution profiles to variable common distribution profile

        :return: None
        '''

        # init results storage var
        # init results storage var

        resultsDict = {}
        resultsDict['head'] = ['deltavalue', 'bidder_id', 'bidder_distr', 'occurence_num']
        resultsDict['data'] = []

        for companyId, rowList in dataByCompanyId.items():
            # rowList is a list of lots won by the company
            rowListLen = len(rowList)
            if rowListLen == 0:
                continue
            # get distribution for a given company
            curr_distribution = self.createValueDistribution(rowList)
            if len(curr_distribution) == 0:
                continue
            if rowListLen > 5:
                # get delta value
                # get delta value

                deltaValue = self.calculateDeltaValue(curr_distribution, commonDistribution)

                # save to dict
                # save to dict

                tmp_row = []
                tmp_row.append(deltaValue)
                tmp_row.append(companyId)
                tmp_row.append('-'.join(str(x) for x in curr_distribution))
                tmp_row.append(str(rowListLen))

                resultsDict['data'].append(tmp_row)

                # print('delta value:', deltaValue)
                # print('custom:', curr_distribution)
                # print('common: ', self.commonValueDistribution)

        return resultsDict

    def calculateDeltaValue(self, distribution, commonDistribution):
        '''
        the idea of this function is to return a value that would assess the relation between two distributions:
        - the more the value positive, the more is benefitial the change compared to common distribution
        - the more the value negative, the less is benefitial the change compared to common distribution
        - 0.0 delta value means, that the distribution is equal to common distribution

        :param distribution: list of values
        :return: float
        '''

        if self._variableFieldName == 'StPrejetihPonudb':
            return self.calculateDeltaValueNumOfOffers(distribution, commonDistribution)
        elif self._variableFieldName == 'OcenjenaVrednostSorazmerno,KoncnaVrednostSorazmerno':
            return self.calculateDeltaValueBudgetAssessment(distribution, commonDistribution)
        else:
            # here new variableList list functions
            return -10.0

    def manipulateResults(self, resultsDict, resultsDictValuesDistribution):
        '''
        The class idea is to compare company parameters to overall parameters. But what if, one would need to compare
        company's parameters to averaged companies parameters? This function is doing exactly that.

        :return: None
        '''

        if self._variableFieldName == 'OcenjenaVrednostSorazmerno,KoncnaVrednostSorazmerno':
            return self.manipulateResultsBudgetAssessment(resultsDict, resultsDictValuesDistribution)

        return resultsDict

    def saveAnomalies2File(self, distribution, resultsDict, cpvCode = ''):
        '''
        This function saves anomalies to file

        :return: None
        '''

        # first, anomalies need to be sorted by deltavalue
        # first, anomalies need to be sorted by deltavalue

        resultsDict['data'].sort(key=lambda x: x[0])

        # convert all values to string
        # convert all values to string

        resultsDict['data'] = [[str(j) for j in i] for i in resultsDict['data']]

        # create positive / negative deviations data storage
        # create positive / negative deviations data storage

        numOfRows = len(resultsDict['data'])
        if numOfRows > 200:
            # taking out 25% of most deviating hits
            numOfDeviatinResults = int(numOfRows * 0.25)
        else:
            # half of the hits go to positive devs, half to negative
            numOfDeviatinResults = int(numOfRows / 2)

        resultsNegDict = {}
        resultsNegDict['head'] = resultsDict['head'].copy()
        resultsNegDict['data'] = resultsDict['data'][:numOfDeviatinResults]

        resultsPosDict = {}
        resultsPosDict['head'] = resultsDict['head'].copy()
        resultsPosDict['data'] = resultsDict['data'][-numOfDeviatinResults:]
        resultsPosDict['data'].reverse()

        # create common distribution file
        # create common distribution file

        cmnDistrDict = {}
        cmnDistrDict['head'] = ['common_distribution']
        tmp_row = []
        tmp_row.append('-'.join(str(x) for x in distribution))
        cmnDistrDict['data'] = [tmp_row]

        # enrich analysis data
        # enrich analysis data

        if self._dataSourceType == 'mju':
            fieldsDict = {'bidder_id': 'bidder_name'}
            resultsNegDict = self.sharedMethods.appendMJUOrganizationNames2Dict(resultsNegDict, fieldsDict)
            resultsPosDict = self.sharedMethods.appendMJUOrganizationNames2Dict(resultsPosDict, fieldsDict)
            resultsAllDict = self.sharedMethods.appendMJUOrganizationNames2Dict(resultsDict, fieldsDict)

        # save to file
        # save to file

        allDataFileName = self._dataStorageFilePath + self._dataStorageFileName + '-data-values.tsv'
        allDataFileName = allDataFileName.replace('CPV', cpvCode)
        self.conf.sharedCommon.sendDict2Output(resultsAllDict, allDataFileName)

        deviationsFileName = self._dataStorageFilePath + self._dataStorageFileName + '-neg-deviations.tsv'
        deviationsFileName = deviationsFileName.replace('CPV', cpvCode)
        self.conf.sharedCommon.sendDict2Output(resultsNegDict, deviationsFileName)

        deviationsFileName = self._dataStorageFilePath + self._dataStorageFileName + '-pos-deviations.tsv'
        deviationsFileName = deviationsFileName.replace('CPV', cpvCode)
        self.conf.sharedCommon.sendDict2Output(resultsPosDict, deviationsFileName)

        distrFileName = self._dataStorageFilePath + self._dataStorageFileName + '-cmn-distribution.tsv'
        distrFileName = distrFileName.replace('CPV', cpvCode)
        self.conf.sharedCommon.sendDict2Output(cmnDistrDict, distrFileName)

        # save to file all data
        # save to file all data

        # xValues = [[item[0]] for item in resultsDict['data']]

        # graphValuesDict = {}
        # graphValuesDict['head'] = ['deltavalue']
        # graphValuesDict['data'] = xValues
        # graphValuesFileName = self._dataStorageFilePath + self._dataStorageFileName + '-data-values.tsv'
        # self.conf.sharedCommon.sendDict2Output(graphValuesDict, graphValuesFileName)

        return None

    ############ START [num-of-offers] custom functions ############
    ############ START [num-of-offers] custom functions ############

    def returnValueListNumOfOffers(self, rowList):
        '''
        Function creates a list of values. It allows only three values:
        - one offer (1),
        - two offers (2)
        - three offers and more (3)
        The idea of allowing only three values lies in:
        - focus is set on a question: was there was only one or more?
        - and by narrowing down the options, it increases the accuracy of the distribution due to lack of data for a single company

        :return: list of values
        '''

        valueList = []
        variable_index = self.featureVectorData['head'].index(self._variableFieldName)
        for row in rowList:
            curr_value_str = row[variable_index]
            if curr_value_str == '0':
                continue
            elif curr_value_str == '1' or curr_value_str == '2':
                valueList.append(int(curr_value_str))
            else:
                valueList.append(3)

        return valueList

    def createValueDistributionNumOfOffers(self, valueList, defineAbsoluteRange=False):
        '''
        Function gets in a list of values and returns a distribution of values.

        :param valueList: list, list of values to be histogramized
        :param valueRange: list with two values: minimum and maximum value from the valueList
        :return: distribution values
        '''

        if len(valueList) == 0:
            return []

        # absolute range is defined with common dataset
        # absolute range is defined with common dataset

        if defineAbsoluteRange:
            self.commonDistributionMaxValue = 3
            self.commonDistributionMinValue = 1

        # sort valueList values into a histogramList
        # sort valueList values into a histogramList

        distributionList = [0, 0, 0]
        unitValue = 100 / len(valueList)
        for value in valueList:
            index = value -1
            distributionList[index] += unitValue

        return [int(round(elem, 0)) for elem in distributionList]

    def calculateDeltaValueNumOfOffers(self, distribution, commonDistribution):
        '''
        Function returns deltaValue, assessing comparison between distribution and distribution.
        DeltaValue is calculated this way:
        - penalizes, if custom share exceeds common share for 1 offer
        - is neutral fo changes for two offers
        - rewards, if custom share exceeds common share for 3 or more offers

        :param distribution:
        :return: float
        '''

        oneOfferKoeff = 1.0
        oneOfferValue = commonDistribution[0] - distribution[0]
        twoOfferKoeff = 0.1
        twoOfferValue = distribution[1] - commonDistribution[1]
        triOfferKoeff = 1.0
        triOfferValue = distribution[2] - commonDistribution[2]

        deltaValue = oneOfferKoeff * oneOfferValue + twoOfferKoeff * twoOfferValue + triOfferKoeff * triOfferValue
        return deltaValue

    ############ END [num-of-offers] custom functions ############
    ############ END [num-of-offers] custom functions ############

    ############ START [budget-assessment] custom functions ############
    ############ START [budget-assessment] custom functions ############

    def returnValueListBudgetAssessment(self, rowList):
        '''
        Function creates a list of values. It allows only three values:
        - one offer (1),
        - two offers (2)
        - three offers and more (3)
        The idea of allowing only three values lies in:
        - focus is set on a question: was there was only one or more?
        - and by narrowing down the options, it increases the accuracy of the distribution due to lack of data for a single company

        :return: list of values
        '''

        valueList = []

        fieldNameList =  self._variableFieldName.split(',')
        assessed_value_index = self.featureVectorData['head'].index(fieldNameList[0])
        final_value_index = self.featureVectorData['head'].index(fieldNameList[1])

        for row in rowList:
            curr_value_str = float(row[assessed_value_index]) - float(row[final_value_index])
            valueList.append(curr_value_str)

        return valueList

    def createValueDistributionBudgetAssessment(self, valueList):
        '''
        Function gets in a list of values and returns a distribution of values.

        :param valueList: list, list of values to be histogramized
        :param valueRange: list with two values: minimum and maximum value from the valueList
        :return: distribution values
        '''

        if len(valueList) < 2:
            return [0.0]

        # norm by (x - mean) / range
        # norm by (x - mean) / range

        max_x = max(valueList)
        min_x = min(valueList)
        mean = statistics.mean(valueList)
        delta = max_x - min_x

        if delta < 0.0000001:
            return [0.0]

        normalList = [(x - mean)/delta for x in valueList]
        stdev = statistics.stdev(normalList)

        return [stdev]

    def calculateDeltaValueBudgetAssessment(self, distribution, commonDistribution):
        '''
        Function returns deltaValue, assessing comparison between distribution and distribution.
        DeltaValue is a diiference of:
        - common standard deviayion
        - company's standard deviation

        Ideally, one would want the difference to be 0 because:
        - if case the difference is positive, the assessed budget is being too well assessed
        - if case the difference is negative, the assessed budget is being lousily assessed

        :param distribution:
        :return: float
        '''

        deltaValue = commonDistribution[0] - distribution[0]
        return deltaValue

    def manipulateResultsBudgetAssessment(self, resultsDict, resultsDictValuesDistribution):
        '''
        Function takes in resultsDict and replaces deltavalue, which is at position 0 at every row in  resultsDict['data']

        :return: resultsDict
        '''

        if len(resultsDict['data']) == 0:
            return resultsDict

        # FIRST APPROACH: normalizing to benchmark value (std deviation of all considered tenders)
        # FIRST APPROACH: normalizing to benchmark value (std deviation of all considered tenders)

        if self.budgetAssessAnomalousValueMethod == 'norm-to-benchmark':

            dataSigma = resultsDictValuesDistribution[0]
            if abs(dataSigma) < 0.00000000001:
                return resultsDict

            for i in range(len(resultsDict['data'])):
                resultsDict['data'][i][0] = resultsDict['data'][i][0] / dataSigma

        # SECOND APPROACH: center distribution to 0 in order to be comparable to other distributions
        # SECOND APPROACH: center distribution to 0 in order to be comparable to other distributions

        if self.budgetAssessAnomalousValueMethod == 'norm-to-mean':

            # collect all delta values
            # collect all delta values

            dataList = []
            for row in resultsDict['data']:
                dataList.append(row[0])

            # replace delta-value by (mean - delta-valiue) / mean
            # replace delta-value by (mean - delta-valiue) / mean

            mean = statistics.mean(dataList)

            # avoid if mean == 0
            if abs(mean) > 0.00000000001:
                for i in range(len(resultsDict['data'])):
                    resultsDict['data'][i][0] = (mean - resultsDict['data'][i][0]) / mean

        return resultsDict

    ############ END [budget-assessment] custom functions ############
    ############ END [budget-assessment] custom functions ############

    ############ additional functions ############
    ############ additional functions ############

    def removeOutliersFromTheList(self, valueList):
        '''
        The problem is: imagine a list with values between 1 and 10 - and one outlier with value 100. If you'd want
        to normalize value list to a range between 1 and 10 (what noramlly happens in histogram), you'd be getting
        all values but one concentrated in field 1 wit all the other filed equal to zero (except the last one). The
        value distribution would be lost.

        :param valueList: list of values
        :return: list of values stripped of outliers
        '''

        # preserve only values that are within m standard deviations from mean
        # preserve only values that are within m standard deviations from mean

        m = 2.0
        mean = self.conf.numpy.mean(valueList)
        # avoid stdd being zero, in case all values are equal
        stdd = self.conf.numpy.std(valueList) + 1.0
        return [e for e in valueList if abs(e - mean) < m * stdd]
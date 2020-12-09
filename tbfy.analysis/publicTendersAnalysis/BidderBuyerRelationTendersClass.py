
'''
This class examines how bidders and buyers are connected. It calculates a share of a single bidder in overall buyer budget
as well as buyer's share in bidders overall revenue. Then it calculates mutual connections between bidders and buyers.
'''

class BidderBuyerRelationTendersClass:

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
        self._buyerIdFieldName = ''
        self._bidderIdFieldName = ''
        self._cpvFieldName = ''
        self._dataSourceType = ''

        # data storage variables
        # data storage variables

        self.featureVectorData = {}
        self.featureVectorDataByBidderId = {}
        #self.featureVectorDataByBuyerId = {}

        self.featureVectorDataClassified = {}
        self.featureVectorDataByBidderIdClassified = {}
        #self.featureVectorDataByBuyerIdClassified = {}

        self.bidder2BuyerDependencies = {}
        self.buyer2BidderDependencies = {}
        self.mutualDependencies = {}


        '''

        self.commonValueDistribution = []
        self.commonDistributionMaxValue = 0.0
        self.commonDistributionMinValue = 0.0

        self.commonValueDistributionClassified = {}

        # results
        # results

        self.resultsDict = {}
        self.resultsClassifiedDict = {}
        '''

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

        self._cpvFieldName = distributionConfig['cpvFieldName'] if 'cpvFieldName' in distributionConfig else self._cpvFieldName
        self._variableFieldName = distributionConfig['variableFieldName'] if 'variableFieldName' in distributionConfig else self._variableFieldName
        self._buyerIdFieldName = distributionConfig['buyerIdFieldName'] if 'buyerIdFieldName' in distributionConfig else self._buyerIdFieldName
        self._bidderIdFieldName = distributionConfig['bidderIdFieldName'] if 'bidderIdFieldName' in distributionConfig else self._bidderIdFieldName
        self._dataSourceType = distributionConfig['dataSourceType'] if 'dataSourceType' in distributionConfig else self._dataSourceType

        return None

    def calculateBidderBuyerRelations(self):
        '''
        This is main function for distributions analysis.

        :return: None
        '''

        # read feature vector file data
        # read feature vector file data

        self.readFVDataFile()

        # calculate dependencies
        # calculate dependencies

        self.calculateRelationDependencies()

        '''
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

        self.resultsDict = self.manipulateResults(self.resultsDict)

        for cpvCode, resultsDict in self.resultsClassifiedDict.items():
            self.resultsClassifiedDict[cpvCode] = self.manipulateResults(resultsDict)

        # save anomalies to file
        # save anomalies to file

        self.saveAnomalies2File(self.commonValueDistribution, self.resultsDict)

        for cpvCode, resultsDict in self.resultsClassifiedDict.items():
            distribution = self.commonValueDistributionClassified[cpvCode]
            self.saveAnomalies2File(distribution, resultsDict, cpvCode)
        '''

        return None

    def readFVDataFile(self):
        '''
        Function reads feature vector data file into self.featureVectorData variable

        :return:
        '''

        # read feature vecor data file
        # read feature vecor data file

        self.featureVectorData = self.conf.sharedCommon.readDataFile2Dict(self._dataSourceFilePath + self._dataSourceFileName, "\t")

        # organize data for later analysis
        # organize data for later analysis

        bidderId_index = self.featureVectorData['head'].index(self._bidderIdFieldName)
        cpv_index = self.featureVectorData['head'].index(self._cpvFieldName)

        for row in self.featureVectorData['data']:

            # get classificators
            # get classificators

            tmp_bidderId = str(row[bidderId_index])
            tmp_cpv = str(row[cpv_index])

            # classify by bidder
            # classify by bidder

            if tmp_bidderId not in self.featureVectorDataByBidderId:
                self.featureVectorDataByBidderId[tmp_bidderId] = []

            self.featureVectorDataByBidderId[tmp_bidderId].append(row)

            # classify by cpv
            # classify by cpv

            if tmp_cpv not in self.featureVectorDataClassified:
                self.featureVectorDataClassified[tmp_cpv] = []
                self.featureVectorDataByBidderIdClassified[tmp_cpv] = {}

            self.featureVectorDataClassified[tmp_cpv].append(row)

            # classify by cpv, bidder
            # classify by cpv, bidder

            if tmp_bidderId not in self.featureVectorDataByBidderIdClassified[tmp_cpv]:
                self.featureVectorDataByBidderIdClassified[tmp_cpv][tmp_bidderId] = []

            self.featureVectorDataByBidderIdClassified[tmp_cpv][tmp_bidderId].append(row)

        return None

    def calculateRelationDependencies(self):
        '''
        Function calculates dependencies in relations based on transaction share.

        :return: None
        '''

        bidder2BuyerDependencies = {}
        buyer2BidderDependencies = {}
        bidderTotal = {}
        buyerTotal = {}
        buyerId_index = self.featureVectorData['head'].index(self._buyerIdFieldName)
        value_index = self.featureVectorData['head'].index(self._variableFieldName)

        for bidderId,bidderRows in self.featureVectorDataByBidderId.items():
            for row in bidderRows:

                buyerId = str(row[buyerId_index])
                value = float(row[value_index])

                # bidder 2 buyer dependency
                # bidder 2 buyer dependency

                if bidderId not in bidder2BuyerDependencies:
                    bidder2BuyerDependencies[bidderId] = {}
                    bidderTotal[bidderId] = 0.0

                if buyerId not in bidder2BuyerDependencies[bidderId]:
                    bidder2BuyerDependencies[bidderId][buyerId] = 0.0

                bidder2BuyerDependencies[bidderId][buyerId] += value
                bidderTotal[bidderId] += value

                # buyer 2 bidder dependency
                # buyer 2 bidder dependency

                if buyerId not in buyer2BidderDependencies:
                    buyer2BidderDependencies[buyerId] = {}
                    buyerTotal[buyerId] = 0.0

                if bidderId not in buyer2BidderDependencies[buyerId]:
                    buyer2BidderDependencies[buyerId][bidderId] = 0.0

                buyer2BidderDependencies[buyerId][bidderId] += value
                buyerTotal[buyerId] += value

        # converting absolute shares to relative :: bidder2buyer
        # converting absolute shares to relative :: bidder2buyer

        self.bidder2BuyerDependencies = {}
        for bidderId,buyersDict in bidder2BuyerDependencies.items():
            # consider only relations with at least 5 interactions
            if len(buyersDict) >= 2:
                for buyerId,value in buyersDict.items():
                    tmp_key = bidderId + "-" + buyerId
                    # avoid zero division
                    if bidderTotal[bidderId] < 1.0:
                        continue
                    self.bidder2BuyerDependencies[tmp_key] = [value / bidderTotal[bidderId], len(buyersDict)]

        # sort dependencies
        # sort dependencies

        self.bidder2BuyerDependencies = {k: v for k, v in sorted(self.bidder2BuyerDependencies.items(), reverse=True, key=lambda item: item[1][0])}

        # converting absolute shares to relative :: buyer2bidder
        # converting absolute shares to relative :: buyer2bidder

        self.buyer2BidderDependencies = {}
        for buyerId,bidderDict in buyer2BidderDependencies.items():
            # consider only relations with at least 5 interactions
            if len(bidderDict) >= 2:
                for bidderId,value in bidderDict.items():
                    tmp_key = buyerId + "-" + bidderId
                    self.buyer2BidderDependencies[tmp_key] = [value / buyerTotal[buyerId], len(bidderDict)]

        # sort dependencies
        # sort dependencies

        self.buyer2BidderDependencies = {k: v for k, v in sorted(self.buyer2BidderDependencies.items(), reverse=True, key=lambda item: item[1][0])}

        # calculating mutual dependency
        # calculating mutual dependency

        self.mutualDependencies = {}
        for buyerId,bidderDict in buyer2BidderDependencies.items():
            for bidderId, bidderValue in bidderDict.items():
                if bidderId not in bidder2BuyerDependencies:
                    continue
                if buyerId not in bidder2BuyerDependencies[bidderId]:
                    continue
                # check total value sums
                if bidderId not in bidderTotal:
                    continue
                if bidderTotal[bidderId] < 0.01:
                    continue
                if buyerId not in buyerTotal:
                    continue
                if buyerTotal[buyerId] < 0.01:
                    continue

                buyerValue = bidder2BuyerDependencies[bidderId][buyerId]
                tmp_key = buyerId + "-" + bidderId
                self.mutualDependencies[tmp_key] = [buyerValue * bidderValue / (buyerTotal[buyerId] * bidderTotal[bidderId]), 0]

        self.mutualDependencies = {k: v for k, v in sorted(self.mutualDependencies.items(), reverse=True, key=lambda item: item[1][0])}

        return None

    def saveAnomalies2File(self):
        '''
        This function saves anomalies to file

        :return: None
        '''

        # BIDDER 2 BUYER convert data into correct format
        # BIDDER 2 BUYER convert data into correct format

        dataDict = {}
        dataDict['head'] = ['buyerId', 'bidderId', 'share', 'num_tenders']
        dataDict['data'] = []

        for key,row in self.bidder2BuyerDependencies.items():
            idsList = key.split('-')
            if len(idsList) != 2:
                continue
            if row[0] < 0.05:
                # ignore shares smaller than 5%
                continue
            tmp_row = [idsList[1], idsList[0], str(row[0]), str(row[1])]
            dataDict['data'].append(tmp_row)

        # enrich data
        # enrich data

        fieldsDict = {'bidderId': 'bidder_name', 'buyerId': 'buyer_name'}
        dataDict = self.sharedMethods.appendMJUOrganizationNames2Dict(dataDict, fieldsDict)

        # save data 2 file
        # save data 2 file

        fulFileName = self._dataStorageFilePath + self._dataStorageFileName + '-bidder2buyer.tsv'
        fulFileName = fulFileName.replace('-CPV', '')
        self.conf.sharedCommon.sendDict2Output(dataDict, fulFileName)

        # BUYER 2 BIDDER convert data into correct format
        # BUYER 2 BIDDER convert data into correct format

        dataDict = {}
        dataDict['head'] = ['buyerId', 'bidderId', 'share', 'num_tenders']
        dataDict['data'] = []

        for key,row in self.buyer2BidderDependencies.items():
            idsList = key.split('-')
            if len(idsList) != 2:
                continue
            if row[0] < 0.05:
                # ignore shares smaller than 5%
                continue
            tmp_row = [idsList[0], idsList[1], str(row[0]), str(row[1])]
            dataDict['data'].append(tmp_row)

        # enrich data
        # enrich data

        fieldsDict = {'bidderId': 'bidder_name', 'buyerId': 'buyer_name'}
        dataDict = self.sharedMethods.appendMJUOrganizationNames2Dict(dataDict, fieldsDict)

        # save data 2 file
        # save data 2 file

        fulFileName = self._dataStorageFilePath + self._dataStorageFileName + '-buyer2bidder.tsv'
        fulFileName = fulFileName.replace('-CPV', '')
        self.conf.sharedCommon.sendDict2Output(dataDict, fulFileName)

        # MUTUAL DEPENDENCY convert data into correct format
        # MUTUAL DEPENDENCY convert data into correct format

        dataDict = {}
        dataDict['head'] = ['buyerId', 'bidderId', 'share', 'num_tenders']
        dataDict['data'] = []

        for key,row in self.mutualDependencies.items():
            idsList = key.split('-')
            if len(idsList) != 2:
                continue
            if row[0] < 0.05:
                # ignore shares smaller than 5%
                continue
            tmp_row = [idsList[0], idsList[1], str(row[0]), str(row[1])]
            dataDict['data'].append(tmp_row)

        # enrich data
        # enrich data

        fieldsDict = {'bidderId': 'bidder_name', 'buyerId': 'buyer_name'}
        dataDict = self.sharedMethods.appendMJUOrganizationNames2Dict(dataDict, fieldsDict)

        # save data 2 file
        # save data 2 file

        fulFileName = self._dataStorageFilePath + self._dataStorageFileName + '-mutual.tsv'
        fulFileName = fulFileName.replace('-CPV', '')
        self.conf.sharedCommon.sendDict2Output(dataDict, fulFileName)

        return None

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
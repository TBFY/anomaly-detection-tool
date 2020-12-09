
class PartialCumulativeClass:
    '''
    the concept:

    '''

    def __init__(self, conf, shared):

        self.conf = conf
        self.shared = shared
        self.sharedAnalysis = None

        # define data source / destination
        # define data source / destination

        self.dataSourceFilePath = ''
        self.dataSourceFileName = ''

        self.saveAnomaliesFilePath = self.conf.transactionsDataResultsPath + 'time_periods/'
        self.saveAnomaliesFileName = 'part_cumulCAT.tsv'

        # test purposes :: -1 == full analysis
        # test purposes :: -1 == full analysis

        self.test_limit_rows = -1

        # storage vars
        # storage vars

        self.transactionsData = {}

        self.transactionsDataSums = {}
        self.transactionsDataSumsWeights = {}

        self.transactionsDataSumsClassified = {}
        self.transactionsDataSumsWeightsClassified = {}

        self.transactionsDataSumsPartial = {}
        self.transactionsDataSumsPartialClassified = {}

        self.transactionsDataSumsPartialTransposed = {}
        self.transactionsDataSumsPartialTransposedClassified = {}

        self.weightsComparedTransposed = {}
        self.weightsComparedTransposedClassified = {}

        self.transactionDataTimeFrameCluster = 3

        # analysis variables
        # analysis variables

        self._transactions_av_window_size = 5
        self._transactions_av_std_dev = 1.5

        # anomalies storage variables
        # anomalies storage variables

        self.exceptionsDict = {}
        self.exceptionsClassifiedDict = {}

    def findAnomaliesThroughPartialCumulation(self):

        # get transactions
        # get transactions

        fullDataPathSource = self.dataSourceFilePath + self.dataSourceFileName
        self.transactionsData = self.conf.sharedCommon.readAndOrganizeTransactions2Dict(fullDataPathSource, '\t', self.test_limit_rows)

        # working area:
        # - create partial sums by summing self._transactionDataWindowSum consecutive transactions
        # -

        self.createTransactionTimeFrameSums()

        '''
        # working area; for every transaction list between two entities:
        # - calculate derivative
        # - average derivative
        # - identify anomalies
        # - add identified anomalies on two lists: (i) cumuylative anomaly list (ii) full anomalies list :: retain company classificatyion

        for classificator, transactionDict in self.transactionsData['data'].items():
            for companyIds, transactionList in transactionDict.items():

                companyIdList = companyIds.split('-')
                companyIdPublic = companyIdList[0]
                companyIdAny = companyIdList[1]

                # initialize
                # initialize

                if classificator not in self.exceptionsClassifiedDict:
                    self.exceptionsClassifiedDict[classificator] = [0] * (len(transactionList) + 1)
                    self.exceptionsClassifiedCompaniesDict[classificator] = [{} for _ in range(len(transactionList))]
                    if len(self.exceptionsCumulatedList) == 0:
                        self.exceptionsCumulatedList = [0] * (len(transactionList) + 1)
                        self.exceptionsCumulatedCompaniesList = [{} for _ in range(len(transactionList))]

                # execute calculations
                # execute calculations

                tmp_derivatives = self.shared.getDerivatives(transactionList)
                tmp_derivatives_av = self.shared.getAveragedList(tmp_derivatives, self._transactions_av_window_size)
                tmp_exceptions = self.shared.getExceptionsLocal(tmp_derivatives, tmp_derivatives_av,
                                                                  self._transactions_av_std_dev)

                # add exceptions to cumulative and classified dictionary
                # add exceptions to cumulative and classified dictionary

                for index in tmp_exceptions:
                    self.exceptionsClassifiedDict[classificator][index] = self.exceptionsClassifiedDict[classificator][
                                                                              index] + 1
                    self.exceptionsCumulatedList[index] = self.exceptionsCumulatedList[index] + 1

                    # associate companies to exceptions classification
                    # associate companies to exceptions classification

                    if companyIdAny not in self.exceptionsClassifiedCompaniesDict[classificator][index]:
                        self.exceptionsClassifiedCompaniesDict[classificator][index][companyIdAny] = 1
                    else:
                        self.exceptionsClassifiedCompaniesDict[classificator][index][companyIdAny] = \
                        self.exceptionsClassifiedCompaniesDict[classificator][index][companyIdAny] + 1
                    if companyIdAny not in self.exceptionsCumulatedCompaniesList[index]:
                        self.exceptionsCumulatedCompaniesList[index][companyIdAny] = 1
                    else:
                        self.exceptionsCumulatedCompaniesList[index][companyIdAny] = \
                        self.exceptionsCumulatedCompaniesList[index][companyIdAny] + 1

                if (plotSingleDerivativesGraph):
                    # self.conf.plt.plot(data_av, color='red')
                    self.conf.plt.plot(tmp_derivatives_av, color='orange')
                    self.conf.plt.plot(tmp_derivatives, 'k.')
                    self.conf.plt.plot(transactionList, 'k.', color='green')
                    # add anomalies
                    anomalies_x = tmp_exceptions.keys()
                    anomalies_y = tmp_exceptions.values()
                    self.conf.plt.scatter(anomalies_x, anomalies_y)
                    
                    #for brk in breaks:
                    #    self.conf.plt.axvline(x=brk)

                    self.conf.plt.show()

        # find maximums and associate company ids to it
        # find maximums and associate company ids to it

        maxList, self.anomaliesList = self.shared.extractDataFromListMaximums(self.exceptionsCumulatedList,
                                                                                self.exceptionsCumulatedCompaniesList,
                                                                                self._transactions_av_window_size,
                                                                                self._breaks_maximum_window_dev)
        for classificator in self.exceptionsClassifiedDict:
            self.anomaliesClassifiedDict[classificator] = []
            maxList, self.anomaliesClassifiedDict[classificator] = self.shared.extractDataFromListMaximums(
                self.exceptionsClassifiedDict[classificator], self.exceptionsClassifiedCompaniesDict[classificator],
                self._transactions_av_window_size, self._breaks_maximum_window_dev)

        '''

        return None

    def createTransactionTimeFrameSums(self):
        '''
        Function takes transaction data transactionsData and creates a list of sums of self.transactionDataTimeFrameCluster consecutive transactions.
        Result is stored in self.transactionsDataPartialSums
        Function creates a list of full sums stored in self.transactionsDataSums.

        :return: 0
        '''

        # list through classifiers
        # list through classifiers

        for classifier in self.transactionsData['data']:

            # init transactions sum dictionary
            # init transactions sum dictionary

            if classifier not in self.transactionsDataSumsClassified:
                self.transactionsDataSumsClassified[classifier] = {}
                self.transactionsDataSumsPartialClassified[classifier] = {}
                self.transactionsDataSumsPartialTransposedClassified[classifier] = []
                self.weightsComparedTransposedClassified[classifier] = []

            # list relations
            # list relations

            for companyIds in self.transactionsData['data'][classifier]:

                #if(companyIds == '5065402000-5486815000'):
                #    print(len(self.transactionsData['data'][classifier][companyIds]), companyIds, self.transactionsData['data'][classifier][companyIds])

                tmp_sum = 0.0
                tmp_sum_part = 0.0
                tmp_frame_index = 0
                tmp_sum_part_index = 0

                if companyIds not in self.transactionsDataSumsPartial:
                    numOfslots = int(len(self.transactionsData['data'][classifier][companyIds]) / self.transactionDataTimeFrameCluster) + 1
                    self.transactionsDataSumsPartial[companyIds] = [0.0] * numOfslots
                    self.transactionsDataSumsPartialClassified[classifier][companyIds] = [0.0] * numOfslots
                    if len(self.transactionsDataSumsPartialTransposedClassified[classifier]) == 0:
                        self.transactionsDataSumsPartialTransposedClassified[classifier] = [{} for _ in range(numOfslots)]
                    if len(self.transactionsDataSumsPartialTransposed) == 0:
                        self.transactionsDataSumsPartialTransposed = [{} for _ in range(numOfslots)]
                    # data vars for storing compared weights
                    if len(self.weightsComparedTransposedClassified[classifier]) == 0:
                        self.weightsComparedTransposedClassified[classifier] = [{} for _ in range(numOfslots)]
                    if len(self.weightsComparedTransposed) == 0:
                        self.weightsComparedTransposed = [{} for _ in range(numOfslots)]

                # list individual transactions
                # list individual transactions

                for trans in self.transactionsData['data'][classifier][companyIds]:

                    tmp_sum = tmp_sum + float(trans)
                    tmp_sum_part = tmp_sum_part + float(trans)
                    tmp_frame_index = tmp_frame_index + 1

                    if tmp_frame_index >= self.transactionDataTimeFrameCluster:
                        # save in a "natural" form
                        self.transactionsDataSumsPartial[companyIds][tmp_sum_part_index] = tmp_sum_part
                        self.transactionsDataSumsPartialClassified[classifier][companyIds][tmp_sum_part_index] = tmp_sum_part
                        # save in a "transposed" form
                        self.transactionsDataSumsPartialTransposed[tmp_sum_part_index][companyIds] = tmp_sum_part
                        self.transactionsDataSumsPartialTransposedClassified[classifier][tmp_sum_part_index][companyIds] = tmp_sum_part

                        tmp_sum_part = 0.0
                        tmp_frame_index = 0
                        tmp_sum_part_index =  tmp_sum_part_index + 1

                # save trailing data
                # save trailing data

                if(tmp_frame_index > 0 and tmp_frame_index < self.transactionDataTimeFrameCluster):
                    # normal data
                    self.transactionsDataSumsPartial[companyIds][tmp_sum_part_index] = tmp_sum_part
                    self.transactionsDataSumsPartialClassified[classifier][companyIds][tmp_sum_part_index] = tmp_sum_part
                    # transposed data
                    self.transactionsDataSumsPartialTransposed[tmp_sum_part_index][companyIds] = tmp_sum_part
                    self.transactionsDataSumsPartialTransposedClassified[classifier][tmp_sum_part_index][companyIds] = tmp_sum_part

                self.transactionsDataSums[companyIds] = tmp_sum
                self.transactionsDataSumsClassified[classifier][companyIds] = tmp_sum

        # get base transaction weights
        # get base transaction weights

        self.transactionsDataSumsWeights = self.convertTransactions2Weights(self.transactionsDataSums)
        for classifier in self.transactionsDataSumsClassified:
            self.transactionsDataSumsWeightsClassified[classifier] = self.convertTransactions2Weights(self.transactionsDataSumsClassified[classifier])

        # compare partial transaction weights to base weights
        # compare partial transaction weights to base weights

        self.exceptionsDict = self.identifyAnomalies(self.transactionsDataSumsPartialTransposed, self.transactionsDataSumsWeights)
        # print(self.exceptionsDict)
        for classifier in self.transactionsDataSumsPartialTransposedClassified:
            self.exceptionsClassifiedDict[classifier] = self.identifyAnomalies(self.transactionsDataSumsPartialTransposedClassified[classifier], self.transactionsDataSumsWeightsClassified[classifier])
            #print(self.exceptionsClassifiedDict[classifier])

        return None

    def convertTransactions2Weights(self, dataDict):

        weightsList = {}
        data_sum = sum(dataDict.values())

        if data_sum == 0.0:
            return weightsList

        for ids,value in dataDict.items():
            weightsList[ids] = value / data_sum

        return weightsList

    def identifyAnomalies(self, partialTransactionSumsTransposed, transactionSumWeights):

        anomalyDict = {}

        for partialDataSet in partialTransactionSumsTransposed:

            tmp_partialWeights = self.convertTransactions2Weights(partialDataSet)

            # get comparative weights
            # get comparative weights

            tmp_comparedWeights = {}
            for ids in tmp_partialWeights:
                if transactionSumWeights[ids] > 0.0 and tmp_partialWeights[ids] > 0.0:
                    tmp_comparedWeights[ids] = self.conf.numpy.log10(tmp_partialWeights[ids] / transactionSumWeights[ids])
                    # tmp_comparedWeights[ids] = tmp_partialWeights[ids] / transactionSumWeights[ids]

            '''
            # plot histogram
            # plot histogram

            plotHistogram = False
            if plotHistogram:
                self.conf.plt.plot(list(tmp_comparedWeights.values()), 'k.')
                self.conf.plt.show()
                self.conf.plt.close()
                self.conf.plt.figure(figsize=(8, 6))
                self.conf.plt.style.use('seaborn-poster')
            '''

            # average comparative weights and look identify anomalies
            # average comparative weights and look identify anomalies

            # requiring minimum amount of data
            # requiring minimum amount of data

            if len(tmp_comparedWeights) < self._transactions_av_window_size:
                continue

            tmp_comparedWeights_av = self.shared.getAveragedList(list(tmp_comparedWeights.values()), self._transactions_av_window_size)
            anomaliesDetected = self.shared.getExceptionsLocal(list(tmp_comparedWeights.values()), tmp_comparedWeights_av, self._transactions_av_std_dev)

            idsList = list(tmp_comparedWeights.keys())
            for index, value in enumerate(anomaliesDetected):
                maticnaList = idsList[index].split('-')
                if index not in anomalyDict:
                    anomalyDict[maticnaList[1]] = float(value)
                else:
                    anomalyDict[maticnaList[1]] = anomalyDict[maticnaList[1]] + float(value)

            # add anomalies onto a main datasotre variable
            # add anomalies onto a main datasotre variable

            '''
            plotAnomalies = False
            if plotAnomalies:
                self.conf.plt.plot(tmp_comparedWeights_av, color='red')
                self.conf.plt.plot(list(tmp_comparedWeights.values()), 'k.')
                # self.conf.plt.hist(list(tmp_comparedWeights.values()), 1000)
                # add anomalies
                anomalies_x = anomaliesDetected.keys()
                anomalies_y = anomaliesDetected.values()
                self.conf.plt.scatter(anomalies_x, anomalies_y)
                # for brk in breaks:
                #    self.conf.plt.axvline(x=brk)
                self.conf.plt.show()
                self.conf.plt.close()
                self.conf.plt.figure(figsize=(8, 6))
                self.conf.plt.style.use('seaborn-poster')
            '''

        return sorted(anomalyDict.items(), key=lambda kv: kv[1], reverse=True)

    # print results
    # print results

    def saveAnomalies2File(self):
        '''
        function saves anomnalies into file

        :return: None
        '''

        # set dictionary in correct format
        # set dictionary in correct format

        finalDataDict = {}
        finalDataDict['head'] = ["maticna", "score"]
        finalDataDict['data'] = []
        for row in self.exceptionsDict:
            tmp_row = [str(row[0]), str(row[1])]
            finalDataDict['data'].append(tmp_row)

        # enrich data
        # enrich data

        fieldsDict = {'maticna': 'company_name'}
        finalDataDict = self.sharedAnalysis.appendAjpesOrganizationNames2Dict(finalDataDict, fieldsDict)

        fileName = self.saveAnomaliesFileName.replace('CAT', '')
        fullFileName = self.saveAnomaliesFilePath + fileName
        self.conf.sharedCommon.sendDict2Output(finalDataDict, fullFileName)

        # repeat for every company group, classified by their field of interest
        # repeat for every company group, classified by their field of interest

        for classificator in self.exceptionsClassifiedDict:
            # skip
            finalDataDict = {}
            finalDataDict['head'] = ["maticna", "score"]
            finalDataDict['data'] = []
            for row in self.exceptionsClassifiedDict[classificator]:
                tmp_row = [str(row[0]), str(row[1])]
                finalDataDict['data'].append(tmp_row)

            # enrich data
            # enrich data

            fieldsDict = {'maticna': 'company_name'}
            finalDataDict = self.sharedAnalysis.appendAjpesOrganizationNames2Dict(finalDataDict, fieldsDict)

            # save data
            # save data

            fileName = self.saveAnomaliesFileName.replace('CAT', classificator)
            fullFileName = self.saveAnomaliesFilePath + fileName
            self.conf.sharedCommon.sendDict2Output(finalDataDict, fullFileName)

        return None


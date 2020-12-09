
class DerivativesAnomalyClass:
    '''
    the concept:
    - calculate all derivatives
    - identify exceptions
    - accumulate exceptions
    - anomalies are defined as:
      (i) list companies ordered by deviation size
      (ii) list companies accumulated within exceptions peaks
    '''

    def __init__(self, conf, shared):

        self.conf = conf
        self.shared = shared
        self.sharedAnalysis = None

        # define data source / destination
        # define data source / destination

        self.dataSourceFilePath = ''
        self.dataSourceFileName = ''

        self.saveAnomaliesFilePath = self.conf.transactionsDataResultsPath + 'local_extremes/'
        self.saveAnomaliesFileName = 'derivativesCAT.tsv'

        # test purposes :: -1 == full analysis
        # test purposes :: -1 == full analysis

        self.test_limit_rows = -1

        # storage vars
        # storage vars

        self.transactionsData = {}

        # analysis variables
        # analysis variables

        self._transactions_av_window_size = 5
        self._transactions_av_std_dev = 2.0
        self._breaks_maximum_window_dev = 1

        # anomalies storage variables
        # anomalies storage variables

        self.exceptionsClassifiedDict = {}
        self.exceptionsClassifiedCompaniesDict = {}
        self.exceptionsCumulatedList = []
        self.exceptionsCumulatedCompaniesList = []

        # results variables
        # results variables

        self.anomaliesList = []
        self.anomaliesClassifiedDict = {}

    def findAnomaliesThroughDerivatives(self):
        '''
        typical transaction sum data histogram is of form of a very sharply declining exponential function

        :return:
        '''

        # get transactions
        # get transactions

        fullDataPathSource = self.dataSourceFilePath + self.dataSourceFileName
        self.transactionsData = self.conf.sharedCommon.readAndOrganizeTransactions2Dict(fullDataPathSource, '\t', self.test_limit_rows)

        # for every transaction list between two entities:
        # - calculate derivative
        # - average derivative
        # - identify anomalies
        # - add identified anomalies on two lists: (i) cumulative anomaly list (ii) full anomalies list :: retain company classificatyion

        for classificator,transactionDict in self.transactionsData['data'].items():
            # print(classificator, len(transactionDict))
            # print(transactionDict)
            for companyIds,transactionList in transactionDict.items():
                companyIdList = companyIds.split('-')
                companyIdPublic = companyIdList[0]
                companyIdAny = companyIdList[1]

                # initialize storage vars
                # initialize storage vars

                if classificator not in self.exceptionsClassifiedDict:
                    self.exceptionsClassifiedDict[classificator] = [0] * (len(transactionList) + 1)
                    self.exceptionsClassifiedCompaniesDict[classificator] = [{} for _ in range(len(transactionList))]
                    if len(self.exceptionsCumulatedList) == 0:
                        self.exceptionsCumulatedList = [0] * (len(transactionList) + 1)
                        self.exceptionsCumulatedCompaniesList = [{} for _ in range(len(transactionList))]

                # execute calculations
                # execute calculations

                tmp_derivatives =    self.shared.getDerivatives(transactionList)
                tmp_derivatives_av = self.shared.getAveragedList(tmp_derivatives, self._transactions_av_window_size)
                tmp_exceptions = self.shared.getExceptionsLocal(tmp_derivatives, tmp_derivatives_av, self._transactions_av_std_dev)

                # add exceptions to cumulative and classified dictionary
                # add exceptions to cumulative and classified dictionary

                for index in tmp_exceptions:
                    self.exceptionsClassifiedDict[classificator][index] = self.exceptionsClassifiedDict[classificator][index] + 1
                    self.exceptionsCumulatedList[index] = self.exceptionsCumulatedList[index] + 1

                    # associate companies to exceptions classification
                    # associate companies to exceptions classification

                    if companyIdAny not in self.exceptionsClassifiedCompaniesDict[classificator][index]:
                        self.exceptionsClassifiedCompaniesDict[classificator][index][companyIdAny] = 1
                    else:
                        self.exceptionsClassifiedCompaniesDict[classificator][index][companyIdAny] = self.exceptionsClassifiedCompaniesDict[classificator][index][companyIdAny] + 1

                    if companyIdAny not in self.exceptionsCumulatedCompaniesList[index]:
                        self.exceptionsCumulatedCompaniesList[index][companyIdAny] = 1
                    else:
                        self.exceptionsCumulatedCompaniesList[index][companyIdAny] = self.exceptionsCumulatedCompaniesList[index][companyIdAny] + 1

                '''
                # for debugging purposes
                if (plotSingleDerivativesGraph):
                    # self.conf.plt.plot(data_av, color='red')
                    self.conf.plt.plot(tmp_derivatives_av, color='orange')
                    self.conf.plt.plot(tmp_derivatives, 'k.')
                    self.conf.plt.plot(transactionList, 'k.', color='green')
                    # add anomalies
                    anomalies_x = tmp_exceptions.keys()
                    anomalies_y = tmp_exceptions.values()
                    self.conf.plt.scatter(anomalies_x, anomalies_y)
                    # for brk in breaks:
                    #     self.conf.plt.axvline(x=brk)
                    self.conf.plt.show()
                '''

        # find maximums and associate company ids to it
        # find maximums and associate company ids to it

        maxList, self.anomaliesList = self.shared.extractDataFromListMaximums(self.exceptionsCumulatedList, self.exceptionsCumulatedCompaniesList, self._transactions_av_window_size, self._breaks_maximum_window_dev)
        for classificator in self.exceptionsClassifiedDict:
            self.anomaliesClassifiedDict[classificator] = []
            maxList, self.anomaliesClassifiedDict[classificator] = self.shared.extractDataFromListMaximums(self.exceptionsClassifiedDict[classificator], self.exceptionsClassifiedCompaniesDict[classificator], self._transactions_av_window_size, self._breaks_maximum_window_dev)

        return None

    def saveAnomalies2File(self):
        '''
        function save anomalies into file

        :return: dictionary sorted from highest to lowest deviation from cluster average value
        '''

        max_anomalies_abs = 1000
        max_anomalies_rel = .1

        # save anomalies list
        # save anomalies list

        i_rel = int(max_anomalies_rel * len(self.anomaliesList))
        i_max = max_anomalies_abs if i_rel < max_anomalies_abs else i_rel

        anomaliesList = self.anomaliesList[:i_max]

        data2FileDict = {}
        data2FileDict['head'] = ['company_id', 'score']
        data2FileDict['data'] = []
        for row in anomaliesList:
            new_row = [str(row[0]), str(row[1])]
            data2FileDict['data'].append(new_row)

        # enrich data
        # enrich data

        fieldsDict = {'company_id': 'company_name'}
        data2FileDict = self.sharedAnalysis.appendAjpesOrganizationNames2Dict(data2FileDict, fieldsDict)

        # save to file
        # save to file

        fullFilePath = self.saveAnomaliesFilePath + self.saveAnomaliesFileName.replace('CAT', '-companies')
        self.conf.sharedCommon.sendDict2Output(data2FileDict, fullFilePath)

        # save cumulated exceptions
        # save cumulated exceptions

        data2FileAnomaliesDict = {}
        data2FileAnomaliesDict['head'] = ['date', 'value']
        data2FileAnomaliesDict['data'] = []

        for date,value in zip(self.transactionsData['head'][3:], self.exceptionsCumulatedList[:-1]):
            data2FileAnomaliesDict['data'].append([str(date),str(value)])

        fullFilePath = self.saveAnomaliesFilePath + self.saveAnomaliesFileName.replace('CAT', '-time')
        self.conf.sharedCommon.sendDict2Output(data2FileAnomaliesDict, fullFilePath)

        # repeat for every classification
        # repeat for every classification

        for classificator in self.exceptionsClassifiedDict:

            # save anomalies list
            # save anomalies list

            anomaliesList = self.anomaliesClassifiedDict[classificator][:i_max]

            data2FileDict = {}
            data2FileDict['head'] = ['company_id', 'score']
            data2FileDict['data'] = []
            for row in anomaliesList:
                new_row = [str(row[0]), str(row[1])]
                data2FileDict['data'].append(new_row)

            # enrich data
            # enrich data

            fieldsDict = {'company_id': 'company_name'}
            data2FileDict = self.sharedAnalysis.appendAjpesOrganizationNames2Dict(data2FileDict, fieldsDict)

            # save to file
            # save to file

            fullFilePath = self.saveAnomaliesFilePath + self.saveAnomaliesFileName.replace('CAT', '-companies-' + classificator)
            self.conf.sharedCommon.sendDict2Output(data2FileDict, fullFilePath)

            # save cumulated exceptions
            # save cumulated exceptions

            data2FileAnomaliesDict['data'] = []
            for date,value in zip(self.transactionsData['head'][3:], self.exceptionsClassifiedDict[classificator][:-1]):
                data2FileAnomaliesDict['data'].append([str(date),str(value)])

            fullFilePath = self.saveAnomaliesFilePath + self.saveAnomaliesFileName.replace('CAT', '-time-' + classificator)
            self.conf.sharedCommon.sendDict2Output(data2FileAnomaliesDict, fullFilePath)

        return None



class PeriodsAnomalyClass:
    '''
    the concept:
    1) phase 1
       - for every pair of entities convolve transaction list into a smooth curve
       - identify transaction trends: when a series of transactions start / end
       - merge all starting / ending points in one graph
       - save starting / ending points into graph and its relations
    2) phase 2
       - define core dates
       - identify peaks around core dates
       - identify all entities within core dates peaks
       - sort entities by likleiness of being part of the peak
    '''

    def __init__(self, conf, shared):

        self.conf = conf
        self.shared = shared
        self.sharedAnalysis = None

        # define data source / destination
        # define data source / destination

        self.dataSourceFilePath = ''
        self.dataSourceFileName = ''

        self.saveAnomaliesFilePath = self.conf.transactionsDataResultsPath + 'period_margin/'
        self.saveAnomaliesFileName = 'periodsCAT.tsv'

        # test purposes :: -1 == full analysis
        # test purposes :: -1 == full analysis

        self.test_limit_rows = -1

        # define transactions data storage variables
        # define transactions data storage variables

        self._transactions_av_window_size = 5
        self._transactions_av_std_dev = 2.5

        # storage raw data vars
        # storage raw data vars

        self.transactionsData = {}
        self.periodBreaksCompaniesList = []
        self.periodBreaksCompaniesListClassified = {}
        self.periodBreaksCompaniesAnomalyList = {}

        # results variables
        # results variables

        self.deviationList = {}
        self.deviationListClassified = {}
        self.breaksAccumulation = []
        self.breaksAccumulationClassified = {}

        # analysis parameters
        # analysis parameters

        # a threshold to surpass to count as non-zero value
        self._breaks_activation_treshold = 1.0
        # number of consecutive below/above threshold values, that triggers a break
        self._breaks_activation_window_size = 5
        self._breaks_av_window_size = 5
        self._breaks_av_std_dev = 2.5
        self._breaks_maximum_window_dev = 2

    def findAnomaliesThroughPeriodMargin(self):
        '''
        typical transaction sum data histogram is of form of a very sharply declining exponential function

        :return: None
        '''

        # read transactions file
        # read transactions file

        fullDataPathSource = self.dataSourceFilePath + self.dataSourceFileName
        self.transactionsData = self.conf.sharedCommon.readAndOrganizeTransactions2Dict(fullDataPathSource, '\t', self.test_limit_rows)

        # working area
        # working area

        tmp_k1 = list(self.transactionsData['data'].keys())[0]
        tmp_k2 = list(self.transactionsData['data'][tmp_k1].keys())[0]
        numberOfTransactionData = len(self.transactionsData['data'][tmp_k1][tmp_k2])
        self.breaksAccumulation = [0] * (numberOfTransactionData + 1)
        self.periodBreaksCompaniesList = [[] for _ in range(numberOfTransactionData + 1)]

        for classificator,transactionsDict in self.transactionsData['data'].items():
            self.breaksAccumulationClassified[classificator] = [0] * (numberOfTransactionData + 1)
            self.periodBreaksCompaniesListClassified[classificator] = [[] for _ in range(numberOfTransactionData + 1)]
            #print("class: ", classificator, " => ", len(transactionsDict))
            #print(transactionsDict)
            for company_ids, transactionList in transactionsDict.items():
                tmp_breaks = self.getProcessedData2BreaksList(classificator, company_ids, transactionList, plotData=False)
                #print(tmp_breaks)
                for b_index in tmp_breaks:
                    self.breaksAccumulation[b_index] = self.breaksAccumulation[b_index] + 1
                    self.breaksAccumulationClassified[classificator][b_index] = self.breaksAccumulationClassified[classificator][b_index] + 1

        # remove 0th element (moment when most of transactions start - irrelevant date)
        # remove 0th element (moment when most of transactions start - irrelevant date)

        self.breaksAccumulation = self.breaksAccumulation[1:]
        for classificator in self.breaksAccumulationClassified:
            #print(self.breaksAccumulationClassified[classificator])
            self.breaksAccumulationClassified[classificator] = self.breaksAccumulationClassified[classificator][1:]

        return None

    def getProcessedData2BreaksList(self, classificator, company_ids, data, plotData = False):
        '''
        Function plots:
        - returns a list of breaks, where a series of tyransactions start / end
        - plots data on graph if needed

        :param classificator: string, second entity classificator
        :param company_ids: string, two companies ids in form "id1-id2"
        :param data: list, list of data
        :param plotData: boolean, plot or not to plot
        :return: list of breaks
        '''

        # process data and extract anomalies
        # process data and extract anomalies

        data_av = self.shared.getAveragedList(data, self._transactions_av_window_size)
        exceptionsList = self.shared.getExceptionsLocal(data, data_av, self._transactions_av_std_dev)

        # save exceptions
        # save exceptions

        self.deviationList[company_ids] = exceptionsList
        self.deviationListClassified[classificator] = {}
        self.deviationListClassified[classificator][company_ids] = exceptionsList

        # remove exceptions and continue process with lists cleared of exceptions
        # remove exceptions and continue process with lists cleared of exceptions

        data_no_exceptions = data.copy()
        for index in exceptionsList.keys():
            data_no_exceptions[index] = 0.0

        data_no_exceptions_av = self.shared.getAveragedList(data_no_exceptions, self._transactions_av_window_size)

        # cluster data
        # cluster data

        breaks = self.shared.getBreaksFromData(data_no_exceptions_av, self._breaks_activation_treshold, self._breaks_activation_window_size)

        # classify company according when period break started / ended
        # classify company according when period break started / ended

        tmp_ids = company_ids.split("-")
        for index,brk in enumerate(breaks):
            if(brk == 0): continue
            self.periodBreaksCompaniesList[brk].append(tmp_ids[1])
            self.periodBreaksCompaniesListClassified[classificator][brk].append(tmp_ids[1])

        # showData on plot
        # showData on plot

        if(plotData):
            #self.conf.plt.plot(data_av, color='red')
            self.conf.plt.plot(data_no_exceptions_av, color='orange')
            #self.conf.plt.plot(data, 'k.')
            self.conf.plt.plot(data_no_exceptions, 'k.')
            # add anomalies
            anomalies_x = exceptionsList.keys()
            anomalies_y = exceptionsList.values()
            #self.conf.plt.scatter(anomalies_x, anomalies_y)
            for brk in breaks:
                self.conf.plt.axvline(x=brk)
            self.conf.plt.show()

        return breaks

    def getAnomalyFromBreaksCumulativeGraph(self, breaks_av, std_dev, companyBreaksList):
        '''
        Function gets list of data (accumulated transaction periods breaks) and returns a list of maximums and a list of companies involved in maximums

        :param breaks_av: list of accumulated transaction period breaks
        :return: list of maximums, dictionary of companies involved in maximums
        '''

        unavailableIndexList = []
        companyDict = {}
        maxList = self.shared.getMaximumList(breaks_av, self._breaks_maximum_window_dev)

        for mx in maxList:
            tmp_left = mx  - std_dev
            tmp_right = mx + std_dev
            if(tmp_left < 0): tmp_left = 0
            if (tmp_right >= len(breaks_av)): tmp_right = len(breaks_av) - 1

            i = tmp_left - 1
            while i <= tmp_right:
                # avoid double count
                # avoid double count
                i = i + 1
                if i in unavailableIndexList: continue
                else: unavailableIndexList.append(i)

                #for maticna in self.periodBreaksCompaniesList[i]:
                for maticna in companyBreaksList[i]:
                    if maticna in companyDict:
                        companyDict[maticna] = companyDict[maticna] + 1
                    else:
                        companyDict[maticna] = 1

        return maxList, sorted(companyDict.items(), key=lambda kv: kv[1], reverse=True)

    def saveAnomalies2File(self):
        '''
        function save anomalies into file

        :return: dictionary sorted from highest to lowest deviation from cluster average value
        '''

        max_anomalies_abs = 1000
        max_anomalies_rel = .1

        # save cumulated exceptions
        # save cumulated exceptions
        
        data2FileAnomaliesDict = {}
        data2FileAnomaliesDict['head'] = ['date', 'value']
        data2FileAnomaliesDict['data'] = []

        for date,value in zip(self.transactionsData['head'][3:], self.breaksAccumulation):
            data2FileAnomaliesDict['data'].append([str(date),str(value)])

        fullFilePath = self.saveAnomaliesFilePath + self.saveAnomaliesFileName.replace('CAT', '-time')
        self.conf.sharedCommon.sendDict2Output(data2FileAnomaliesDict, fullFilePath)

        # save anomalies list
        # save anomalies list

        # get and limit the number of anomalies
        # get and limit the number of anomalies

        breaks_av = self.shared.getAveragedList(self.breaksAccumulation, self._breaks_av_window_size)
        maxList, periodBreaksCompaniesAnomalyList = self.getAnomalyFromBreaksCumulativeGraph(breaks_av, self._breaks_maximum_window_dev, self.periodBreaksCompaniesList)

        i_rel = int(max_anomalies_rel * len(periodBreaksCompaniesAnomalyList))
        i_max = max_anomalies_abs if i_rel < max_anomalies_abs else i_rel

        anomaliesList = periodBreaksCompaniesAnomalyList[:i_max]

        # save anomalous companies
        # save anomalous companies

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

        # repeat for every category of companies
        # repeat for every category of companies

        for classificator in self.breaksAccumulationClassified:

            # save cumulated exceptions
            # save cumulated exceptions

            data2FileAnomaliesDict = {}
            data2FileAnomaliesDict['head'] = ['date', 'value']
            data2FileAnomaliesDict['data'] = []

            for date, value in zip(self.transactionsData['head'][3:], self.breaksAccumulationClassified[classificator]):
                data2FileAnomaliesDict['data'].append([str(date), str(value)])

            fullFilePath = self.saveAnomaliesFilePath + self.saveAnomaliesFileName.replace('CAT', '-time-' + classificator)
            self.conf.sharedCommon.sendDict2Output(data2FileAnomaliesDict, fullFilePath)

            # save anomalies list
            # save anomalies list

            # get and limit the number of anomalies
            # get and limit the number of anomalies

            breaks_av = self.shared.getAveragedList(self.breaksAccumulationClassified[classificator], self._breaks_av_window_size)
            maxList, periodBreaksCompaniesAnomalyList = self.getAnomalyFromBreaksCumulativeGraph(breaks_av, self._breaks_maximum_window_dev, self.periodBreaksCompaniesList)

            i_rel = int(max_anomalies_rel * len(periodBreaksCompaniesAnomalyList))
            i_max = max_anomalies_abs if i_rel < max_anomalies_abs else i_rel

            anomaliesList = periodBreaksCompaniesAnomalyList[:i_max]

            # save anomalous companies
            # save anomalous companies

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

        return None

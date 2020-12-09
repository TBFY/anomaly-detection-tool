
'''
Class reads all MJU anomalies files and create a common anomely measure. The idea is to aling all anomalies and detect companies that are most anomalous.

Anomalies derived from anomaly analysis are first mapped into a normalised space [0, 1], where:
- anomalies near 0 represent normal behaviour, while
anomalies near 1 represent highly anomalous behaviour.

In order to map from normalised space into a common anomalous space, we need a function. Function, selected for such mapping is:

[ 2 / (2 - x^2) ] - 1

The idea of this function is to reduce common anomaly values for companies near 0 in a normalised anomaly space, while pushing up companies near 1.

The reasoning behind this specific function:
- it satisfies boundary conditions f(0) = 0 and f(1) = 1
- it's simple
- it has a stronger differentiation between 0 and 1 compared to x^1 (in fact, we could also use x^3 - not that important)
'''

class CommonAnomalyMeasure:

    def __init__(self, conf, shared):

        self.conf = conf
        self.sharedMethods = shared

        # config params
        # config params

        self.anomalies2IncludeList = []

        # storage variables
        # storage variables

        self.cmnAnomalyPerCompanyDict = {}
        self.companyId2Name = {}

    def configureAnalysis(self, configDict):
        '''
        Function sets config parameters for analysis.

        :param ratiosConfig: dict containing config params for the script
        :return: None
        '''

        # import params
        # import params

        self.anomalies2IncludeList = configDict['anomalies2include']

        return None

    #### START - reading in functions ####
    #### START - reading in functions ####
    #### START - reading in functions ####

    def readAnomlyValues(self):
        '''
        Function reads into a single variable self.cmnAnomalyPerCompanyDict all available anomalies

        :return: None
        '''

        # read in anomalies
        # read in anomalies

        for anomalyLabel in self.anomalies2IncludeList:
            if anomalyLabel == 'distributions.budget':
                self.readInDistributionsBudgetAnomalies()
            elif anomalyLabel == 'distributions.offers':
                self.readInDistributionsOffersAnomalies()
            elif anomalyLabel == 'ratios.budget':
                self.readInRatiosBudgetAnomalies()
            elif anomalyLabel == 'ratios.revenue':
                self.readInRatiosRevenueAnomalies()
            elif anomalyLabel == 'relations':
                self.readInRelationsAnomalies()

        return None

    def readInDistributionsBudgetAnomalies(self):
        '''
        Functions reads in distribution budget anomalies.

        :return: None
        '''

        # set dir path to anomalies files
        # set dir path to anomalies files

        path2AnomaliesDir = self.conf.tenderDataResultsPath + 'distributions/budgetAssessment/'

        # find all (.tsv) anomaly files
        # find all (.tsv) anomaly files

        allFiles = [f for f in self.conf.os.listdir(path2AnomaliesDir) if self.conf.os.path.isfile(self.conf.os.path.join(path2AnomaliesDir, f))]
        fileSubstring = '--data-values.tsv'
        anomalyFilesList = [curFile for curFile in allFiles if curFile[-len(fileSubstring):] == fileSubstring]

        # read file by file
        # read file by file

        for fileName in anomalyFilesList:

            # read file data
            # read file data

            fullFileName = path2AnomaliesDir + fileName
            tmp_dataDict = self.conf.sharedCommon.readDataFile2Dict(fullFileName, "\t")
            if len(tmp_dataDict['data']) == 0:
                continue

            # define max delta value: needed for later normalisation
            # define max delta value: needed for later normalisation

            value_index = tmp_dataDict['head'].index('deltavalue')
            maxDeltaValue = max([float(sublist[value_index]) for sublist in tmp_dataDict['data']])

            # save data organized per company
            # save data organized per company

            raw_anomaly_index = tmp_dataDict['head'].index('deltavalue')
            bidder_id_index = tmp_dataDict['head'].index('bidder_id')
            bidder_name_index = tmp_dataDict['head'].index('bidder_name')
            for row in tmp_dataDict['data']:
                raw_anomaly_value = float(row[raw_anomaly_index])
                bidder_id = row[bidder_id_index]
                bidder_name = row[bidder_name_index]

                # store company name for later use
                # store company name for later use

                if bidder_id not in self.companyId2Name:
                    self.companyId2Name[bidder_id] = bidder_name

                # init common anmaly value
                # init common anmaly value

                if bidder_id not in self.cmnAnomalyPerCompanyDict:
                    self.cmnAnomalyPerCompanyDict[bidder_id] = 0.0

                # add common anomaly value to company's score
                # add common anomaly value to company's score

                normAnomalyValue = raw_anomaly_value / maxDeltaValue
                self.cmnAnomalyPerCompanyDict[bidder_id] += self.mapNormValue2CommonAnomalyValue(normAnomalyValue)

        return None

    def readInDistributionsOffersAnomalies(self):
        '''
        Functions reads in distribution num of offers anomalies.

        :return: None
        '''

        # set dir path to anomalies files
        # set dir path to anomalies files

        path2AnomaliesDir = self.conf.tenderDataResultsPath + 'distributions/offersNum/'

        # find all (.tsv) anomaly files
        # find all (.tsv) anomaly files

        allFiles = [f for f in self.conf.os.listdir(path2AnomaliesDir) if self.conf.os.path.isfile(self.conf.os.path.join(path2AnomaliesDir, f))]
        fileSubstring = '--data-values.tsv'
        anomalyFilesList = [curFile for curFile in allFiles if curFile[-len(fileSubstring):] == fileSubstring]

        # read file by file
        # read file by file

        for fileName in anomalyFilesList:

            # read file data
            # read file data

            fullFileName = path2AnomaliesDir + fileName
            tmp_dataDict = self.conf.sharedCommon.readDataFile2Dict(fullFileName, "\t")
            if len(tmp_dataDict['data']) == 0:
                continue

            # define min delta value: needed for later normalisation
            # define min delta value: needed for later normalisation

            value_index = tmp_dataDict['head'].index('deltavalue')
            minDeltaValue = min([float(sublist[value_index]) for sublist in tmp_dataDict['data']])

            # save data organized per company
            # save data organized per company

            raw_anomaly_index = tmp_dataDict['head'].index('deltavalue')
            bidder_id_index = tmp_dataDict['head'].index('bidder_id')
            bidder_name_index = tmp_dataDict['head'].index('bidder_name')
            for row in tmp_dataDict['data']:
                raw_anomaly_value = float(row[raw_anomaly_index])
                bidder_id = row[bidder_id_index]
                bidder_name = row[bidder_name_index]

                # store company name for later use
                # store company name for later use

                if bidder_id not in self.companyId2Name:
                    self.companyId2Name[bidder_id] = bidder_name

                # init common anomaly value
                # init common anomaly value

                if bidder_id not in self.cmnAnomalyPerCompanyDict:
                    self.cmnAnomalyPerCompanyDict[bidder_id] = 0.0

                # add common anomaly value to company's score
                # add common anomaly value to company's score

                normAnomalyValue = raw_anomaly_value / minDeltaValue
                self.cmnAnomalyPerCompanyDict[bidder_id] += self.mapNormValue2CommonAnomalyValue(normAnomalyValue)

        return None

    def readInRatiosRevenueAnomalies(self):
        '''
        Functions reads in ratio budget anomalies.

        :return: None
        '''

        # set dir path to anomalies files
        # set dir path to anomalies files

        path2AnomaliesDir = self.conf.tenderDataResultsPath + 'ratios/revenuePerEmployee/'

        # find all (.tsv) anomaly files
        # find all (.tsv) anomaly files

        allFiles = [f for f in self.conf.os.listdir(path2AnomaliesDir) if self.conf.os.path.isfile(self.conf.os.path.join(path2AnomaliesDir, f))]
        fileSubstring = 'si-ministry-pos'
        anomalyFilesList = [curFile for curFile in allFiles if curFile[:len(fileSubstring)] == fileSubstring]

        # read trend curve, reflecting non anomalous behaviour
        # read trend curve, reflecting non anomalous behaviour

        fullTrendFileName = path2AnomaliesDir + 'si-ministry-linear-fit.tsv'
        trendCurvedict = self.conf.sharedCommon.readDataFile2Dict(fullTrendFileName, "\t")
        trend_k = float(trendCurvedict['data'][0][0])
        trend_n = float(trendCurvedict['data'][0][1])

        # read file by file
        # read file by file

        for fileName in anomalyFilesList:

            # read file data
            # read file data

            fullFileName = path2AnomaliesDir + fileName
            tmp_dataDict = self.conf.sharedCommon.readDataFile2Dict(fullFileName, "\t")
            if len(tmp_dataDict['data']) == 0:
                continue

            # define max anomaly value: needed for later normalisation
            # define max anomaly value: needed for later normalisation

            value_index = tmp_dataDict['head'].index('y_value')
            maxYValue_raw = max([float(sublist[value_index]) for sublist in tmp_dataDict['data']])

            # substract trend value (max value is associated with 1st place ==>> x_val = 1)
            # substract trend value (max value is associated with 1st place ==>> x_val = 1)

            maxYValue = maxYValue_raw - (trend_k * 1.0 + trend_n)

            # save data organized per company
            # save data organized per company

            raw_x_value_index = tmp_dataDict['head'].index('x_val')
            raw_anomaly_index = tmp_dataDict['head'].index('y_value')
            bidder_id_index = tmp_dataDict['head'].index('bidderId')
            bidder_name_index = tmp_dataDict['head'].index('bidderName')
            for row in tmp_dataDict['data']:

                raw_anomaly_value = float(row[raw_anomaly_index])
                raw_x_value = float(row[raw_x_value_index])
                bidder_id = row[bidder_id_index]
                bidder_name = row[bidder_name_index]

                # there is a proble mwith "raw anomaly value" as it's simply calculated as:
                # x = log(tenderValue / companyNumEmployees)
                # in order to really calcualte anomalies, one needs to substract "normal" value (or normal trend), which is in our case a linear curve

                raw_anomaly_value_norm = raw_anomaly_value - (trend_k * raw_x_value + trend_n)

                # store company name for later use
                # store company name for later use

                if bidder_id not in self.companyId2Name:
                    self.companyId2Name[bidder_id] = bidder_name

                # init common anomaly value
                # init common anomaly value

                if bidder_id not in self.cmnAnomalyPerCompanyDict:
                    self.cmnAnomalyPerCompanyDict[bidder_id] = 0.0

                # add common anomaly value to company's score
                # add common anomaly value to company's score

                normAnomalyValue = raw_anomaly_value_norm / maxYValue
                self.cmnAnomalyPerCompanyDict[bidder_id] += self.mapNormValue2CommonAnomalyValue(normAnomalyValue)

        return None

    def readInRatiosBudgetAnomalies(self):
        '''
        Functions reads in ratio revenue per employee anomalies.

        :return: None
        '''

        # set dir path to anomalies files
        # set dir path to anomalies files

        path2AnomaliesDir = self.conf.tenderDataResultsPath + 'ratios/budgetAssessment/'

        # find all (.tsv) anomaly files
        # find all (.tsv) anomaly files

        allFiles = [f for f in self.conf.os.listdir(path2AnomaliesDir) if self.conf.os.path.isfile(self.conf.os.path.join(path2AnomaliesDir, f))]
        fileSubstring = 'neg-deviations.tsv'
        anomalyFilesList = [curFile for curFile in allFiles if curFile[-len(fileSubstring):] == fileSubstring]

        # read trend curve, reflecting non anomalous behaviour
        # read trend curve, reflecting non anomalous behaviour

        fullTrendFileName = path2AnomaliesDir + 'si-ministry-linear-fit.tsv'
        trendCurvedict = self.conf.sharedCommon.readDataFile2Dict(fullTrendFileName, "\t")
        trend_k = float(trendCurvedict['data'][0][0])
        trend_n = float(trendCurvedict['data'][0][1])

        # read file by file
        # read file by file

        for fileName in anomalyFilesList:

            # read file data
            # read file data

            fullFileName = path2AnomaliesDir + fileName
            tmp_dataDict = self.conf.sharedCommon.readDataFile2Dict(fullFileName, "\t")
            if len(tmp_dataDict['data']) == 0:
                continue

            # define max anomaly value: needed for later normalisation
            # define max anomaly value: needed for later normalisation

            value_index = tmp_dataDict['head'].index('y_value')
            maxYValue_raw = max([float(sublist[value_index]) for sublist in tmp_dataDict['data']])
            minYValue_raw = min([float(sublist[value_index]) for sublist in tmp_dataDict['data']])

            # substract trend value (max value is associated with 1st place ==>> x_val = 1)
            # substract trend value (max value is associated with 1st place ==>> x_val = 1)

            minYValue = minYValue_raw + (trend_k * 1.0 + trend_n)
            maxYValue = maxYValue_raw - (trend_k * 1.0 + trend_n)

            # save data organized per company
            # save data organized per company

            raw_x_value = 0
            raw_anomaly_index = tmp_dataDict['head'].index('y_value')
            bidder_id_index = tmp_dataDict['head'].index('bidderId')
            bidder_name_index = tmp_dataDict['head'].index('bidderName')
            for row in tmp_dataDict['data']:
                raw_anomaly_value = float(row[raw_anomaly_index])
                raw_x_value += 1
                bidder_id = row[bidder_id_index]
                bidder_name = row[bidder_name_index]

                # there is a proble mwith "raw anomaly value" as it's simply calculated as:
                # x = log(tenderEstimatedValue / tenderFinalValue)
                # in order to really calcualte anomalies, one needs to substract "normal" value (or normal trend), which is in our case a linear curve

                correctionFactor = trend_k * raw_x_value + trend_n
                if raw_anomaly_value > 0:
                    raw_anomaly_value_norm = (raw_anomaly_value - correctionFactor) / maxYValue
                else:
                    raw_anomaly_value_norm = (raw_anomaly_value + correctionFactor) / minYValue

                # store company name for later use
                # store company name for later use

                if bidder_id not in self.companyId2Name:
                    self.companyId2Name[bidder_id] = bidder_name

                # init common anomaly value
                # init common anomaly value

                if bidder_id not in self.cmnAnomalyPerCompanyDict:
                    self.cmnAnomalyPerCompanyDict[bidder_id] = 0.0

                # add common anomaly value to company's score
                # add common anomaly value to company's score

                normAnomalyValue = abs(raw_anomaly_value_norm)
                self.cmnAnomalyPerCompanyDict[bidder_id] += self.mapNormValue2CommonAnomalyValue(normAnomalyValue)

        return None

    def readInRelationsAnomalies(self):
        '''
        Functions reads in relational anomalies.

        :return: None
        '''

        # set dir path to anomalies files
        # set dir path to anomalies files

        path2AnomaliesDir = self.conf.tenderDataResultsPath + 'relations_bb/'

        # find all (.tsv) anomaly files
        # find all (.tsv) anomaly files

        allFiles = [f for f in self.conf.os.listdir(path2AnomaliesDir) if self.conf.os.path.isfile(self.conf.os.path.join(path2AnomaliesDir, f))]
        fileSubstring = 'buyer2bidder.tsv'
        anomalyFilesList = [curFile for curFile in allFiles if curFile[-len(fileSubstring):] == fileSubstring]

        # read file by file
        # read file by file

        for fileName in anomalyFilesList:

            # read file data
            # read file data

            fullFileName = path2AnomaliesDir + fileName
            tmp_dataDict = self.conf.sharedCommon.readDataFile2Dict(fullFileName, "\t")
            if len(tmp_dataDict['data']) == 0:
                continue

            # save data organized per company
            # save data organized per company

            raw_anomaly_index = tmp_dataDict['head'].index('share')
            bidder_id_index = tmp_dataDict['head'].index('bidderId')
            bidder_name_index = tmp_dataDict['head'].index('bidder_name')
            for row in tmp_dataDict['data']:
                raw_anomaly_value = float(row[raw_anomaly_index])
                bidder_id = row[bidder_id_index]
                bidder_name = row[bidder_name_index]

                # store company name for later use
                # store company name for later use

                if bidder_id not in self.companyId2Name:
                    self.companyId2Name[bidder_id] = bidder_name

                # init common anomaly value
                # init common anomaly value

                if bidder_id not in self.cmnAnomalyPerCompanyDict:
                    self.cmnAnomalyPerCompanyDict[bidder_id] = 0.0

                # add common anomaly value to company's score
                # add common anomaly value to company's score

                normAnomalyValue = raw_anomaly_value
                self.cmnAnomalyPerCompanyDict[bidder_id] += self.mapNormValue2CommonAnomalyValue(normAnomalyValue)

        return None

    #### END - reading in functions ####
    #### END - reading in functions ####
    #### END - reading in functions ####

    def mapNormValue2CommonAnomalyValue(self, normAnomalyValue):
        '''
        Functions calculates a common anomaly measure for relations anomalies.

        :return: float
        '''

        # no anomaly for negative values
        # no anomaly for negative values

        if normAnomalyValue < 0.0:
            return 0.0

        return (2 / (2 - normAnomalyValue * normAnomalyValue)) - 1

    def save2File(self):
        '''
        Function saves anomaly list into tsv file

        :return: None
        '''

        # first sort by common anomaly valiue
        # first sort by common anomaly valiue

        self.cmnAnomalyPerCompanyDict = {k: v for k, v in sorted(self.cmnAnomalyPerCompanyDict.items(), reverse=True, key=lambda item: item[1])}

        # then create dictionary to be saved to file
        # then create dictionary to be saved to file

        finalCommonAnomalyDict = {}
        finalCommonAnomalyDict['head'] = ['common_anomaly_value', 'company_id', 'company_name']
        finalCommonAnomalyDict['data'] = []

        for companyId,commonAnomalyValue in self.cmnAnomalyPerCompanyDict.items():

            # skip zero values
            # skip zero values

            if commonAnomalyValue < 0.0001:
                continue

            companyName = self.companyId2Name[companyId] if companyId in self.companyId2Name else '-'
            tmp_row = [str(commonAnomalyValue), companyId, companyName]
            finalCommonAnomalyDict['data'].append(tmp_row)

        # save to file
        # save to file

        fullFilePath = self.conf.tenderDataResultsPath + 'common-anomaly-measure.tsv'
        self.conf.sharedCommon.sendDict2Output(finalCommonAnomalyDict, fullFilePath)

        return None
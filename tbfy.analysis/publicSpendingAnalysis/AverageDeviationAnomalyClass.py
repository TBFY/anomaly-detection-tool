
class AverageDeviationAnomalyClass:

    def __init__(self, conf, confa):

        self.confObj = conf
        self.confaObj = confa

        # init global vars
        # init global vars

        self.sql = conf.sql
        self.cur = conf.db.cursor()
        self.gl  = conf.Global

        # define transactions data storage variables
        # define transactions data storage variables

        self.transactionsData = {}
        self.transactionsDataSums = {}
        self.transactionsDataSumsClassified = {}

        # results variables
        # results variables

        self.deviationList = {}
        self.deviationListClassified = {}

        self.storageDataFilePath = '../data/data2Web/'
        self.relativeNumOfDeviations = 0.1
        self.absoluteNumOfDeviations = 100

        # data source specific variables
        # data source specific variables

        self.companyList = {}

    # typical transaction sum data histogram is of form of a very sharply declining exponential function
    # after 30% of slots, the exponential function tail is gone and the remaining transactions are defined as anomaly

    def createAverageDeviationList(self, adConfig):

        # get params
        # get params

        file2AnalysePath = adConfig['files2AnalysePath'] if 'files2AnalysePath' in adConfig else ''
        files2AnalyseName = adConfig['files2AnalyseName'] if 'files2AnalyseName' in adConfig else ''
        tmp_filePath = file2AnalysePath + files2AnalyseName

        # get sorted average deviations
        # get sorted average deviations

        self.readTransactionsFileData(tmp_filePath)
        self.deviationList = self.getSortedDeviationList(self.transactionsDataSums)
        for classifier in self.transactionsDataSumsClassified:
            self.deviationListClassified[classifier] = self.getSortedDeviationList(self.transactionsDataSumsClassified[classifier])

        return 0

    # print histogram tail results
    # print histogram tail results

    def printAverageDeviationList(self):

        self.getCompanyList()
        self.printDataList(self.deviationList, 'deviationList.tsv')

        for classifier in self.deviationListClassified:
            fileName = 'deviationList-' + classifier + '.tsv'
            self.printDataList(self.deviationListClassified[classifier], fileName)

        return 0

    def printDataList(self, dataDict, fileName):

        numOfItems2Print = int(len(dataDict) * self.relativeNumOfDeviations)
        if(self.absoluteNumOfDeviations < numOfItems2Print):
            numOfItems2Print = self.absoluteNumOfDeviations

        fileObject = open(self.storageDataFilePath + fileName, 'w+')

        # print legend (1st row)
        # print legend (1st row)

        rowString = "maticna\tnaziv\tstd-deviacija"
        self._send2Output(rowString, fileObject)

        # print data
        # print data

        i = 0
        for maticna in dataDict:

            # limit items to numOfItems2Print
            # limit items to numOfItems2Print

            i = i + 1
            if(numOfItems2Print < i):
                break

            # assemble date data
            # assemble date data

            rowString = maticna + "\t"
            if maticna in self.companyList.keys():
                rowString = rowString + self.companyList[maticna]['popolno_ime'] + "\t"
            else:
                rowString = rowString + 'undefined' + "\t"

            rowString = rowString + str(dataDict[maticna])

            # print data
            # print data

            self._send2Output(rowString, fileObject)

        return 0

    def _send2Output(self, rowString, fileObject = None):

        if(fileObject != None):
            fileObject.write(rowString + "\n")
        else:
            print(rowString)

        return 0

    # returns transactions data file :: company's interest category :: maticna_public :: maticna_private :: [transactions]
    # returns transactions data file :: company's interest category :: maticna_public :: maticna_private :: [transactions]

    def readTransactionsFileData(self, filePath):

        # if data already stored in variables - return
        # if data already stored in variables - return

        if(len(self.transactionsData) > 0 and len(self.transactionsDataSums) > 0):
            return 0

        # save data in variables
        # save data in variables

        file = open(filePath)
        line_num = 0
        for line in file:

            # skip first line
            # skip first line

            line_num = line_num + 1
            if(line_num == 1): continue

            # create from a line "maticna-publis TAB maticna-private TAB classifier TAB sum TAB sum TAB .... sum TAB sum" a list
            # create from a line "maticna-publis TAB maticna-private TAB classifier TAB sum TAB sum TAB .... sum TAB sum" a list

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
            while(i < num_of_sums):
                self.transactionsData[company_classifier][maticna_public][maticna_private][i] = float(tmp_list[i + 3])
                tmp_sum = tmp_sum + float(tmp_list[i + 3])
                i = i + 1

            self.transactionsDataSums[maticna_private] = self.transactionsDataSums[maticna_private] + tmp_sum
            self.transactionsDataSumsClassified[company_classifier][maticna_private] = self.transactionsDataSumsClassified[company_classifier][maticna_private] + tmp_sum

        return 0

    def getSortedDeviationList(self, data2Analyse):

        dataList = data2Analyse.values()
        average = sum(dataList) / len(dataList)

        deviationList = {}
        for maticna in data2Analyse:
            deviationList[maticna] = abs(average - data2Analyse[maticna]) / average

        return {k: v for k, v in sorted(deviationList.items(), key=lambda x: x[1], reverse=True)}

    '''
    # takes transactions data and transforms them into a hostogram list
    # takes transactions data and transforms them into a hostogram list
    
    self.convertTransactionData2HistogramList(self._histogramNumOfSlots)

    def convertTransactionData2HistogramList(self, numOfBins):

        # don't change anything if data already available
        # don't change anything if data already available

        if(self._histogramSize == numOfBins): return 0
        else: self._histogramSize = numOfBins

        # organize transactions data into histogram list:
        # find max & min value in self.transactionsData value set
        # divide (max - min) value into numOfBins
        # assign transaction to every bin

        # find min and max value
        # find min and max value


        minVal = 10000000000.0
        maxVal = 0.0

        for tmp_class in self.transactionsDataSums:
            for tmp_mpublic in self.transactionsDataSums[tmp_class]:
                for tmp_mprivate in self.transactionsDataSums[tmp_class][tmp_mpublic]:
                    minVal = self.transactionsDataSums[tmp_class][tmp_mpublic][tmp_mprivate] if self.transactionsDataSums[tmp_class][tmp_mpublic][tmp_mprivate] < minVal else minVal
                    maxVal = self.transactionsDataSums[tmp_class][tmp_mpublic][tmp_mprivate] if maxVal < self.transactionsDataSums[tmp_class][tmp_mpublic][tmp_mprivate] else maxVal

        # assign elements to histogram list
        # assign elements to histogram list

        self.histogramCumulativeAll = [int(0)] * numOfBins
        valueRange = maxVal - minVal
        numOfBinsFloat = float(numOfBins)
        exceptCount = 0

        for tmp_class in self.transactionsDataSums:
            for tmp_mpublic in self.transactionsDataSums[tmp_class]:
                for tmp_mprivate in self.transactionsDataSums[tmp_class][tmp_mpublic]:
                    curr_bin = int(numOfBinsFloat * (self.transactionsDataSums[tmp_class][tmp_mpublic][tmp_mprivate] - minVal) / valueRange)
                    if(curr_bin == numOfBins):
                        curr_bin = curr_bin - 1
                        exceptCount = exceptCount + 1

                    self.histogramCumulativeAll[curr_bin] = self.histogramCumulativeAll[curr_bin] + 1

        #print(exceptCount)
        #print(self.histogramCumulativeAll)

        # repeat process for every companies subgrup
        # repeat process for every companies subgrup

        for tmp_class in self.transactionsDataSums:

            # find min and max value
            # find min and max value

            minVal = 10000000000.0
            maxVal = 0.0

            for tmp_mpublic in self.transactionsDataSums[tmp_class]:
                for tmp_mprivate in self.transactionsDataSums[tmp_class][tmp_mpublic]:
                    minVal = self.transactionsDataSums[tmp_class][tmp_mpublic][tmp_mprivate] if self.transactionsDataSums[tmp_class][tmp_mpublic][tmp_mprivate] < minVal else minVal
                    maxVal = self.transactionsDataSums[tmp_class][tmp_mpublic][tmp_mprivate] if maxVal < self.transactionsDataSums[tmp_class][tmp_mpublic][tmp_mprivate] else maxVal

            # if difference less than hal a cent, values are the same => only one match per class
            # if difference less than hal a cent, values are the same => only one match per class

            if(abs(minVal - maxVal) < 0.005): minVal = 0.0

            # assign elements to histogram list according its classifier
            # assign elements to histogram list according its classifier

            self.histogramCumulativeClassified[tmp_class] = [int(0)] * numOfBins
            self.histogramRelationListsClassified[tmp_class] = self.confaObj.numpy.empty((numOfBins, 0)).tolist()
            valueRange = maxVal - minVal
            numOfBinsFloat = float(numOfBins)
            exceptCount = 0

            for tmp_mpublic in self.transactionsDataSums[tmp_class]:
                for tmp_mprivate in self.transactionsDataSums[tmp_class][tmp_mpublic]:
                    curr_bin = int(numOfBinsFloat * (self.transactionsDataSums[tmp_class][tmp_mpublic][tmp_mprivate] - minVal) / valueRange)
                    if(curr_bin == numOfBins):
                        curr_bin = curr_bin - 1
                        exceptCount = exceptCount + 1
    
                    self.histogramCumulativeClassified[tmp_class][curr_bin] = self.histogramCumulativeClassified[tmp_class][curr_bin] + 1
                    relationString = tmp_mpublic + '-' + tmp_mprivate
                    self.histogramRelationListsClassified[tmp_class][curr_bin].append(relationString)

            #print(exceptCount)
            #print(self.histogramCumulativeClassified[tmp_class])
            #print(self.histogramRelationListsClassified[tmp_class])

        return 0
    '''



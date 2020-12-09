
'''
Module takes data in raw format from the ministry of public administration, stores them into postgreSQL and
converts it into feature vectors for the stream story analysis.
'''

class MJURaw2FeatureVectors:

    def __init__(self, conf, shared):

        self.conf = conf
        self.shared = shared

        # list of fields to be retained as features in feature vector
        # list of fields to be retained as features in feature vector

        self.selectedFieldList = {}
        self.entryOverlapInstructions = {}
        self.selectedFieldListKeys = {}
        self.selectedRawAwardsListKeys = {}
        self.selectedFieldListKeyPositions = {}

        # set date string to identify correct files // example: 6th of January 2020 => 202016
        # set date string to identify correct files // example: 6th of January 2020 => 202016

        self.dateString = ''

        # data storage variables
        # data storage variables

        self.rawData = {}
        self.rawAwards = {}
        self.featureVectors = {}
        self.missingDataStopScript = False

        # file variables
        # file variables

        self.rawTenderDataFileName = 'PostopkiJN_DATE.csv'
        self.rawTenderDataFilePath = conf.tenderDataRawPath

        self.rawAwardsDataFileName = 'PostopkiJNIzvajalci_DATE.csv'
        self.rawAwardsDataFilePath = conf.tenderDataRawPath

        self.joinField = 'IDIzpPriloge'
        self.rawAwardData2BeAppended2Tender = ['PonudnikMaticna', 'PonudnikPostnaStevilka', 'Ponudnik_OBCINA', 'Ponudnik_Velik_EU', 'Ponudnik_Velik_RS']
        self.estimatedTenderValueFieldKey = 'OcenjenaVrednost'
        self.finalTenderValueFieldKey = 'KoncnaVrednost'

        # save config parameters
        # save config parameters

        self.featureVectorsSaveConf = {}

        self.featureVectorsSaveConf['fullFV'] = {}
        self.featureVectorsSaveConf['fullFV']['aggregatedFilePath'] = conf.fullFeatureVectorFormatPath
        self.featureVectorsSaveConf['fullFV']['aggregatedFileName'] = 'feature-vectors.tsv'
        self.featureVectorsSaveConf['fullFV']['dailySourceFilePath'] = conf.fullFeatureVectorFormatPath + 'daily/'
        self.featureVectorsSaveConf['fullFV']['dailySourceFileName'] = 'DATE-feature-vectors.tsv'

        # stream story feature vectors
        # stream story feature vectors

        self.featureVectorsSaveConf['ssFV'] = {}
        self.featureVectorsSaveConf['ssFV']['aggregatedFilePath'] = conf.ssFeatureVectorFormatPath
        self.featureVectorsSaveConf['ssFV']['aggregatedFileName'] = 'stream-story-fv.tsv'
        self.featureVectorsSaveConf['ssFV']['dailySourceFilePath'] = conf.ssFeatureVectorFormatPath + 'daily/'
        self.featureVectorsSaveConf['ssFV']['dailySourceFileName'] = 'DATE-stream-story-fv.tsv'

        # init code dict
        # init code dict

        self.featureVectorMapFile = 'map-REPLACE_KEY.tsv'

        self.codeDict = {}
        self.invokeCategorizationsFromFiles()

    def setFieldsLists(self, fieldsLists, entryOverlapInstructions):
        '''
        function resets listrs of fields to be exported in feature vector tab separated list

        :param fieldsLists: dict
        :return: none
        '''

        # set variable
        # set variable

        self.selectedFieldList = {}
        self.entryOverlapInstructions = {}

        self.selectedFieldList = fieldsLists
        self.entryOverlapInstructions = entryOverlapInstructions

        return None

    def convertRawFiles(self, organizeByUniqueField, fvSaveKey, sortByFirstField = True, queryDatabase = False):
        '''
        function finds all non converted files and sends them into conversion

        :param organizeByUniqueField: a unique field used for organazing the data
        :param fvSaveKey: this enables various conversions into feature vectors; currently there are two: FV for analysis and FV for stream story
        :param sortByFirstField: used for sorting
        :param queryDatabase: this field enables raw data to be inserted into SQL database - as same raw files are being used multiple times for conversion, however they need to be inserted into sql DB only once

        :return: None
        '''

        # test purposes - datestring is already set
        # test purposes - datestring is already set

        if len(self.dateString) > 0:
            self.readRawFile(queryDatabase)
            self.convertRaw2FV(organizeByUniqueField)
            self.save2File(fvSaveKey, sortByFirstField)
            return None

        # normal execution
        # normal execution

        allRawFilesList = [f for f in self.conf.os.listdir(self.conf.tenderDataRawPath) if self.conf.os.path.isfile(self.conf.os.path.join(self.conf.tenderDataRawPath, f)) and 'PostopkiJN_' in f]

        for fileName in allRawFilesList:
            filePieces = fileName.split('_')
            filePieces = filePieces[1].split('.')

            # get converted ff
            # get converted ff

            self.dateString = filePieces[0]
            fulFilePath = self.conf.os.path.join(self.featureVectorsSaveConf[fvSaveKey]['dailySourceFilePath'], self.featureVectorsSaveConf[fvSaveKey]['dailySourceFileName'].replace('DATE', self.dateString))

            if self.conf.os.path.isfile(fulFilePath):
                continue
            else:
                #print('converting: ', fulFilePath)
                self.missingDataStopScript = False
                self.readRawFile(queryDatabase)
                self.convertRaw2FV(organizeByUniqueField)
                self.save2File(fvSaveKey, sortByFirstField)

        # join all daily files to one final file
        # join all daily files to one final file

        self.joinDailyFiles2FinalFile(fvSaveKey, sortByFirstField)

        return None

    def readRawFile(self, queryDatabase):
        '''
        Function reads raw data file in csv format and stores the data in self.rawData variable

        :param queryDatabase: parameter defining, whether data should be stored into database
        :return: None
        '''

        # read tenders and awards file
        # read tenders and awards file

        rawTenderDataFileName = self.rawTenderDataFileName.replace('DATE', self.dateString)
        #print(rawTenderDataFileName)
        #print()
        tenderFilePath = self.conf.os.path.join(self.rawTenderDataFilePath, rawTenderDataFileName)
        if self.fileExists(tenderFilePath):
            tendersData = self.conf.sharedCommon.readDataFile2Dict(tenderFilePath, splitChar = ';')
        else:
            self.missingDataStopScript = True
            return None

        # avoid empty file
        # avoid empty file

        if len(tendersData['data']) == 0:
            self.missingDataStopScript = True
            return None

        # file not empty => store organization names for humanly representable data
        nameIndex = tendersData['head'].index('NarocnikOrganizacija')
        idIndex = tendersData['head'].index('NarocnikMaticna')
        #print(tendersData['head'])
        self.shared.storeMJUOrganizationNames2Db(tendersData['data'], idIndex, nameIndex)

        rawAwardsDataFileName = self.rawAwardsDataFileName.replace('DATE', self.dateString)
        awardsFilePath = self.conf.os.path.join(self.rawAwardsDataFilePath, rawAwardsDataFileName)
        if self.fileExists(tenderFilePath):
            awardsData = self.conf.sharedCommon.readDataFile2Dict(awardsFilePath, splitChar = ';')
        else:
            self.missingDataStopScript = True
            return None

        # avoid empty file
        # avoid empty file

        if len(awardsData['data']) == 0:
            self.missingDataStopScript = True
            return None

        # store raw data into sql DB
        # store raw data into sql DB

        if queryDatabase:
            self.shared.storeMJURaw2SQLDB(tendersData, 'cst_postopki_jn', 'idizppriloge')
            self.shared.storeMJURaw2SQLDB(awardsData, 'cst_postopki_jn_izvajalci', 'id_obrazecsubjekt')

        # for convenient reasons, store organization names for later use
        # for convenient reasons, store organization names for later use

        nameIndex = awardsData['head'].index('PonudnikOrganizacija')
        idIndex = awardsData['head'].index('PonudnikMaticna')
        self.shared.storeMJUOrganizationNames2Db(awardsData['data'], idIndex, nameIndex)

        # create dictionary for fieldName to fieldIndex
        # create dictionary for fieldName to fieldIndex

        awardIndex2Name = {}
        for fieldName in self.rawAwardData2BeAppended2Tender:
            index = awardsData['head'].index(fieldName)
            awardIndex2Name[index] = fieldName

        # organize awardsData by unique field to make it searchable
        # organize awardsData by unique field to make it searchable

        awardsDataOrdered = {}
        keyIndex = awardsData['head'].index(self.joinField)
        #print(keyIndex, self.joinField)
        zaporednaIndex = awardsData['head'].index('Zaporedna')
        for row in awardsData['data']:
            tmp_zaporedna = row[zaporednaIndex]
            tmp_keyIndex = row[keyIndex]

            if tmp_keyIndex not in awardsDataOrdered:
                awardsDataOrdered[tmp_keyIndex] = {}

            awardsDataOrdered[tmp_keyIndex][tmp_zaporedna] = row

        # init data structure:
        # self.rawData
        # self.rawData['head'] => [], feature tender head data
        # self.rawData['data']
        # self.rawData['data'][] => data on specific subtender

        # init data variable
        # init data variable

        self.rawData['head'] = tendersData['head'] + self.rawAwardData2BeAppended2Tender
        # append proportional estimates in case of multiple winners
        self.rawData['head'].append(self.estimatedTenderValueFieldKey + 'Sorazmerno')
        self.rawData['head'].append(self.finalTenderValueFieldKey + 'Sorazmerno')
        self.rawData['data'] = []

        # join tender data and award data into single row :: a single tender can have multiple winners
        # join tender data and award data into single row :: a single tender can have multiple winners

        tenderKeyIndex = tendersData['head'].index(self.joinField)
        for tenderRow in tendersData['data']:

            # find all awardees
            # find all awardees

            tmp_awardTenderKey = tenderRow[tenderKeyIndex]
            awardsDict = awardsDataOrdered[tmp_awardTenderKey]

            # find estimated and final proportional budgets
            # find estimated and final proportional budgets

            estimatedTenderValue_index = tendersData['head'].index(self.estimatedTenderValueFieldKey)
            estimatedTenderValue = self.convert2Numerical(tenderRow[estimatedTenderValue_index], self.estimatedTenderValueFieldKey)
            finalTenderValue_index = tendersData['head'].index(self.finalTenderValueFieldKey)
            finalTenderValue = self.convert2Numerical(tenderRow[finalTenderValue_index], self.finalTenderValueFieldKey)

            numWinners = len(awardsDict)
            proportional_estimatedTenderValue = estimatedTenderValue / numWinners
            proportional_finalTenderValue = finalTenderValue / numWinners

            # attach to every tender row an award row
            # attach to every tender row an award row

            for zaporedna,awardRow in awardsDict.items():
                # for every award create one final row
                # for every award create one final row

                tenderRowCopy = tenderRow.copy()

                for index, fieldName in awardIndex2Name.items():
                    tenderRowCopy.append(awardRow[index])

                # in case multiple winners, add field for proportional share for the budget
                # in case multiple winners, add field for proportional share for the budget

                tenderRowCopy.append(str(proportional_estimatedTenderValue).replace('.', ','))
                tenderRowCopy.append(str(proportional_finalTenderValue).replace('.', ','))

                # append row
                # append row

                self.rawData['data'].append(tenderRowCopy)

        # print(len(self.rawData['data']))
        # print(len(self.rawData['head']))
        # print(len(self.rawData['data'][0]))
        #
        # print(self.rawData['head'])
        # print(self.rawData['data'][0])

        return None

    def convertRaw2FV(self, organizeByUniqueField):
        '''
        Function converts raw MJU data into feature vectors list

        :return: void
        '''

        # continue if data available
        # continue if data available

        if self.missingDataStopScript:
            return None

        # append to head proportional budgets
        # append to head proportional budgets

        proportionalFinalValueKey = self.estimatedTenderValueFieldKey + 'Sorazmerno'
        proportionalAssessedValueKey = self.finalTenderValueFieldKey + 'Sorazmerno'
        self.selectedFieldList[proportionalFinalValueKey] = 'float'
        self.selectedFieldList[proportionalAssessedValueKey] = 'float'

        # then, convert names to keys
        # then, convert names to keys

        self.selectedFieldListKeys = {}
        self.featureVectors['head'] = []
        for fieldName, fieldProp in self.selectedFieldList.items():
            self.featureVectors['head'].append(fieldName)
            # selected fields: fieldName => position in full data list
            key_n = self.rawData['head'].index(fieldName)
            self.selectedFieldListKeys[fieldName] = key_n
            # selected fields: fieldName => position in selected field dict
            pos_n = list(self.selectedFieldList).index(fieldName)
            self.selectedFieldListKeyPositions[fieldName] = pos_n

        # enrich data with proportional budgets
        # enrich data with proportional budgets

        proportionalFinalValueKey_index = self.rawData['head'].index(proportionalFinalValueKey)
        proportionalAssessedValueKey_index = self.rawData['head'].index(proportionalAssessedValueKey)
        self.selectedFieldListKeys[proportionalFinalValueKey] = proportionalFinalValueKey_index
        self.selectedFieldListKeys[proportionalAssessedValueKey] = proportionalAssessedValueKey_index

        selectedFinalValueKey_index = list(self.selectedFieldList).index(proportionalFinalValueKey)
        selectedAssessedValueKey_index = list(self.selectedFieldList).index(proportionalAssessedValueKey)
        self.selectedFieldListKeyPositions[proportionalFinalValueKey] = selectedFinalValueKey_index
        self.selectedFieldListKeyPositions[proportionalAssessedValueKey] = selectedAssessedValueKey_index

        # adding data
        # adding data

        self.featureVectors['data'] = []
        uniqueField_index = self.rawData['head'].index(organizeByUniqueField)
        for tenderRow in self.rawData['data']:
            curr_vector = []
            for fieldName, curr_key in self.selectedFieldListKeys.items():
                # building feature vector
                curr_value = tenderRow[curr_key]
                curr_value = self.convert2Numerical(curr_value, fieldName)
                curr_vector.append(str(curr_value))

            self.featureVectors['data'].append(curr_vector)

        return None

    def convert2Numerical(self, stringValue, fieldName):
        '''
        function takes in a string value and returns an associated numerical value to be inserted into a feature vector

        :param stringValue: input string value
        :return: numValue - a numerical representative of stringValue
        '''

        # lower and upper cases need to be treated equally
        # lower and upper cases need to be treated equally

        stringValue = stringValue.lower()

        # first, check dictKey property
        # first, check dictKey property

        if fieldName in self.selectedFieldList:
            fieldProp = self.selectedFieldList[fieldName]

        # return string
        # return string

        if fieldProp == 'str':
            return str(stringValue)

        # return integers and floats
        # return integers and floats

        if fieldProp == 'int':
            if stringValue == '':
                return 0
            return int(stringValue)

        if fieldProp == 'float':
            if stringValue == '':
                return 0.0
            stringValue = stringValue.replace('.', '')
            stringValue = stringValue.replace(',', '.')
            return float(stringValue)

        # return date / datetime in numerical format
        # return date / datetime in numerical format

        if fieldProp == 'date':
            tmp_list = stringValue.split('-')
            t = self.conf.datetime.datetime(int(tmp_list[0]), int(tmp_list[1]), int(tmp_list[2]), 0, 0)
            return int((t - self.conf.datetime.datetime(1970, 1, 1)).total_seconds())

        if fieldProp == 'datetime':
            tmp_list = stringValue.split(' ')
            date_list = tmp_list[0].split('-')
            time_list = tmp_list[1].split(':')
            t = self.conf.datetime.datetime(int(date_list[0]), int(date_list[1]), int(date_list[2]), int(time_list[0]), int(time_list[1]), int(time_list[2]))
            return int((t - self.conf.datetime.datetime(1970, 1, 1)).total_seconds())

        # return numerical employees num EU
        # return numerical employees num EU

        employeesNum = {}
        employeesNum['0 zaposlenih'] = 0.1
        employeesNum['1 zaposlen'] = 1
        employeesNum['2 zaposlena'] = 2
        employeesNum['3 ali 4 zaposleni'] = 3
        employeesNum['5 do 9 zaposlenih'] = 7
        employeesNum['10 do 19 zaposlenih'] = 15
        employeesNum['20 do 49 zaposlenih'] = 35
        employeesNum['50 do 99 zaposlenih'] = 75
        employeesNum['100 do 149 zaposlenih'] = 125
        employeesNum['150 do 199 zaposlenih'] = 175
        employeesNum['200 do 249 zaposlenih'] = 225
        employeesNum['250 do 499 zaposlenih'] = 375
        employeesNum['500 do 999 zaposlenih'] = 750
        employeesNum['nad 1000 zaposlenih'] = 2000

        # in case of data missing about emplyees this is the logic:
        # minimise number on supplier side
        # maximise number of provider side
        # this approach kind of keeps potential anomalies => better to create a false anomaly than to lose one

        if fieldProp == 'nempl_byr':
            employeesNum['ni podatka o zaposlenih'] = 2000
            employeesNum['null'] = 2000
            employeesNum[''] = 2000
            return employeesNum[stringValue]
        elif fieldProp == 'nempl_bidr':
            employeesNum['ni podatka o zaposlenih'] = 1
            employeesNum['null'] = 1
            employeesNum[''] = 1
            return employeesNum[stringValue]

        # return numerical employees num SI
        # return numerical employees num SI

        employeesNumRS = {}
        employeesNumRS['mikro enote'] = 1
        employeesNumRS['majhne enote'] = 10
        employeesNumRS['srednje enote'] = 100
        employeesNumRS['velike enote'] = 1000
        employeesNumRS['velikost rs se ne izračunava'] = 0
        employeesNumRS[''] = 0
        employeesNumRS['null'] = 0
        employeesNumRS['ni podatka o velikosti'] = 0

        # in case of data missing about emplyees this is the logic:
        # minimise number on supplier side
        # maximise number of provider side
        # this approach kind of keeps potential anomalies => better to create a false anomaly than to lose one

        if fieldProp == 'nempl_byr_rs':
            employeesNumRS['velikost rs se ne izračunava'] = 1000
            employeesNumRS[''] = 1000
            employeesNumRS['null'] = 1000
            employeesNumRS['ni podatka o velikosti'] = 1000
            if stringValue in employeesNumRS:
                return employeesNumRS[stringValue]
            else:
                return 1000
        elif fieldProp == 'nempl_bidr_rs':
            employeesNumRS['velikost rs se ne izračunava'] = 1
            employeesNumRS[''] = 1
            employeesNumRS['null'] = 1
            employeesNumRS['ni podatka o velikosti'] = 1
            if stringValue in employeesNumRS:
                return employeesNumRS[stringValue]
            else:
                return 1

        # return categorized values
        # return categorized values

        self.selectedRawAwardsListKeys

        if fieldName in self.selectedFieldListKeys:
            dictKey = self.selectedFieldListKeys[fieldName]
            key_code = (self.rawData['head'][dictKey]).lower()
        elif fieldName in self.selectedRawAwardsListKeys:
            dictKey = self.selectedRawAwardsListKeys[fieldName]
            key_code = (self.rawAwards['head'][dictKey]).lower()

        if key_code not in self.codeDict:
            self.codeDict[key_code] = {}

        # init a new association rule if yet not existing
        # init a new association rule if yet not existing

        if stringValue not in self.codeDict[key_code]:
            #print('NOT')
            self.codeDict[key_code][stringValue] = len(self.codeDict[key_code]) + 1

        # return associated value
        # return associated value

        return self.codeDict[key_code][stringValue]

    def fileExists(self, fullFilePath):
        '''
        function checks whether files exist

        :return: boolean
        '''

        if self.conf.os.path.exists(fullFilePath):
            return True
        else:
            return False

    def save2File(self, fvSaveKey, sortByFirstField = True):
        '''
        Function saves to file data stored in self.featureVectors and self.codeDict

        :return: boolean
        '''

        # no data - no save
        # no data - no save

        if len(self.featureVectors) == 0:
            return None

        if len(self.featureVectors['data']) == 0:
            return None

        # sort by first field
        # sort by first  field

        if sortByFirstField:
            self.featureVectors['data'].sort(key=lambda x: x[0])

        # save feature vectors 2 file
        # save feature vectors 2 file

        fullFileName = ''
        fullFileName += self.featureVectorsSaveConf[fvSaveKey]['dailySourceFilePath']
        fullFileName += self.featureVectorsSaveConf[fvSaveKey]['dailySourceFileName'].replace('DATE', self.dateString)
        self.conf.sharedCommon.sendDict2Output(self.featureVectors, fullFileName)

        # save categorizations 2 files
        # save categorizations 2 files

        self.saveCategorizations2File()

        return None

    def joinDailyFiles2FinalFile(self, fvSaveKey, sortByFirstField = True):
        '''
        function joins all daily feature vector files into one big file

        :return: none
        '''

        allFiles = [f for f in self.conf.os.listdir(self.featureVectorsSaveConf[fvSaveKey]['dailySourceFilePath']) if self.conf.os.path.isfile(self.conf.os.path.join(self.featureVectorsSaveConf[fvSaveKey]['dailySourceFilePath'], f))]

        # filter files to start with '20'
        # filter files to start with '20'

        dailySSFV = [curFile for curFile in allFiles if curFile[:2] == '20']

        # read files line by line
        # read files line by line

        finalData = {}
        finalData['head'] = []
        finalData['data'] = []
        for fileName in dailySSFV:
            # read data into var
            fullFileName = self.featureVectorsSaveConf[fvSaveKey]['dailySourceFilePath'] + fileName
            currData = self.conf.sharedCommon.readDataFile2Dict(fullFileName, "\t")

            if len(finalData['head']) == 0:
                finalData['head'] = currData['head']

            for tmp_row in currData['data']:
                finalData['data'].append(tmp_row)

        # filter data
        # filter data

        if sortByFirstField:
            finalData['data'].sort(key=lambda x: x[0])

        # save aggregated data into final file
        # save aggregated data into final file

        fullFileName = self.featureVectorsSaveConf[fvSaveKey]['aggregatedFilePath'] + self.featureVectorsSaveConf[fvSaveKey]['aggregatedFileName']
        self.conf.sharedCommon.sendDict2Output(finalData, fullFileName)

        return None

    def saveCategorizations2File(self):
        '''
        function saves categorizations, a map between descriptive strings and associated integers, to files

        :return: none
        '''

        dictionary = {}
        dictionary['head'] = ['value', 'field']
        for tmp_key, tmp_dict in self.codeDict.items():
            dictionary['data'] = []
            for field_key, field_value in tmp_dict.items():
                dictionary['data'].append([str(field_value), str(field_key)])

            tmp_fileName = self.conf.featureVectorMapPath + self.featureVectorMapFile.replace('REPLACE_KEY', tmp_key)
            self.conf.sharedCommon.sendDict2Output(dictionary, tmp_fileName.lower())

        return None

    def invokeCategorizationsFromFiles(self):
        '''
        inverse operation to 'saveCategorizations2File'

        :return: none
        '''

        # get all files in self.conf.featureVectorMapPath directory
        # get all files in self.conf.featureVectorMapPath directory

        allFiles = [f for f in self.conf.os.listdir(self.conf.featureVectorMapPath) if self.conf.os.path.isfile(self.conf.os.path.join(self.conf.featureVectorMapPath, f))]

        # filter files to start with 'map-'
        # filter files to start with 'map-'

        mapFiles = [curFile for curFile in allFiles if curFile[:4] == 'map-']

        # import data in files into varable
        # import data in files into varable

        for file in mapFiles:
            fullFileName = self.conf.featureVectorMapPath + file
            tmpDict = self.conf.sharedCommon.readDataFile2Dict(fullFileName, "\t")
            tmpCatName = file[4:-4]

            self.codeDict[tmpCatName] = {}
            for valueList in tmpDict['data']:
                self.codeDict[tmpCatName][str(valueList[1])] = int(valueList[0])

        return None
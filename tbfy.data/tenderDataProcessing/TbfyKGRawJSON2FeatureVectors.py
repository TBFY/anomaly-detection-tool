
'''
Module takes data in raw format from the TBFY KG and converts it into feature vectors for later data analysis
'''

import json
from shutil import copyfile

class TbfyKGRawJSON2FeatureVectors:

    def __init__(self, conf, shared):

        self.conf = conf
        self.shared = shared

        # source and destination paths
        # source and destination paths

        self.tbfyKGRawFilePath = self.conf.tbfyKGRawDataPath
        self.tbfyKGFeatureVectorsPath = self.conf.tbfyKGFeatureVectorsDataPath

        # storage vars
        # storage vars

        self.rawFilesDirs2ProcessList = []
        self.suppliersDataDict = {}
        self.organizationNames = {}
        self.organizationNames['head'] = ['orgCountry, orgId, orgName']
        self.organizationNames['data'] = []

        self.featureVectorsDict = {}
        self.featureVectorsDict['head'] = []
        self.featureVectorsDict['data'] = {}

        self.fullFeatureVectorsDict = {}
        self.fullFeatureVectorsDict['head'] = []
        self.fullFeatureVectorsDict['data'] = {}

        # init code dict
        # init code dict

        self.featureVectorMapFile = 'map-REPLACE_KEY.tsv'

        self.categoryMappingDict = {}
        self.invokeCategorizationsFromFiles()

    #### START functions selecting files for processing ####
    #### START functions selecting files for processing ####
    #### START functions selecting files for processing ####

    def createListOfDirsForConversion(self):
        '''
        function identifies all directories, that were not yet processed

        :return: None
        '''

        # set list up only if not empty
        # set list up only if not empty

        if len(self.rawFilesDirs2ProcessList) > 0:
            return None

        # find all raw data directories
        # find all raw data directories

        raw_data_dirs_list = [f.name for f in self.conf.os.scandir(self.tbfyKGRawFilePath) if f.is_dir()]

        # find all converted data files
        # find all converted data files

        path2processed = self.tbfyKGFeatureVectorsPath + 'daily/'
        processed_dates_list = [f.name for f in self.conf.os.scandir(path2processed) if f.is_dir()]

        # determine not yet processed directories
        # determine not yet processed directories

        self.rawFilesDirs2ProcessList = [x for x in raw_data_dirs_list if x not in processed_dates_list]

        return None

    def createSuppliersDataDict(self):
        '''
        function looks for all files with 'supplier' in file name, extracts json from it and stores it in local dict

        :return: None
        '''

        # find file with supplier data
        # find file with supplier data

        for directory in self.rawFilesDirs2ProcessList:
            directoryFullPath = self.conf.os.path.join(self.tbfyKGRawFilePath, directory)
            supplierFileList = [f.name for f in self.conf.os.scandir(directoryFullPath) if '-supplier-' in f.name]

            for supplierFileName in supplierFileList:
                fullSupplierFilePath = self.conf.os.path.join(directoryFullPath, supplierFileName)
                with open(fullSupplierFilePath, 'r', encoding="utf-8") as fs:
                    jsonSupplierDict = json.load(fs)
                    tmp_companyName = jsonSupplierDict['results']['company']['name'].lower()
                    if tmp_companyName not in self.suppliersDataDict:
                        self.suppliersDataDict[tmp_companyName] = {}
                    self.suppliersDataDict[tmp_companyName]['fileName'] = fullSupplierFilePath
                    self.suppliersDataDict[tmp_companyName]['jsonData'] = jsonSupplierDict

        return None

    #### END functions selecting files for processing ####
    #### END functions selecting files for processing ####
    #### END functions selecting files for processing ####

    def convertRaw2FV(self):
        '''
        Function converts raw MJU data into stream story feature vectors

        :return: void
        '''

        # first create of list of directories (containing files) that will be converted
        # first create of list of directories (containing files) that will be converted

        self.createListOfDirsForConversion()
        self.createSuppliersDataDict()

        # from dir to dir - convert all containing files
        # from dir to dir - convert all containing files

        for curr_directoryDate in self.rawFilesDirs2ProcessList:
            #print(curr_directoryDate)
            # get all files from directoryFullPath
            directoryFullPath = self.conf.os.path.join(self.tbfyKGRawFilePath, curr_directoryDate)
            allFilesInDirList = [f for f in self.conf.os.listdir(directoryFullPath) if self.conf.os.path.isfile(self.conf.os.path.join(directoryFullPath, f)) and 'award' in f]

            # convert file by file into a feature vectos list
            for awardFile in allFilesInDirList:
                self.convertOCDSFile2FV(curr_directoryDate, awardFile)

        return None

    def convertOCDSFile2FV(self, curr_directoryDate, awardFile):
        '''
        function converts a file into a feature vector

        :param fullFilePath: full path to a file to be converted
        :return: None
        '''

        # reading data into dict
        # reading data into dict

        directoryFullPath = self.conf.os.path.join(self.tbfyKGRawFilePath, curr_directoryDate)
        fullFilePath = self.conf.os.path.join(directoryFullPath, awardFile)

        # abort if file has no contencts
        # abort if file has no contencts

        if self.conf.os.path.getsize(fullFilePath) < 10:
            return None

        with open(fullFilePath, 'r', encoding="utf-8") as f:
            jsonDict = json.load(f)
            #print(fullFilePath)
            fileContentString = self.conf.sharedCommon.fileGetContents(fullFilePath)

            # find all tender lots; every lot is a single feature vector
            # find all tender lots; every lot is a single feature vector

            featureVectorsDictHeadInConstruction = True if len(self.featureVectorsDict['head']) == 0 else False
            fullFeatureVectorsDictHeadInConstruction = True if len(self.fullFeatureVectorsDict['head']) == 0 else False
            for release in jsonDict['releases']:

                # every release can have several lot awardees
                # every release can have several lot awardees

                last_item_n = 0
                for award_n, award in enumerate(release['awards']):
                    curr_fv_list = []
                    # adding ocid
                    if featureVectorsDictHeadInConstruction:
                        self.featureVectorsDict['head'].append('ocid')
                    curr_fv_list.append(str(release['ocid']))
                    # adding award id
                    if featureVectorsDictHeadInConstruction:
                        self.featureVectorsDict['head'].append('award_id')
                    curr_fv_list.append(str(award['id']))
                    # adding date in linux seconds
                    if featureVectorsDictHeadInConstruction:
                        self.featureVectorsDict['head'].append('publishDate')
                    if 'date' in award:
                        curr_fv_list.append(str(self.convert2Numerical(award['date'], 'datetime')))
                    else:
                        curr_fv_list.append(str(self.convert2Numerical(release['date'], 'datetime')))

                    # adding tender cpv code
                    if 'items' in release['tender']:
                        if award_n in release['tender']['items']:
                            item_n = award_n
                            last_item_n = item_n
                        else:
                            item_n = last_item_n
                        cpvCode = release['tender']['items'][item_n]['classification']['id']
                    else:
                        cpvCode = '0'

                    if featureVectorsDictHeadInConstruction:
                        self.featureVectorsDict['head'].append('cpv')
                    curr_fv_list.append(cpvCode)

                    # adding ted publishing
                    if featureVectorsDictHeadInConstruction:
                        self.featureVectorsDict['head'].append('publishedOnTed')
                    publishedOnTed = 0 if fileContentString.find('ted.europa.eu') == -1 else 1
                    curr_fv_list.append(str(publishedOnTed))
                    # adding tender value
                    if featureVectorsDictHeadInConstruction:
                        self.featureVectorsDict['head'].append('amount')
                        self.featureVectorsDict['head'].append('currency')
                    if 'value' in award and 'amount' in award['value']:
                        curr_fv_list.append(str(award['value']['amount']))
                        if 'currency' in award['value']:
                            curr_fv_list.append(str(self.convert2Numerical(award['value']['currency'], 'currency')))
                        elif publishedOnTed == 1:
                            curr_fv_list.append(str(self.convert2Numerical('eur', 'currency')))
                        else:
                            curr_fv_list.append(str(self.convert2Numerical('eur', 'currency')))
                    else:
                        curr_fv_list.append('0')
                        curr_fv_list.append('0')
                    # adding buyer data
                    if featureVectorsDictHeadInConstruction:
                        self.featureVectorsDict['head'].append('buyerPostId')
                        self.featureVectorsDict['head'].append('buyerCountry')
                    if 'buyer' in release:
                        postId = 0 if ('address' not in release['buyer'] or 'postalCode' not in release['buyer']['address']) else release['buyer']['address']['postalCode']
                        buyerCountry = self.convert2Numerical(release['buyer']['address']['countryName'], 'country-name')
                        #buyerName = release['buyer']['name']
                    else:
                        postId = 0
                        buyerCountry = self.convert2Numerical('', 'country-name')
                        #buyerName = '-'
                    curr_fv_list.append(str(postId))
                    curr_fv_list.append(str(buyerCountry))
                    # adding supplier data
                    if featureVectorsDictHeadInConstruction:
                        self.featureVectorsDict['head'].append('supplierCountry')
                    if 'suppliers' in award and len(award['suppliers']) > 0:
                        # supplier address
                        if 'address' in award['suppliers'][0] and 'countryName' in award['suppliers'][0]['address']:
                            supplierCountry = self.convert2Numerical(award['suppliers'][0]['address']['countryName'], 'country-name')
                        else:
                            supplierCountry = buyerCountry
                    else:
                        supplierCountry = self.convert2Numerical('', 'country-name')
                    curr_fv_list.append(str(supplierCountry))
                    # adding award criteria
                    if featureVectorsDictHeadInConstruction:
                        self.featureVectorsDict['head'].append('awardCriteriaDetails')
                    if 'awardCriteriaDetails' in release['tender']:
                        curr_fv_list.append(str(self.convert2Numerical(release['tender']['awardCriteriaDetails'], 'award-criteria')))
                    else:
                        curr_fv_list.append('0')

                    # append fv to the list // organize by country
                    # append fv to the list // organize by country

                    buyerCountryName = list(self.categoryMappingDict['country-name'].keys())[list(self.categoryMappingDict['country-name'].values()).index(buyerCountry)]

                    if curr_directoryDate not in self.featureVectorsDict['data']:
                        self.featureVectorsDict['data'][curr_directoryDate] = {}

                    if buyerCountryName not in self.featureVectorsDict['data'][curr_directoryDate]:
                        self.featureVectorsDict['data'][curr_directoryDate][buyerCountryName] = []

                    self.featureVectorsDict['data'][curr_directoryDate][buyerCountryName].append(curr_fv_list)

                    # disable head generation
                    # disable head generation

                    if featureVectorsDictHeadInConstruction == True:
                        featureVectorsDictHeadInConstruction = False

                    # add supplier data
                    # add supplier data

                    if 'suppliers' in award:
                        tmp_companyName = award['suppliers'][0]['name'].lower()
                        if tmp_companyName in self.suppliersDataDict:
                            # creating head
                            if fullFeatureVectorsDictHeadInConstruction:
                                self.fullFeatureVectorsDict['head'] = self.featureVectorsDict['head'].copy()
                            supplierJson = self.suppliersDataDict[tmp_companyName]['jsonData']
                            curr_full_fv_list = curr_fv_list.copy()
                            # adding supplier num of employees
                            if fullFeatureVectorsDictHeadInConstruction:
                                self.fullFeatureVectorsDict['head'].append('supplier_num_employees')
                            supplier_num_employees = '0' if 'number_of_employees' not in supplierJson['results']['company'] else supplierJson['results']['company']['number_of_employees']
                            curr_full_fv_list.append(str(self.convert2Numerical(str(supplier_num_employees), 'num-of-employees')))
                            # adding supplier company id
                            if fullFeatureVectorsDictHeadInConstruction:
                                self.fullFeatureVectorsDict['head'].append('supplier_company_id')
                            curr_full_fv_list.append(str(supplierJson['results']['company']['company_number']))
                            # adding jurisdiction code
                            if fullFeatureVectorsDictHeadInConstruction:
                                self.fullFeatureVectorsDict['head'].append('supplier_jurisdiction')
                            jurisdiction_code = supplierJson['results']['company']['jurisdiction_code']
                            curr_full_fv_list.append(str(jurisdiction_code))
                            # adding if supplier changed name
                            if fullFeatureVectorsDictHeadInConstruction:
                                self.fullFeatureVectorsDict['head'].append('supplier_changed_name')
                            supplier_changed_name = 0 if len(supplierJson['results']['company']['previous_names']) == 0 else 1
                            curr_full_fv_list.append(str(supplier_changed_name))
                            # adding supplier postal code
                            if fullFeatureVectorsDictHeadInConstruction:
                                self.fullFeatureVectorsDict['head'].append('supplier_postal_code')
                            if 'registered_address' in supplierJson['results']['company']:
                                curr_full_fv_list.append(str(supplierJson['results']['company']['registered_address']['postal_code']))
                            else:
                                curr_full_fv_list.append('0')

                            # add fv to supplier list
                            # add fv to supplier list

                            if curr_directoryDate not in self.fullFeatureVectorsDict['data']:
                                self.fullFeatureVectorsDict['data'][curr_directoryDate] = {}

                            if buyerCountryName not in self.fullFeatureVectorsDict['data'][curr_directoryDate]:
                                self.fullFeatureVectorsDict['data'][curr_directoryDate][buyerCountryName] = []

                            self.fullFeatureVectorsDict['data'][curr_directoryDate][buyerCountryName].append(curr_full_fv_list)

                            # disable head generation
                            # disable head generation

                            if fullFeatureVectorsDictHeadInConstruction == True:
                                fullFeatureVectorsDictHeadInConstruction = False

        return None

    def save2File(self):

        # save categorizations 2 files
        # save categorizations 2 files

        self.saveCategorizations2File()

        # save scarce feature vectors into files
        # save scarce feature vectors into files

        filePath = self.conf.os.path.join(self.conf.tbfyKGFeatureVectorsDataPath, 'daily')
        for directoryDate, dataDict in self.featureVectorsDict['data'].items():
            # if not exixtent, create directory
            newFilePath = self.conf.os.path.join(filePath, directoryDate)
            if not self.conf.os.path.exists(newFilePath):
                self.conf.os.makedirs(newFilePath)

            for countryName, dataDictCountry in self.featureVectorsDict['data'][directoryDate].items():
                fileName = countryName.replace(' ', '-') + '-tbfy-kg-scarce-fv.tsv'
                tmp_dict = {}
                tmp_dict['head'] = self.featureVectorsDict['head']
                tmp_dict['data'] = dataDictCountry
                self.conf.sharedCommon.sendDict2Output(tmp_dict, self.conf.os.path.join(newFilePath, fileName))

        # save full feature vectors into files
        # save full feature vectors into files

        filePath = self.conf.os.path.join(self.conf.tbfyKGFeatureVectorsDataPath, 'daily')
        for directoryDate, dataDict in self.fullFeatureVectorsDict['data'].items():
            # if not exixtent, create directory
            newFilePath = self.conf.os.path.join(filePath, directoryDate)
            if not self.conf.os.path.exists(newFilePath):
                self.conf.os.makedirs(newFilePath)
            for countryName, dataDictCountry in self.fullFeatureVectorsDict['data'][directoryDate].items():
                fileName = countryName.replace(' ', '-') + '-tbfy-kg-full-fv.tsv'
                tmp_dict = {}
                tmp_dict['head'] = self.fullFeatureVectorsDict['head']
                tmp_dict['data'] = dataDictCountry
                self.conf.sharedCommon.sendDict2Output(tmp_dict, self.conf.os.path.join(newFilePath, fileName))

        # join all daily fv files into one single fv file
        # join all daily fv files into one single fv file

        self.joinDailyFiles2OneFile()

        return None

    def joinDailyFiles2OneFile(self):
        '''
        function is joining daily feature vectors files into one single national file

        :return: None
        '''

        for curr_directoryDate in self.rawFilesDirs2ProcessList:

            directoryFullPath = self.conf.os.path.join(self.conf.tbfyKGFeatureVectorsDataPath, 'daily')
            directoryFullPath = self.conf.os.path.join(directoryFullPath, curr_directoryDate)

            # first, destination dir needs to exist
            # first, destination dir needs to exist

            if self.conf.os.path.exists(directoryFullPath) == False:
                continue

            # join scarce files
            # join scarce files

            allScarceFilesInDirList = [f for f in self.conf.os.listdir(directoryFullPath) if self.conf.os.path.isfile(self.conf.os.path.join(directoryFullPath, f)) and '-scarce-' in f]

            if len(allScarceFilesInDirList) > 0:
                for scarceFileName in allScarceFilesInDirList:
                    filePieces = scarceFileName.split('-tbfy-')
                    # get aggregator file name
                    aggregatorBaseFile = filePieces[0].lower() + '-tbfy-kg-scarce-aggregated.tsv'
                    fullAggregatorFileName = self.conf.os.path.join(self.conf.tbfyKGFeatureVectorsDataPath, aggregatorBaseFile)
                    # get file name to be appended
                    file2Append = self.conf.os.path.join(self.conf.tbfyKGFeatureVectorsDataPath, 'daily')
                    file2Append = self.conf.os.path.join(file2Append, curr_directoryDate)
                    file2Append = self.conf.os.path.join(file2Append, scarceFileName)
                    # append file to aggregator
                    self.appendFileContents2Aggregator(file2Append, fullAggregatorFileName)

            # join full files
            # join full files

            allFulFVFilesInDirList = [f for f in self.conf.os.listdir(directoryFullPath) if self.conf.os.path.isfile(self.conf.os.path.join(directoryFullPath, f)) and '-full-' in f]
            if len(allFulFVFilesInDirList) > 0:
                for fullFVFileName in allFulFVFilesInDirList:
                    filePieces = fullFVFileName.split('-tbfy-')
                    # get aggregator file name
                    aggregatorBaseFile = filePieces[0].lower() + '-tbfy-kg-fullfv-aggregated.tsv'
                    fullAggregatorFileName = self.conf.os.path.join(self.conf.tbfyKGFeatureVectorsDataPath, aggregatorBaseFile)
                    # get file name to be appended
                    file2Append = self.conf.os.path.join(self.conf.tbfyKGFeatureVectorsDataPath, 'daily')
                    file2Append = self.conf.os.path.join(file2Append, curr_directoryDate)
                    file2Append = self.conf.os.path.join(file2Append, fullFVFileName)
                    # append file to aggregator
                    self.appendFileContents2Aggregator(file2Append, fullAggregatorFileName)

        return None

    def appendFileContents2Aggregator(self, file2Append, fullAggregatorFileName):
        '''
        function takes contents of file file2Append and appends it to a file fullAggregatorFileName

        :param file2Append: string, full path to file
        :param fullAggregatorFileName: string, full path to file
        :return: None
        '''

        # if aggregated file does not exist, simply copy file2Append
        # if aggregated file does not exist, simply copy file2Append

        if self.conf.os.path.exists(fullAggregatorFileName) == False:
            copyfile(file2Append, fullAggregatorFileName)
            return None

        with open(file2Append, "r", encoding="utf-8") as f:
            contents2AppendList = f.readlines()[1:]
            contents2Append = "".join(contents2AppendList)

        with open(fullAggregatorFileName, "a", encoding="utf-8") as myfile:
            myfile.write(contents2Append)

        return None

    def convert2Numerical(self, stringValue, fieldType):
        '''
        function takes in a string value and returns an associated numerical value to be inserted into a feature vector

        :param stringValue: input string value
        :return: numValue - a numerical representative of stringValue
        '''

        # convert datetime into linux time (seconds)
        # convert datetime into linux time (seconds)

        if fieldType == 'datetime':
            # there are various formats of data time varibale:
            # YYYY-MM-DDTHH:MM:SS+00:00
            # YYYY-MM-DDTHH:MM:SSZ

            tmp_datetime = stringValue.split('T')
            date_list = tmp_datetime[0].split('-')
            time_list = tmp_datetime[1][0:8].split(':')
            t = self.conf.datetime.datetime(int(date_list[0]), int(date_list[1]), int(date_list[2]), int(time_list[0]), int(time_list[1]), int(time_list[2]))
            return int((t - self.conf.datetime.datetime(1970, 1, 1)).total_seconds())

        # return number of employees
        # return number of employees

        if fieldType == 'num-of-employees':
            if stringValue.lower() == '1000-999999':
                return 2000
            if stringValue.lower() == '10000-':
                return 10000
            if stringValue.lower() == '0':
                return 0.1
            if stringValue.find('-') > 0:
                employeesValuesList = stringValue.split('-')
                if len(employeesValuesList) != 2:
                    print('num of employees error 1 value: ', stringValue)
                else:
                    employeesNumVal1 = int(employeesValuesList[0])
                    employeesNumVal2 = int(employeesValuesList[1])
                    if str(employeesNumVal1) != employeesValuesList[0] or str(employeesNumVal2) != employeesValuesList[1]:
                        print('num of employees error 2 value: ', stringValue)
                    return int(0.5 * (employeesNumVal2 + employeesNumVal1))
            if stringValue.strip() == '':
                return 0
            if str(int(stringValue)) == stringValue:
                return int(stringValue)

            print('no num-employees classification: ', stringValue, 'heh')
            return 0

        # convert abbreviations or double labels
        # convert abbreviations or double labels

        if fieldType == 'country-name':
            stringValue = self.returnCountryName(stringValue)

        if fieldType == 'award-criteria':
            if stringValue.lower() == 'other' or stringValue.lower() == '':
                stringValue = 'not specified'

        # return categorized values
        # return categorized values

        fieldType = fieldType.lower()
        stringValue = stringValue.lower()

        if fieldType not in self.categoryMappingDict:
            self.categoryMappingDict[fieldType] = {}

        # init a new association rule if yet not existing
        # init a new association rule if yet not existing

        if stringValue not in self.categoryMappingDict[fieldType]:
            self.categoryMappingDict[fieldType][stringValue] = len(self.categoryMappingDict[fieldType]) + 1

        # return associated value
        # return associated value

        return self.categoryMappingDict[fieldType][stringValue]

    def returnCountryName(self, stringValue):
        '''
        function accepts various country names and returns a unified country name

        :param stringValue: string, country name
        :return: string, country name
        '''

        stringCountryConversions = {
            'pt': 'portugal',
            'pt': 'portugal',
            'fr': 'france',
            'uk': 'united kingdom',
            'es': 'spain',
            'pl': 'poland',
            'se': 'sweden',
            'be': 'belgium',
            'mt': 'malta',
            'ro': 'romania',
            'it': 'italy',
            'bg': 'bulgaria',
            'hu': 'hungary',
            'no': 'norway',
            'cy': 'cyprus',
            'cz': 'czech republic',
            'nl': 'netherlands',
            'lt': 'lithuania',
            'lu': 'luxembourg',
            'gr': 'greece',
            'at': 'austria',
            'ee': 'estonia',
            'dk': 'denmark',
            'si': 'slovenia',
            'ch': 'switzerland',
            'mk': 'macedonia',
            'sk': 'slovakia',
            'ie': 'ireland',
            'de': 'germany',
            'lv': 'latvia',
            'sa': 'saudi arabia',
            'us': 'us',
            'hr': 'croatia',
            'fi': 'finland',
            'rs': 'serbia',
            'au': 'australia',
            'tr': 'turkey',
            'is': 'iceland',
            'sr': 'suriname',
            'ad': 'andorra',
            'bt': 'bhutan',
            'jp': 'japan',
            'by': 'belarus',
            'ru': 'russia',
            'ca': 'canada',
            'li': 'liechtenstein',
            'ba': 'bosnia and herzegovina',
            'al': 'albania',
            'ua': 'ukraine',
            'gi': 'gibraltar',
            '': 'undefined'
        }

        stringValue = stringValue.lower()
        if stringValue in stringCountryConversions:
            return stringCountryConversions[stringValue]
        else:
            return stringValue

    def saveCategorizations2File(self):
        '''
        function saves categorizations, a map between descriptive strings and associated integers, to files

        :return: none
        '''

        dictionary = {}
        dictionary['head'] = ['value', 'field']
        for tmp_key, tmp_dict in self.categoryMappingDict.items():
            dictionary['data'] = []
            for field_key, field_value in tmp_dict.items():
                dictionary['data'].append([str(field_value), str(field_key)])

            tmp_fileName = self.conf.tbfyKGFeatureVectorMapPath + self.featureVectorMapFile.replace('REPLACE_KEY', tmp_key)
            self.conf.sharedCommon.sendDict2Output(dictionary, tmp_fileName.lower())

        return None

    def invokeCategorizationsFromFiles(self):
        '''
        inverse operation to 'saveCategorizations2File'

        :return: none
        '''

        # get all files in self.conf.tbfyKGFeatureVectorMapPath directory
        # get all files in self.conf.tbfyKGFeatureVectorMapPath directory

        allFiles = [f for f in self.conf.os.listdir(self.conf.tbfyKGFeatureVectorMapPath) if self.conf.os.path.isfile(self.conf.os.path.join(self.conf.tbfyKGFeatureVectorMapPath, f))]

        # filter files to start with 'map-'
        # filter files to start with 'map-'

        mapFiles = [curFile for curFile in allFiles if curFile[:4] == 'map-']

        # import data in files into varable
        # import data in files into varable

        for file in mapFiles:
            fullFileName = self.conf.tbfyKGFeatureVectorMapPath + file
            tmpDict = self.conf.sharedCommon.readDataFile2Dict(fullFileName, "\t")
            tmpCatName = file[4:-4]

            self.categoryMappingDict[tmpCatName] = {}
            for valueList in tmpDict['data']:
                self.categoryMappingDict[tmpCatName][str(valueList[1])] = int(valueList[0])

        return None


class FVcustomization:

    def __init__(self, conf, getVars):

        self.conf = conf
        self.getVars = getVars
        self.contentHtml = 'Error: SearchModel HTML nof found.'

        # custom vars
        # custom vars

        self.invokedMaps = {}
        self.index2fieldNameConverter = {}
        self.fileContent = {}

    def getView(self):
        '''
        core function to serve a correct / selected view

        :return: string, html format
        '''

        query_t = "landing" if self.getVars.get('t') == None else self.getVars.get('t')
        query_t = query_t.lower()

        # get content HTML
        # get content HTML

        if(query_t == "landing"):
            self.contentHtml = self.getFFCustomizationPage()
        elif(query_t == "dlff_file"):
            self.contentHtml = self.downloadCustomFFDataFile()
        else:
            self.contentHtml = self.conf.sharedMethods.getErrorView(self.conf)

        return self.contentHtml

    def getFFCustomizationPage(self):
        '''
        function returns main landing page

        :return: string, html format
        '''

        # get predefined buyer groups
        # get predefined buyer groups

        sql = self.conf.cDB.sql
        cur = self.conf.cDB.db.cursor()
        shared = self.conf.sharedCommon

        queryBase = "select kategorija, count(*) from su_rpu group by kategorija;"
        queryString = sql.SQL(queryBase)
        cur.execute(queryString)
        # print(queryString.as_string(cur))
        contractees = shared.returnSqlDataInDictFormat(cur)
        # print(contractees)

        buyerGroups = {}
        for row in contractees:
            if row['kategorija'] == None:
                continue
            else:
                buyerGroups[row['kategorija']] = row['kategorija']

        # get menu
        # get menu

        import models.TendersModel as Tenders
        tenderModel = Tenders.TendersModel(self.conf, self.getVars)

        # generate html view
        # generate html view

        dict = {}
        dict["buyerGroups"] = buyerGroups
        dict['tenderMenu'] = tenderModel.getTenderMenu()

        content = self.conf.Template(filename='templates/te_fv_customization.tpl')
        return content.render(data=dict)

    def downloadCustomFFDataFile(self):
        '''
        function creates a custom ff file and sends it back to the user

        :return: ff custom file in form of string
        '''

        filteredDict = self.filterDataAccordingCriteria()
        filteredString = self.convertDict2String(filteredDict)
        self.exportString(filteredString)

        # kill execution at this point
        # kill execution at this point

        self.conf.sys.exit("")

    def filterDataAccordingCriteria(self):
        '''
        function reads data file and filters it according selected parameters

        :return: dictionary
        '''

        fullFilePath = self.conf.sourceFFTenderDataRoot + 'SSFeatureVectors/stream-story-fv.tsv'
        self.fileContent = self.conf.sharedCommon.readDataFile2Dict(fullFilePath, '\t')

        # get data filters
        # get data filters

        query_buyerId = "" if self.getVars.get('buyerId') == None else self.getVars.get('buyerId')
        query_buyerId = self.conf.urllib.parse.unquote(query_buyerId)

        query_bidderId = "" if self.getVars.get('bidderId') == None else self.getVars.get('bidderId')
        query_bidderId = self.conf.urllib.parse.unquote(query_bidderId)

        query_tvoid_numeric = False if self.getVars.get('strictly_numeric') == '1' else True

        if query_tvoid_numeric:
            self.invokeCategorizationsFromFiles()

            # in order to be able to connect invokedMaps to field names and indexes, create index2fieldNameConverter
            # in order to be able to connect invokedMaps to field names and indexes, create index2fieldNameConverter

            for index, fieldName in enumerate(self.fileContent['head']):
                mapFileName = 'map-' + fieldName.lower() + '.tsv'
                if self.conf.os.path.exists(self.conf.featureVectorMapPath + mapFileName):
                    self.index2fieldNameConverter[index] = fieldName

        # create filters from query data
        # create filters from query data

        filters = {}
        if len(query_buyerId) > 0:
            filters['NarocnikMaticna'] = query_buyerId.split(',')
        if len(query_bidderId) > 0:
            filters['PonudnikMaticna'] = query_bidderId.split(',')

        # first, find key indexes
        # first, find key indexes

        filerIndexses = {}
        for key, row in filters.items():
            index = self.fileContent['head'].index(key)
            filerIndexses[key] = index

        # filter data
        # filter data

        filteredData = {}
        filteredData['head'] = self.fileContent['head']
        filteredData['data'] = []

        for row in self.fileContent['data']:
            appendRow = True
            for fieldName, filter in filters.items():
                if str(row[filerIndexses[fieldName]]) not in filters[fieldName]:
                    appendRow = False
                    break

            if appendRow:
                if query_tvoid_numeric:
                    row = self.convertNumericRow2Text(row)
                filteredData['data'].append(row)

        return filteredData

    def convertNumericRow2Text(self, row):
        '''
        funtion converts numeric featurs to text-labeled fetaures

        :param dataDict:
        :return:
        '''

        for index, fieldName in self.index2fieldNameConverter.items():
            new_value = self.invokedMaps[fieldName.lower()][row[index]]
            row[index] = new_value.replace(',', ' ')

            # if row[index] not in self.invokedMaps[fieldName.lower()]:
            #     print(fieldName.lower(), row[index], index, row)
            #     print('<br />')

        return row

    def invokeCategorizationsFromFiles(self):
        '''
        function reads map files that were created when converting tender data into numerical feature vector

        :return: dictionary
        '''

        # get all files in self.conf.featureVectorMapPath directory
        # get all files in self.conf.featureVectorMapPath directory

        allFiles = [f for f in self.conf.os.listdir(self.conf.featureVectorMapPath) if self.conf.os.path.isfile(self.conf.os.path.join(self.conf.featureVectorMapPath, f))]

        # filter files to start with 'map-'
        # filter files to start with 'map-'

        mapFiles = [curFile for curFile in allFiles if curFile[:4] == 'map-']

        # import data in files into varable
        # import data in files into varable

        self.invokedMaps = {}
        for file in mapFiles:
            fullFileName = self.conf.featureVectorMapPath + file
            tmpDict = self.conf.sharedCommon.readDataFile2Dict(fullFileName, "\t")
            tmpCatName = file[4:-4]

            self.invokedMaps[tmpCatName] = {}
            for valueList in tmpDict['data']:
                self.invokedMaps[tmpCatName][str(valueList[0])] = str(valueList[1])

        return None

    def convertDict2String(self, dataDict):
        '''
        function converts dictionary into string; dictionary is of the form:
        dataDict['head'] = list of filed names
        dataDict['data'] = list of vectors

        every line in a string is made of vectors values

        :param dataDict: dictionary
        :return: string
        '''

        # convert slovenian head to english
        # convert slovenian head to english

        fvTranslations = self.conf.sharedCommon.getMJUFVEnglishTranslator()
        engHead = []
        for sloVal in dataDict['head']:
            engHead.append(fvTranslations[sloVal])

        # stringify content
        # stringify content

        #contentString = ','.join(dataDict['head']) + self.conf.os.linesep
        contentString = ','.join(engHead) + '<br />'
        # i = 0
        # print('num of selected rows: ', len(dataDict['data']))
        oldTimeStamp = 0
        for row in dataDict['data']:
            # consecutive timestamps are expected to increase
            currTimeStamp = int(row[0])
            if currTimeStamp <= oldTimeStamp:
                currTimeStamp = oldTimeStamp + 1
                row[0] = str(currTimeStamp)

            #contentString += ','.join(row) + self.conf.os.linesep
            contentString += ','.join(row) + '<br />'
            oldTimeStamp = currTimeStamp
            # i += 1
            # if i == 10:
            #     break

        return contentString

    def exportString(self, dataString):
        '''
        returning string in various formats; because of time constraints, only print is currently implemented;
        TO-DO: return string as a file through header manipulation

        :param dataString: string to be returned to the user
        :return:
        '''

        # google search
        # https://www.google.com/search?client=firefox-b-d&q=python+http.server++serve+file+over

        # export as a file:
        # https://stackoverflow.com/questions/46105356/serve-a-file-from-pythons-http-server-correct-response-with-a-file

        print(dataString)
        return None



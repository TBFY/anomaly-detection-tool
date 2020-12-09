
'''
Series of methods shared by data analysis methods
'''

class SharedAnalysisMethods:

    def __init__(self, conf = None):
        self. conf = conf

    def appendTBFYKGFieldMapValue(self, dataDict, fieldsList):
        '''
        function enriches dataDict a list of lists and extracts company names nad ids and stores them in DB

        :param dataDict:
            dataDict['head'] = [column names]
            dataDict['data'] = [list of vectors, column values]
        :param fieldsList: is a list od dictionary elemens, which look like this:
            fieldsDict['dataColumnName'] = a column name in dataDict['head']
            fieldsDict['mapFileId'] = a name to identfy mappings in tbfyKGFV/mappings/
            fieldsDict['newColumnName'] = name of a field to be appended to dataDict
        :return: enriched dataDict
        '''

        # return if empty
        # return if empty

        if len(dataDict['data']) == 0:
            return dataDict

        # init final dictionary
        # init final dictionary

        returnDataDict = {}
        returnDataDict['head'] = dataDict['head'].copy()
        returnDataDict['data'] = dataDict['data'].copy()

        # for every element in fieldsList, read map into dictionary
        # for every element in fieldsList, read map into dictionary

        for currentMapDict in fieldsList:

            mappingFileName = 'map-' + currentMapDict['mapFileId'] + '.tsv'
            fullFileName = self.conf.tenderTbfyKGFVPath + 'mappings/' + mappingFileName
            tmpDict = self.conf.sharedCommon.readDataFile2Dict(fullFileName, "\t")

            mapDict = {}
            for row in tmpDict['data']:
                mapDict[row[0]] = row[1]

            # no mappings no conversion
            # no mappings no conversion

            if len(dataDict['data']) == 0:
                return tmpDict

            # enrich dataDict with values from a map
            # enrich dataDict with values from a map

            returnDataDict['head'].append(currentMapDict['newColumnName'])
            field_index = returnDataDict['head'].index(currentMapDict['dataColumnName'])
            for i,dataRow in enumerate(returnDataDict['data']):
                tmp_key = dataRow[field_index]
                value_append = mapDict[tmp_key]
                returnDataDict['data'][i].append(value_append)

        return returnDataDict

    def appendMJUOrganizationNames2Dict(self, dataDict, fieldsDict):
        '''
        function gets a list of lists and extracts company names nad ids and stores them in DB

        :param dataList: list of lists
        :param idIndex: integer, position of company id in list
        :param nameIndex: integer, position of company name in list
        :return:
        '''

        # return if empty
        # return if empty

        if len(dataDict['data']) == 0:
            return dataDict

        # initialize companyNames dict
        # initialize companyNames dict

        companyNames = {}
        for fieldKey, fieldValue in fieldsDict.items():
            fieldKeyIndex = dataDict['head'].index(fieldKey)
            for vector in dataDict['data']:
                companyNames[vector[fieldKeyIndex]] = ''

        # find all companies in DB
        # find all companies in DB

        sql = self.conf.cDB.sql
        cur = self.conf.cDB.db.cursor()

        companyIdsString = "','".join(str(v) for v in companyNames.keys())
        queryBase = "select {}, {} from {} where company_id IN ('" + companyIdsString + "')"
        queryString = sql.SQL(queryBase).format(
            # set queried fields
            sql.Identifier('company_id'),
            sql.Identifier('company_name'),
            # set table name
            sql.Identifier('cst_companies_mju'))
        #print(queryString.as_string(cur))
        cur.execute(queryString)
        companiesDB = self.conf.sharedCommon.returnSqlDataInDictFormat(cur, 'company_id')

        # enrich dataDict with company names
        # enrich dataDict with company names

        returnDataDict = {}
        returnDataDict['head'] = dataDict['head']
        returnDataDict['data'] = []

        # enrich dict head
        for fieldKey, fieldValue in fieldsDict.items():
            returnDataDict['head'].append(fieldValue)
        # enrich dict data
        for vector in dataDict['data']:
            newVector = vector.copy()
            for fieldKey, fieldValue in fieldsDict.items():
                fieldKeyIndex = dataDict['head'].index(fieldKey)
                # find value to be appended
                tmp_cid = vector[fieldKeyIndex]
                if tmp_cid in companiesDB and 'company_name' in companiesDB[tmp_cid]:
                    value2append = companiesDB[tmp_cid]['company_name']
                else:
                    value2append = '-'

                newVector.append(value2append)

            returnDataDict['data'].append(newVector)

        return returnDataDict

    def appendAjpesOrganizationNames2Dict(self, dataDict, fieldsDict):
        '''
        function gets a list of list and appends to every vector a company name

        :param dataDict: dictionary, dataDict['data'] = list of lists
        :param fieldsDict: dict, defining field names
        :return:
        '''

        # return if empty
        # return if empty

        if len(dataDict['data']) == 0:
            return dataDict

        # initialize companyNames dict
        # initialize companyNames dict

        companyNames = {}
        for fieldKey, fieldValue in fieldsDict.items():
            fieldKeyIndex = dataDict['head'].index(fieldKey)
            for vector in dataDict['data']:
                companyNames[vector[fieldKeyIndex]] = ''

        # find all companies in DB
        # find all companies in DB

        sql = self.conf.cDB.sql
        cur = self.conf.cDB.db.cursor()

        companyIdsString = "','".join(str(v) for v in companyNames.keys())
        queryBase = "select {}, {} from {} where company_id IN ('" + companyIdsString + "')"
        queryString = sql.SQL(queryBase).format(
            # set queried fields
            sql.Identifier('company_id'),
            sql.Identifier('company_name'),
            # set table name
            sql.Identifier('cst_companies_mju'))
        #print(queryString.as_string(cur))
        cur.execute(queryString)
        companiesMJUDB = self.conf.sharedCommon.returnSqlDataInDictFormat(cur, 'company_id')

        # find still missing company names
        # find still missing company names

        missingCompanyNames = {}
        for companyId in companyNames:
            if companyId not in companiesMJUDB:
                missingCompanyNames[companyId] = ''

        # look into ajpes DB for names
        # look into ajpes DB for names

        companyNames = missingCompanyNames.copy()

        companyIdsString = "','".join(str(v) for v in companyNames.keys())
        queryBase = "select {},{} from {} where {} IN ('" + companyIdsString + "')"
        queryString = sql.SQL(queryBase).format(
            sql.Identifier('maticna'),
            sql.Identifier('popolno_ime'),
            sql.Identifier('prs_enota_rs'),
            sql.Identifier('maticna'))
        cur.execute(queryString)
        #print(queryString.as_string(cur), tuple(companyNames.keys()))
        companiesAjpesDB = self.conf.sharedCommon.returnSqlDataInDictFormat(cur, 'maticna')

        # find still missing company names
        # find still missing company names

        missingCompanyNames = {}
        for companyId in companyNames:
            if companyId not in companiesAjpesDB:
                missingCompanyNames[companyId] = ''

        # look into historical ajpes DB for names
        # look into historical ajpes DB for names

        companyNames = missingCompanyNames.copy()

        companyIdsString = "','".join(str(v) for v in companyNames.keys())
        queryBase = "select {},{} from {} where {} IN ('" + companyIdsString + "')"
        queryString = sql.SQL(queryBase).format(
            sql.Identifier('maticna'),
            sql.Identifier('popolno_ime'),
            sql.Identifier('hs_prs_enota_rs'),
            sql.Identifier('maticna'))
        cur.execute(queryString)
        #print(queryString.as_string(cur), tuple(companyNames.keys()))
        companiesAjpesHstDB = self.conf.sharedCommon.returnSqlDataInDictFormat(cur, 'maticna')

        # enrich data
        # enrich data

        returnDataDict = {}
        returnDataDict['head'] = dataDict['head']
        returnDataDict['data'] = []

        # enrich dict head
        for fieldKey, fieldValue in fieldsDict.items():
            returnDataDict['head'].append(fieldValue)
        # enrich dict data
        for vector in dataDict['data']:
            newVector = vector.copy()
            for fieldKey, fieldValue in fieldsDict.items():
                fieldKeyIndex = dataDict['head'].index(fieldKey)
                # find value to be appended
                tmp_cid = vector[fieldKeyIndex]
                if tmp_cid in companiesMJUDB and 'company_name' in companiesMJUDB[tmp_cid]:
                    value2append = companiesMJUDB[tmp_cid]['company_name']
                elif tmp_cid in companiesAjpesDB and 'popolno_ime' in companiesAjpesDB[tmp_cid]:
                    value2append = companiesAjpesDB[tmp_cid]['popolno_ime']
                elif tmp_cid in companiesAjpesHstDB and 'popolno_ime' in companiesAjpesHstDB[tmp_cid]:
                    value2append = companiesAjpesHstDB[tmp_cid]['popolno_ime']
                else:
                    value2append = '-'

                newVector.append(value2append)

            returnDataDict['data'].append(newVector)

        return returnDataDict


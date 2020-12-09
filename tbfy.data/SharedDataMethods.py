
'''
Series of methods shared by data processing methods
'''

class SharedDataMethods:

    def __init__(self, conf=None):

        self.conf = conf

    def storeMJUOrganizationNames2Db(self, dataList, idIndex, nameIndex):
        '''
        function gets a list of lists and extracts company names nad ids and stores them in DB

        :param dataList: list of lists
        :param idIndex: integer, position of company id in list
        :param nameIndex: integer, position of company name in list
        :return:
        '''

        if len(dataList) == 0:
            return None

        # get names
        # get names

        companyNames = {}
        for row in dataList:
            companyNames[row[idIndex]] = row[nameIndex]

        # find names that are not in DB yet
        # find names that are not in DB yet

        sql = self.conf.cDB.sql
        cur = self.conf.cDB.db.cursor()
        db = self.conf.cDB.db

        dictKeys = "','".join(str(v) for v in companyNames.keys())
        queryBase = "select {} from {} where company_id IN ('" + dictKeys + "')"
        queryString = sql.SQL(queryBase).format(
            # set queried fields
            sql.Identifier('company_id'),
            # set table name
            sql.Identifier('cst_companies_mju'))
        #print(queryString.as_string(cur))
        cur.execute(queryString)
        companiesInDB = self.conf.sharedCommon.returnSqlDataInDictFormat(cur, 'company_id')

        # save names in DB
        # save names in DB

        doCommit = False
        for company_id, company_name in companyNames.items():

            # skip existing records
            # skip existing records

            if company_id in companiesInDB:
                continue

            # add non existing records
            # add non existing records

            queryBase = "INSERT INTO cst_companies_mju (company_id, company_name) VALUES (%s, %s)"
            queryString = sql.SQL(queryBase).format()
            #print(queryString.as_string(cur))
            row_values = (company_id, company_name)
            cur.execute(queryString, row_values)
            doCommit = True

        # commit changes
        # commit changes

        if doCommit:
            db.commit()

        return None

    def storeMJURaw2SQLDB(self, dataDict, tableName, tableUniqueField):
        '''
        function takes in dataDict and inserts the data into sql DB table with name tableName

        :param dataList: dictionary
        :param idIndex: name of the table to insert the data
        :return: none
        '''

        # set db vars
        # set db vars

        sql = self.conf.cDB.sql
        cur = self.conf.cDB.db.cursor()
        db = self.conf.cDB.db

        # get query variables
        # get query variables

        fieldNamesString = ','.join(dataDict['head']).lower()
        valuesList = []
        for val in dataDict['head']:
            valuesList.append('%s')
        valuesString = ','.join(valuesList)

        # set query statement
        # set query statement

        insertQueryStatement = 'INSERT INTO TABLE-NAME-REPLACE (FIELDS-REPLACE) VALUES (VALUES-REPLACE)'
        insertQueryStatement = insertQueryStatement.replace('TABLE-NAME-REPLACE', tableName)
        insertQueryStatement = insertQueryStatement.replace('FIELDS-REPLACE', fieldNamesString)
        insertQueryStatement = insertQueryStatement.replace('VALUES-REPLACE', valuesString)

        formatRules = {
            'ocenjenavrednost': 'float',
            'koncnavrednost': 'float',
            'datumposiljanjaobvestila': 'timestamp',
            'datumobjaveobvestila': 'timestamp',
            'prejsnje_objave_pjn_datum': 'timestamp',
            'prejsnje_objave_uleu_datum': 'timestamp',
            'prejsnje_objave_rokzasprejemanjeponudnikovihvprasanj': 'timestamp',
            'prejsnje_objave_rokzaprejemponudb': 'timestamp',
            'prejsnje_objave_odpiranjeponudbdatum': 'timestamp',
            'prejsnje_objave_sys_spremembaizracunanihdatum': 'timestamp',
            'sys_spremembaizracunanihdatum': 'timestamp',
            'datumoddajesklopa': 'date',
            'stprejetihponudb': 'int',
            'stprejetiheponudb': 'int',
            'letoobdelave': 'int',
            'idizpobrazca': 'int',
            'kategorijanarocnika': 'int',
            'idizppriloge': 'int',
            'id_obrazecsubjekt': 'int',
            'zaporedna': 'int'
        }

        keysList = [x.lower() for x in dataDict['head']]
        tableUniqueField_n = keysList.index(tableUniqueField)

        for row in dataDict['data']:
            # avoid duplication
            # avoid duplication

            queryBase = "select count(*) from " + tableName + " where " + tableUniqueField.lower() + " = '" + row[tableUniqueField_n] + "'"
            queryString = sql.SQL(queryBase)
            cur.execute(queryString)
            result = cur.fetchone()
            if int(result[0]) > 0:
                continue

            # all's good, continue
            # all's good, continue

            tmp_row = row.copy()
            tmp_row = self.formatRowBeforeSQLInjection(keysList, tmp_row, formatRules)
            row_values = tuple(tmp_row)
            queryString = sql.SQL(insertQueryStatement).format()
            cur.execute(queryString, row_values)
            db.commit()

        return None

    def formatRowBeforeSQLInjection(self, headList, valuesList, rulesDict):
        '''
        function takes in valuesList and updates values according rulesDict

        :param headList: filed names, needed to identify position of dields in valuesList
        :param valuesList: list of values to be formatted
        :param rulesDict: rules for foramtting
        :return: formatted values list
        '''

        for fieldName,fieldFormat in rulesDict.items():

            # filedName must be in headList
            # filedName must be in headList

            if fieldName not in headList:
                continue

            # all good - format
            # all good - format

            tmp_n = headList.index(fieldName)
            tmp_value = valuesList[tmp_n]

            if fieldFormat == 'int':
                if tmp_value == '':
                    tmp_value = 0
                valuesList[tmp_n] = int(tmp_value)
            if fieldFormat == 'float':
                tmp_value = tmp_value.replace(',', '.')
                if tmp_value == '':
                    tmp_value = 0
                valuesList[tmp_n] = float(tmp_value)
            if fieldFormat == 'timestamp':
                if tmp_value == '':
                    tmp_value = None
                valuesList[tmp_n] = tmp_value
            if fieldFormat == 'date':
                if tmp_value == '':
                    tmp_value = None
                valuesList[tmp_n] = tmp_value

        return valuesList




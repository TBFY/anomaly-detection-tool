
'''
Series of methods shared by data processing, data analysis and data presentation processes
'''

class SharedCommonMethods:

    def __init__(self):
        return None

    def readDataFile2Dict(self, filePath, splitChar = ',', limitRowsNum = -1):
        '''
        Function reads transaction file located at "filePath" into a dictionary. File is expected to have a format:
        - first line contain column names
        - all other lines contain values
        Returend dictionary is of from:
        - dict[head] = list of column names
        - dict[data] = list of lists of dava

        :param filePath: location of file to read
        :param splitChar: character splitting
        :param limitRowsNum: number of rows  returned in dict[data]
        :return: dictionary
        '''

        import csv

        # init storage dict
        # init storage dict

        tenderDataDict = {}
        tenderDataDict['head'] = []
        tenderDataDict['data'] = []

        # read file contents
        # read file contents

        #with codecs.open('class1.csv', encoding='iso-8859-1') as handle:
        #    reader = csv.reader(handle)

        with open(filePath, newline='', encoding="utf-8-sig") as csvfile:
            tmpReader = csv.reader(csvfile, delimiter=splitChar, quotechar='"')
            line_num = 0
            for row in tmpReader:
                line_num += 1
                if line_num == 1:
                    tenderDataDict['head'] = row
                else:
                    tenderDataDict['data'].append(row)

                if limitRowsNum == line_num:
                    break

        return tenderDataDict

    def readAndOrganizeTransactions2Dict(self, filePath, splitChar = ',', limitRowsNum = -1):
        '''
        Function is very similar to readDataFile2Dict - however, it returns data organized for the needs of specific analysis.
        The expected source file data is: "public.company.id any.company.id any.company.class trans1 trans2 ... transN"

        :param filePath: string, location of source file
        :param splitChar: string, character that splits data in source file
        :param limitRowsNum: int, limits the numer of rows for test purposes
        :return: dictionary, dict[any.company.class][public.company.id-any.company.id] = [transaction list]
        '''

        import csv

        # init storage dict
        # init storage dict

        transactionsDataDict = {}
        transactionsDataDict['head'] = []
        transactionsDataDict['data'] = {}

        # read file contents
        # read file contents

        with open(filePath, newline='', encoding="utf-8-sig") as csvfile:
            tmpReader = csv.reader(csvfile, delimiter=splitChar, quotechar='"')
            line_num = 0
            for row in tmpReader:
                line_num += 1
                if line_num == 1:
                    transactionsDataDict['head'] = row
                    continue

                # reading dta into dict
                # reading dta into dict

                maticna_public = row[0]
                maticna_private = row[1]
                company_classifier = row[2]
                tmp_sums = row[3:]

                if company_classifier not in transactionsDataDict['data'].keys():
                    transactionsDataDict['data'][company_classifier] = {}

                tmp_k = maticna_public + "-" + maticna_private
                transactionsDataDict['data'][company_classifier][tmp_k] = [float(i) for i in tmp_sums]

                if limitRowsNum == line_num:
                    break

        return transactionsDataDict

    def sendDict2Output(self, dataDict, fileName):
        '''
        function takes in a dictionary and saves dictionary data into file

        :param dataDict: dictionary data
        :param fileName: file name where dictionary data are stored
        :return: None
        '''

        fileObject = open(fileName, 'w+',  encoding='utf8')
        separator = "\t"

        # print legend (1st row)
        # print legend (1st row)

        rowString = separator.join(dataDict['head'])
        self._send2Output(rowString, fileObject)

        # print data
        # print data

        i = 0
        for valueList in dataDict['data']:
            #print("tukaj: ", valueList)
            rowString = separator.join(valueList)
            self._send2Output(rowString, fileObject)

        return None

    def _send2Output(self, rowString, fileObject = None):
        '''
        part of sendDict2Output :: functiopn takes a string and sends it to output
        :param rowString: string
        :param fileObject: file object
        :return: None
        '''
        if(fileObject != None):
            fileObject.write(rowString + "\n")
        else:
            print(rowString)

        return None

    def returnSqlDataInDictFormat(self, cur, keyField = ''):
        '''
        function gets a psycopg2 list of queried rows and returns it in list (keyField == '') or dict (keyField != '') format

        :param cur: list of queried rows
        :param keyField: key for a dictionary list; !must be a column in cur rows
        :return:
        '''

        returnDict = 0 if len(keyField) == 0 else 1
        if(returnDict): returnObject = {}
        else: returnObject = []

        for row in cur.fetchall():
            tmpDict = {}
            for (attr, val) in zip((d[0] for d in cur.description), row):
                tmpDict[attr] = val

            # adding DB row on return object
            if(returnDict): returnObject[tmpDict[keyField]] = tmpDict
            else: returnObject.append(tmpDict)

        return returnObject

    def fileGetContents(self, fullFilePath):
        '''
        funtion returns contents of a file located at fullFilePath

        :param fullFilePath: string
        :return: string
        '''

        with open(fullFilePath) as f:
            return f.read()

    def getMJUFVEnglishTranslator(self):
        '''
        funtion returns dictionary converting slovenian names of slovenian ministry data to english

        :return: dictionary
        '''

        translationDict = {}
        translationDict['DatumObjaveObvestila'] = 'Date_of_notice'
        translationDict['NarocnikMaticna'] = 'Buyer_ID'
        translationDict['Narocnik_OBCINA'] = 'Buyer_muncipality'
        translationDict['Narocnik_Oblika'] = 'Buyer_legal_organizational_form'
        translationDict['Narocnik_Glavna_Dejavnost_SKD'] = 'Buyer_main_activity'
        translationDict['Narocnik_Velik_RS'] = 'Buyer_size_SLO'
        translationDict['Narocnik_Velik_EU'] = 'Buyer_size_EU'
        translationDict['Narocnik_Regija'] = 'Buyer_region'
        translationDict['Narocnik_Dejavnost'] = 'Buyer_activity'
        translationDict['VrstaNarocila'] = 'Procurement_category'
        translationDict['VrstaPostopka'] = 'Procedure_type'
        translationDict['VrstaPostopka_EU'] = 'EU_procedure_type'
        translationDict['Merila'] = 'Procedure_type_EU_criteria'
        translationDict['OkvirniSporazum'] = 'Framework_agreement'
        translationDict['SkupnoNarocanje'] = 'Joint_procurement'
        translationDict['EUsredstva'] = 'EU_funds'
        translationDict['ObjavaVEU'] = 'Published_in_EU'
        translationDict['StPrejetihPonudb'] = 'Number_of_bids'
        translationDict['SkupnaPonudba'] = 'Joint_tenders'
        translationDict['OcenjenaVrednost'] = 'Estimated_value'
        translationDict['OcenjenaVrednostValuta'] = 'Estimated_value_currency'
        translationDict['KoncnaVrednost'] = 'Final_value'
        translationDict['KoncnaVrednostValuta'] = 'Final_value_currency'
        translationDict['OddanoPodizvajalcem'] = 'Subcontracted'
        translationDict['CPV_glavni_2mesti'] = 'CPV_level2'
        translationDict['Podrocje'] = 'Area'
        translationDict['VrstaPostopkaIzracunan'] = 'Type_of_procedure_calculated'
        translationDict['PonudnikMaticna'] = 'Bidder_ID'
        translationDict['PonudnikPostnaStevilka'] = 'Bidder_post_code'
        translationDict['Ponudnik_OBCINA'] = 'Bidder_muncipality'
        translationDict['Ponudnik_Velik_EU'] = 'Bidder_size_EU'
        translationDict['Ponudnik_Velik_RS'] = 'Bidder_size_SLO'
        translationDict['OcenjenaVrednostSorazmerno'] = 'Proportional_estimated_value'
        translationDict['KoncnaVrednostSorazmerno'] = 'Proportional_final_value'

        return translationDict

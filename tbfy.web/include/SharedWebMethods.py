
'''
Set of shared methods to be used across website
'''

class SharedWebMethods:

    def __init__(self):
        cDB = None
        sharedCommon = None
        return

    def getErrorView(self, confObj):
        '''
        function returns error message

        :return: string, html format
        '''

        content = confObj.Template(filename='templates/error.tpl')
        return content.render()

    def tuple2dict(self, tup):
        dict = {}
        for a, b in tup:
            dict[a] = b
        return dict

    def getCPVDescriptions(self, confObj, cpvDict):
        '''
        function returns a list of cpv codes with corresponding description

        :param cpvDigits: num of digits to be considered taken into account when selecting cpv codes
        :return: list
        '''

        # find descriptions
        # find descriptions

        sql = confObj.cDB.sql
        cur = confObj.cDB.db.cursor()

        queryBase = "select {},{} from {} where code LIKE '%000000%'"
        queryString = sql.SQL(queryBase).format(
            sql.Identifier('code'),
            sql.Identifier('en'),
            sql.Identifier('mju_cpv'))
        cur.execute(queryString)
        #print(queryString.as_string(cur))
        cpvCodes = confObj.sharedCommon.returnSqlDataInDictFormat(cur, 'code')

        # assign description to dict
        # assign description to dict

        for key,list in cpvCodes.items():
            tmp_code = list['code'][:2]
            if tmp_code in cpvDict:
                cpvDict[tmp_code] = list['en']
            else:
                cpvDict[tmp_code] = 'description missing in DB'

        return cpvDict
    
    def getSKDDescriptions(self, confObj, skdDict):
        '''
        function returns a list of skd codes (slovenian classification) with corresponding description

        :param cpvDigits: num of digits to be considered takein into account when selecting cpv codes
        :return: list
        '''

        # find descriptions
        # find descriptions

        sql = confObj.cDB.sql
        cur = confObj.cDB.db.cursor()

        queryBase = "select {},{} from {} where level = 2 order by code"
        queryString = sql.SQL(queryBase).format(
            sql.Identifier('code'),
            sql.Identifier('descriptor_en'),
            sql.Identifier('mju_skd'))
        #print(queryString.as_string(cur))
        cur.execute(queryString)
        cpvCodes = confObj.sharedCommon.returnSqlDataInDictFormat(cur, 'code')

        # assign description to dict
        # assign description to dict

        returnSkdDict = {}
        for key,list in cpvCodes.items():
            tmp_code = list['code'][1:3]
            if tmp_code not in skdDict:
                continue
            #print("**** ", list['code'], tmp_code, list['descriptor_en'],  " ****<br />")
            if tmp_code in skdDict:
                returnSkdDict[tmp_code] = list['descriptor_en']
            else:
                returnSkdDict[tmp_code] = 'description missing in DB'

        return returnSkdDict

    def getAllValueMaps(self, confObj, datasetType = 'mju'):
        '''
        function returns all value-description maps, created during conversion into feature vectors

        :param confObj: config object
        :param datasetType: dataset type, string, valid values = 'mju' and 'tbfyKG'
        :return: dictionary
        '''

        if datasetType == 'mju':
            path2Dir = confObj.featureVectorMapPath
        else:
            return {}

        # get all files in path2Dir directory
        # get all files in path2Dir directory

        allFiles = [f for f in confObj.os.listdir(path2Dir) if confObj.os.path.isfile(confObj.os.path.join(path2Dir, f))]

        # filter files to start with 'map-'
        # filter files to start with 'map-'

        mapFiles = [curFile for curFile in allFiles if curFile[:4] == 'map-']

        # import data in files into varable
        # import data in files into varable

        codeDict = {}
        for file in mapFiles:
            fullFileName = path2Dir + file
            tmpDict = confObj.sharedCommon.readDataFile2Dict(fullFileName, "\t")
            tmpCatName = file[4:-4]

            codeDict[tmpCatName] = {}
            for valueList in tmpDict['data']:
                codeDict[tmpCatName][int(valueList[0])] = str(valueList[1])

        return codeDict


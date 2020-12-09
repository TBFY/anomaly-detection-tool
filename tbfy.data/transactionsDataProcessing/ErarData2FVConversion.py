
'''
Module takes data in raw format from Erar and converts it into feature vectors csv
'''

class ErarData2FVConversion:

    def __init__(self, conf, shared):

        self.conf = conf
        self.shared = shared

        # data storage variables
        # data storage variables

        self.rawData = {}
        self.FVdata = {}
        self.FVdata['head'] = ['datum_transakcije', 'znesek_transakcije', 'sifra_pu', 'maticna_stevilka']
        self.FVdata['data'] = []

        self.erarFVDailyPath = self.conf.erarFeatureVectorsDataPath + 'daily/'

    def convertRawData2FV(self):
        '''
        function finds all files that ware not yet converted into FV format and executes conversion

        :return: None
        '''

        # find all raw data files, that don't have FV equivalent
        # find all raw data files, that don't have FV equivalent

        listOfFiles2Process = self.getListOfNotYetProcessedFiles()

        # if list empty, abort
        # if list empty, abort

        if len(listOfFiles2Process) > 0:
            for fileName in listOfFiles2Process:
                self.convertErrarDataFile2FV(fileName)

        # join daily files into one big feature vector file
        # join daily files into one big feature vector file

        self.joinDailyFiles2OneFVFile(listOfFiles2Process)

        return None

    def getListOfNotYetProcessedFiles(self):
        '''
        function identifies files in data > rawData > spendingRawData > erarRawData that hasn't have a FV equivalent in
        data > erarFeatureVectors

        :return: list of files to be processed
        '''

        rawDataFiels = [f for f in self.conf.os.listdir(self.conf.erarDataRawPath) if self.conf.os.path.isfile(self.conf.os.path.join(self.conf.erarDataRawPath, f)) and f[len(f) - 3:] == 'csv']

        missingFilesList = []
        for fileName in rawDataFiels:
            fullFilePath = self.erarFVDailyPath + 'fv-' + fileName
            if not self.conf.os.path.isfile(fullFilePath):
                missingFilesList.append(fileName)

        return missingFilesList

    def convertErrarDataFile2FV(self, fileName):
        '''
        function converts raw erar data file into a feture vector data file ready for later analysis

        :param fileName: string, name of file to be processed
        :return: none
        '''

        # check if source file exists
        # check if source file exists

        fullFileName = self.conf.erarDataRawPath + fileName
        if not self.conf.os.path.isfile(fullFileName):
            return None

        # reset storage var and read data file
        # reset storage var and read data file

        self.rawData = {}
        self.rawData = self.conf.sharedCommon.readDataFile2Dict(fullFileName, ';')

        # transpose data matrix
        # transpose data matrix

        transposedData = list(map(list, zip(*self.rawData['data'])))

        # retain only fields listed in self.fieldsFV
        # retain only fields listed in self.fieldsFV

        tmp_fvData = []
        for fieldName in self.FVdata['head']:
            index = self.rawData['head'].index(fieldName)
            tmp_fvData.append(transposedData[index])

        # reset and reverse transpose data matrix
        # reset and reverse transpose data matrix

        self.FVdata['data'] = []
        self.FVdata['data'] = list(map(list, zip(*tmp_fvData)))

        # ignore record is subject missing
        # ignore record is subject missing

        updatedDataList = []
        for row in self.FVdata['data']:
            if row[2] == '':
                continue
            if row[3] == '':
                continue

            updatedDataList.append(row)

        self.FVdata['data'] = updatedDataList

        # save data 2 file
        # save data 2 file

        fullNewFilePath = self.erarFVDailyPath + 'fv-' + fileName
        self.conf.sharedCommon.sendDict2Output(self.FVdata, fullNewFilePath)

        return None

    def joinDailyFiles2OneFVFile(self, listOfFiles2Process = []):
        '''
        function joins daily files into one single file

        :return: None
        '''

        # if destination file does not exists, get all daily files to initiate destination file
        # if destination file does not exists, get all daily files to initiate destination file

        fullErarFVFile = self.conf.erarFeatureVectorsDataPath + 'fv-trans.csv'
        createFullFile = False
        if not self.conf.os.path.exists(fullErarFVFile):
            createFullFile = True
            listOfFiles2Process = [f for f in self.conf.os.listdir(self.conf.erarDataRawPath) if self.conf.os.path.isfile(self.conf.os.path.join(self.conf.erarDataRawPath, f)) and f[len(f) - 3:] == 'csv']

        # retain order
        # retain order

        listOfFiles2Process.sort()

        # if full file does not exist - create full file by copying first daily file
        # if full file does not exist - create full file by copying first daily file

        if createFullFile:
            fileName = listOfFiles2Process.pop(0)
            import shutil
            shutil.copyfile(self.erarFVDailyPath + 'fv-' + fileName, fullErarFVFile)

        # concatenate files into one big file
        # concatenate files into one big file

        with open(fullErarFVFile, 'a') as outfile:
            for fname in listOfFiles2Process:
                with open(self.erarFVDailyPath + 'fv-' + fname) as infile:
                    is_first_line = True
                    for line in infile:
                        if is_first_line:
                            is_first_line = False
                            continue
                        outfile.write(line)

        return None


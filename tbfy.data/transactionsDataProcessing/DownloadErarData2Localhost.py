
'''
Module connects to Erar website and retreives monthly data update
'''

class DownloadErarData2Localhost:

    def __init__(self, conf, shared):

        self.conf = conf
        self.shared = shared

        # manipulated files
        # manipulated files

        self.transactionsUrl = 'https://erar.si/cdn/podatki/'
        self.transactionsFileName = 'transDATE.csv'
        self.dateString = ''

    def downloadLastAvailableErarDataDump(self):
        '''
        Function downloads last available Erar transactions data dump - of not yet in local repository

        :return: void
        '''

        # script:
        # 1) defines filename that needs to be downloaded to localhost
        # 2) downloads the fike

        self.getFilenameForDownload()
        self.downloadFile()

    def getFilenameForDownload(self):
        '''
        functions defines filename that needs to be downloaded

        :param fileName: string
        :return: string
        '''

        tmp_dateObj = self.conf.datetime.datetime.now()
        intYear = int(tmp_dateObj.strftime("%Y"))
        intMonth = int(tmp_dateObj.strftime("%m"))

        numIterations = 0
        intYear_prev = 0
        intMonth_prev = 0
        while not self.fileExistsInRepository(intMonth, intYear):

            intYear_prev = intYear
            intMonth_prev = intMonth

            if intMonth == 1:
                intMonth = 12
                intYear -= 1
            else:
                intMonth -= 1

            # safety check
            # safety check

            numIterations += 1
            if numIterations == 300:
                print('iterations exceeded')
                break

        # set filenameDate variable
        # set filenameDate variable

        if intMonth_prev < 10:
            self.dateString = str(intYear_prev) + '0' + str(intMonth_prev)
        else:
            self.dateString = str(intYear_prev) + str(intMonth_prev)

        return None

    def fileExistsInRepository(self, intMonth, intYear):
        '''
        function gets month anf year and checks whether file exists in reposiroty on localhost

        :param intMonth: integer
        :param intYear: integer
        :return: boolean
        '''

        if intMonth < 10:
            strDate = str(intYear) + '0' + str(intMonth)
        else:
            strDate = str(intYear) + str(intMonth)

        fileName = self.transactionsFileName.replace('DATE', strDate)
        if self.conf.os.path.exists(self.conf.erarDataRawPath + fileName):
            return True
        else:
            return False

    def downloadFile(self):
        '''
        function downloads a file from Erar

        :return: void
        '''

        baseFileName = self.transactionsFileName.replace('DATE', self.dateString)

        urlSourceFileName = self.transactionsUrl
        urlSourceFileName += baseFileName + '.gz'

        destinationFileNameGZ = self.conf.erarDataRawPath
        destinationFileNameGZ += baseFileName + '.gz'

        # download urlSourceFileName to destinationFileName
        # download urlSourceFileName to destinationFileName

        import urllib.request
        import shutil
        import requests

        # check if file exists
        # check if file exists

        r = requests.head(urlSourceFileName)
        if r.status_code != requests.codes.ok:
            return None

        with urllib.request.urlopen(urlSourceFileName) as response, open(destinationFileNameGZ, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)

        # unzip file
        # unzip file

        if self.conf.os.path.exists(destinationFileNameGZ):
            import gzip
            with gzip.open(destinationFileNameGZ, 'rb') as f_in:
                destinationFileName = self.conf.erarDataRawPath + baseFileName
                with open(destinationFileName, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)

        return None

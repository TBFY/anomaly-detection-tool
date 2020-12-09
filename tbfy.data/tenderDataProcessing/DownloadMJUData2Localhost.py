
'''
Module connects to MJU- server and retreived daily data update
'''

class DownloadMJUData2Localhost:

    def __init__(self, conf, shared):

        self.conf = conf
        self.shared = shared

        self.ftpConnection = None

        # manipulated files
        # manipulated files

        self.tendersFileName = 'PostopkiJN_DATE.csv'
        self.awardsFileName = 'PostopkiJNIzvajalci_DATE.csv'

        # set date string
        # set date string

        tmp_dateObj = self.conf.datetime.datetime.now() - self.conf.datetime.timedelta(days=1)
        self.dateString = tmp_dateObj.strftime("%Y%m%d")

    def connect2MJU(self):
        '''
        Function establish a connection to a MJU server

        :return: void
        '''

        from ftplib import FTP

        self.ftpConnection = FTP(self.conf.MJUhidden.ftpHost)
        self.ftpConnection.login(user=self.conf.MJUhidden.ftpUser, passwd=self.conf.MJUhidden.ftpPass)

        return None

    def downloadDailyUpdate(self):
        '''
        Function downloads daily update of MJU tender DB

        :return: void
        '''

        if self.ftpConnection == None:
            return None

        # select correct directory
        # select correct directory

        now = self.conf.datetime.datetime.now()
        self.ftpConnection.cwd('/' + self.conf.MJUhidden.ftpWorkingDir + '/' + str(now.year) + '/')

        # set target file names
        # set target file names

        tendersFileName = self.tendersFileName.replace('DATE', self.dateString)
        awardsFileName = self.awardsFileName.replace('DATE', self.dateString)

        # download file to localhost
        # download file to localhost

        tendersDestinationFileNameFull = self.conf.os.path.join(self.conf.tenderDataRawPath, tendersFileName)
        localFile = open(tendersDestinationFileNameFull, 'wb')
        self.ftpConnection.retrbinary('RETR ' + tendersFileName, localFile.write, 1024)
        localFile.close()

        awardsDestinationFileNameFull = self.conf.os.path.join(self.conf.tenderDataRawPath, awardsFileName)
        localFile = open(awardsDestinationFileNameFull, 'wb')
        self.ftpConnection.retrbinary('RETR ' + awardsFileName, localFile.write, 1024)
        localFile.close()

        # return back to initial directory
        # return back to initial directory

        self.ftpConnection.cwd(self.conf.MJUhidden.ftpReturnDir)

        return None

    def disconnect(self):
        '''
        Function disconnects from ftp server.

        :return: void
        '''

        if self.ftpConnection != None:
            self.ftpConnection.quit()

        return None
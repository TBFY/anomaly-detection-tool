
'''
Module takes erar feature vector data and converts it into transaction time series between two entities
'''

class ErarFV2TransTimeSeries:

    def __init__(self, conf, shared):

        self.conf = conf
        self.shared = shared

        # data storage variables
        # data storage variables

        self.rawData = {}
        self.rawDataLimit = -1

        self.timeSeriesDataDays = {}
        self.timeSeriesDataWeeks = {}
        self.timeSeriesDataMonths = {}

        # currently working only with monthly transactions series
        # currently working only with monthly transactions series

        self.enableConversionDaily = False
        # TO-DO: weekly conversion are not implemented
        self.enableConversionWeekly = False
        self.enableConversionMonthly = True

        # file source and destination
        # file source and destination

        self.featureVectorFile = self.conf.erarFeatureVectorsDataPath + 'fv-trans.csv'
        self.timeSeriesFile = self.conf.erarFeatureVectorsDataPath + 'ts-trans-LIMIT-FRQSAMPLE.csv'

        # working vars // init dates to 1.1.1900
        # working vars // init dates to 1.1.1900
        
        self.mostRecentTransDateObj  = self.conf.datetime.datetime.strptime('1900-01-01', "%Y-%m-%d").date()
        self.leastRecentTransDateObj = self.conf.datetime.datetime.strptime('1900-01-01', "%Y-%m-%d").date()

        # weekend days are omitted: 0 => monday, ... 6 => sunday
        # weekend days are omitted: 0 => monday, ... 6 => sunday

        self.weekendDays = [5,6]

        # date to consecutive day converters
        # date to consecutive day converters

        self.date2DayConverter = {}
        self.date2WeekConverter = {}
        self.date2MonthConverter = {}

        # data erichment variables
        # data erichment variables

        self.privateCompanyDict = {}

    def convertFV2TimeSeries(self):
        '''
        function converts FV format into time series format

        :return: None
        '''

        # first, read transaction feature vector file
        # first, read transaction feature vector file

        self.rawData = self.conf.sharedCommon.readDataFile2Dict(self.featureVectorFile, "\t", self.rawDataLimit)

        # next, create converter for later conversions
        # next, create converter for later conversions

        self.generateDate2TimeConverter()

        # convert from FV to TS format
        # convert from FV to TS format

        self.generateTimeSeriesFormat()

        # get additional data to enrich original feature vector
        # get additional data to enrich original feature vector

        self.getPrivateCompanyClassificatorDictSI()

        # save data to file
        # save data to file

        self.saveTimeSeriesFromat2File()

        return None

    def generateDate2TimeConverter(self):
        '''
        the idea of converter is to assign each date a consecutive integer, for example: 2011-04-01 => 1, 2011-04-02 => 2, ... 2011-05-02 => 32,...

        :return: None
        '''

        # find index for date field
        # find index for date field

        dateIndex = self.rawData['head'].index('datum_transakcije')

        # first, get most recent and least recent date
        # first, get most recent and least recent date

        leastRecentTransaction = list(self.rawData['data'])[0]
        # self.leastRecentTransDateObj = leastRecentTransaction[dateIndex]
        self.leastRecentTransDateObj = self.conf.datetime.datetime.strptime(leastRecentTransaction[dateIndex], "%Y-%m-%d").date()

        lastTransactionIndex = len(self.rawData['data']) - 1
        mostRecentTransaction = list(self.rawData['data'])[lastTransactionIndex]
        #self.mostRecentTransDateObj = mostRecentTransaction[dateIndex]
        self.mostRecentTransDateObj = self.conf.datetime.datetime.strptime(mostRecentTransaction[dateIndex], "%Y-%m-%d").date()

        # get various variables
        # get various variables

        self.numOfDaysBtwn2MostDistTrans = (self.mostRecentTransDateObj - self.leastRecentTransDateObj).days
        self.numOfWeekendDays = self.getNumberOfWeekendsBetweenDates(self.leastRecentTransDateObj, self.mostRecentTransDateObj)

        # get year range
        # get year range

        year_min = int(leastRecentTransaction[0][:4])
        year_max = int(mostRecentTransaction[0][:4])

        # all variables set - create date2day converter
        # all variables set - create date2day converter

        curMonth = -1
        curNumOfWeekendDays = 0
        for i in range(0, self.numOfDaysBtwn2MostDistTrans + 1):

            tmp_date = self.leastRecentTransDateObj + self.conf.datetime.timedelta(days=i)
            tmp_key = tmp_date.strftime("%Y-%m-%d")
            weekDay = tmp_date.weekday()
            weeKey = str(self.leastRecentTransDateObj)

            # updating date2day converter
            # updating date2day converter

            if(weekDay not in self.weekendDays):
                self.date2DayConverter[tmp_key] = i - curNumOfWeekendDays
            else:
                curNumOfWeekendDays = curNumOfWeekendDays + 1

            # updating date2week converter
            # updating date2week converter

            if(weekDay == 0):
                weeKey = tmp_key
            if(weekDay == 6):
                weeKey = weeKey + "=>" + tmp_key
                self.date2WeekConverter[weeKey] = tmp_date.strftime("%W")

            # updating date2month converter
            # updating date2month converter

            if(curMonth != tmp_date.month):
                curYear = tmp_date.year
                curMonth = 12 * (curYear - year_min) + tmp_date.month
                monthKey = tmp_date.strftime("%Y-%m")
                self.date2MonthConverter[monthKey] = curMonth

        #print(self.date2MonthConverter)
        return None

    def getNumberOfWeekendsBetweenDates(self, startDate, endDate):
        '''
        function returns number of weekend days between two dates (startDate, endDate)

        :param startDate: date string
        :param endDate: date string
        :return: integer
        '''

        numOfDaysBetweenDates = (endDate - startDate).days + 1
        numOfWeeks = int(numOfDaysBetweenDates / 7)
        numOfWeekendDays = numOfWeeks * len(self.weekendDays)

        difference = numOfDaysBetweenDates - numOfWeeks * 7
        dayTypeStart = startDate.weekday() + 1
        i = 0
        while (i < difference):
            if(dayTypeStart in self.weekendDays):
                numOfWeekendDays = numOfWeekendDays + 1
            i = i + 1
            dayTypeStart = dayTypeStart + 1

        return numOfWeekendDays

    def generateTimeSeriesFormat(self):
        '''
        function converts feature vector format to transactions time series between two companies format

        :return: None
        '''

        # find indexes for later data identification
        # find indexes for later data identification

        maticna_buyer_n  = self.rawData['head'].index('sifra_pu')
        maticna_bidder_n = self.rawData['head'].index('maticna_stevilka')
        trans_date_n     = self.rawData['head'].index('datum_transakcije')
        trans_amount_n   = self.rawData['head'].index('znesek_transakcije')

        # transform data
        # transform data

        for row in self.rawData['data']:

            # get companies ids
            # get companies ids

            maticna_buyer =  row[maticna_buyer_n]
            maticna_bidder = row[maticna_bidder_n]

            # add data 2 daily dataset
            # add data 2 daily dataset

            if self.enableConversionDaily:

                # init variable
                # init variable

                if maticna_buyer not in self.timeSeriesDataDays.keys():
                    self.timeSeriesDataDays[maticna_buyer] = {}
                if maticna_bidder not in self.timeSeriesDataDays[maticna_buyer].keys():
                    self.timeSeriesDataDays[maticna_buyer][maticna_bidder] = [float(0.0)] * (self.numOfDaysBtwn2MostDistTrans + 1 - self.numOfWeekendDays)

                # add transaction
                # add transaction

                tmp_date = row[trans_date_n]
                if tmp_date not in self.date2DayConverter:
                    # for some reason, sometimes there are some not expected dates, like transaction on weekend day
                    continue
                tmp_day_n = self.date2DayConverter[tmp_date]

                self.timeSeriesDataDays[maticna_buyer][maticna_bidder][tmp_day_n] = self.timeSeriesDataDays[maticna_buyer][maticna_bidder][tmp_day_n] + float(row[trans_amount_n])

            # add data 2 weekly dataset
            # add data 2 weekly dataset

            if self.enableConversionWeekly:

                # init variable
                # init variable

                if maticna_buyer not in self.timeSeriesDataWeeks.keys():
                    self.timeSeriesDataWeeks[maticna_buyer] = {}
                if maticna_bidder not in self.timeSeriesDataWeeks[maticna_buyer].keys():
                    self.timeSeriesDataWeeks[maticna_buyer][maticna_bidder] = [float(0.0)] * (len(self.date2WeekConverter))

                # add transaction
                # add transaction
                '''
                tmp_date = row[trans_date_n]
                if tmp_date not in self.date2DayConverter:
                    # for some reason, sometimes there are some not expected dates, like transaction on weekend day
                    continue
                tmp_day_n = self.date2DayConverter[tmp_date]
                '''

                # TO-DO :: not imeplemented due no need => be careful as week 05 appears in every year => need to distiguish week number through years!
                # TO-DO :: not imeplemented due no need => be careful as week 05 appears in every year => need to distiguish week number through years!
                # In fact, one needs to determine correct week_index and script is implementd

                week_index = 0
                self.timeSeriesDataWeeks[maticna_buyer][maticna_bidder][week_index] = self.timeSeriesDataWeeks[maticna_buyer][maticna_bidder][week_index] + float(row[trans_amount_n])

            # add data 2 monthly dataset
            # add data 2 monthly dataset

            if self.enableConversionMonthly:

                # init variable
                # init variable

                if maticna_buyer not in self.timeSeriesDataMonths.keys():
                    self.timeSeriesDataMonths[maticna_buyer] = {}
                if maticna_bidder not in self.timeSeriesDataMonths[maticna_buyer].keys():
                    self.timeSeriesDataMonths[maticna_buyer][maticna_bidder] = [float(0.0)] * (len(self.date2MonthConverter))

                # add transaction
                # add transaction

                tmp_date = row[trans_date_n][:-3]
                if tmp_date not in self.date2MonthConverter:
                    # avoid potential errors
                    continue
                tmp_month_n = self.date2MonthConverter[tmp_date] - 1

                self.timeSeriesDataMonths[maticna_buyer][maticna_bidder][tmp_month_n] = self.timeSeriesDataMonths[maticna_buyer][maticna_bidder][tmp_month_n] + float(row[trans_amount_n])

        return None

    def saveTimeSeriesFromat2File(self):
        '''
        function saves time series data fromat to file

        :return: none
        '''

        # set file name
        # set file name

        fileNameLimitExt = '-' + str(self.rawDataLimit) if self.rawDataLimit > 0 else ''
        self.timeSeriesFile = self.timeSeriesFile.replace('-LIMIT', fileNameLimitExt)

        # save daily transactions
        # save daily transactions

        if self.enableConversionDaily:
            dataSetDays = self.getDataFormatReadyForFileSave(self.timeSeriesDataDays, self.date2DayConverter)
            fileNameDays = self.timeSeriesFile.replace('FRQSAMPLE', 'days')
            self.conf.sharedCommon.sendDict2Output(dataSetDays, fileNameDays)

        # save weekly transactions
        # save weekly transactions

        if self.enableConversionWeekly:
            dataSetWeeks = self.getDataFormatReadyForFileSave(self.timeSeriesDataWeeks, self.date2WeekConverter)
            fileNameWeeks = self.timeSeriesFile.replace('FRQSAMPLE', 'weeks')
            self.conf.sharedCommon.sendDict2Output(dataSetWeeks, fileNameWeeks)

        # save monthly transactions
        # save monthly transactions

        if self.enableConversionMonthly:
            dataSetMonths = self.getDataFormatReadyForFileSave(self.timeSeriesDataMonths, self.date2MonthConverter)
            fileNameMonths = self.timeSeriesFile.replace('FRQSAMPLE', 'months')
            self.conf.sharedCommon.sendDict2Output(dataSetMonths, fileNameMonths)

        return None

    def getDataFormatReadyForFileSave(self, timeSeriesDict, date2IntDict):
        '''
        function converts dictionary of format dict[buyerId][bidderId] = [trans-on-day-1, trans-on-day-2, trans-on-day-3, ...]
        into a dict [buyerId, bidderId, trans-on-day-1, trans-on-day-2, trans-on-day-3, ...]; the latter is required
        in oder to be saved in file by general function

        :param timeSeriesDict: dictionary
        :return: dictionary
        '''

        returnDict = {}
        returnDict['head'] = ['sifra_pu', 'bidderId', 'skd'] + list(date2IntDict.keys())
        returnDict['data'] = []

        for sifra_pu, bidderDict in timeSeriesDict.items():
            for bidderId, transactionList in bidderDict.items():
                tmp_skd = self.privateCompanyDict[bidderId]['glavna_dejavnost_skd'] if bidderId in self.privateCompanyDict else '00.00'
                newList = [sifra_pu, bidderId, tmp_skd[:2]] + [str(round(i, 2)) for i in transactionList]
                returnDict['data'].append(newList)

        return returnDict

    # locally oriented methods
    # locally oriented methods

    def getPrivateCompanyClassificatorDictSI(self):
        '''
        returns a dict of current and past private companies for Slovenia

        :return: return None
        '''

        sql = self.conf.cDB.sql
        cur = self.conf.cDB.db.cursor()

        queryBase = "select {},{} from {}"
        queryString = sql.SQL(queryBase).format(
            # set queried fields
            sql.Identifier('maticna'),
            sql.Identifier('glavna_dejavnost_skd'),
            # set table name
            sql.Identifier('prs_enota_rs'))
        # print(queryString.as_string(cur))
        cur.execute(queryString)
        currentEntities = self.conf.sharedCommon.returnSqlDataInDictFormat(cur, 'maticna')

        queryBase = "select {},{} from {}"
        queryString = sql.SQL(queryBase).format(
            # set queried fields
            sql.Identifier('maticna'),
            sql.Identifier('glavna_dejavnost_skd'),
            # set table name
            sql.Identifier('hs_prs_enota_rs'))
        # print(queryString.as_string(cur))
        cur.execute(queryString)
        historicEntities = self.conf.sharedCommon.returnSqlDataInDictFormat(cur, 'maticna')

        # merge entities into a dictionary
        # merge entities into a dictionary

        self.privateCompanyDict = {**historicEntities, **currentEntities}

        return None




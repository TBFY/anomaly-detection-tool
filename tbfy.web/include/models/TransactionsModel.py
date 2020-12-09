
'''
TransactionsModel is a module serving a htmls, related to transactions analysis
'''

class TransactionsModel:

    def __init__(self, conf, getVars):
        self.confObj = conf
        self.getVars = getVars
        self.dataRootFilePath = self.confObj.publicSpendingDataRoot
        self.contentHtml = 'Error: SearchModel HTML nof found.'

    def getView(self):
        '''
        a central DataPresentation function returning correct html

        :return: string, html format
        '''

        query_a = "landing" if self.getVars.get('a') == None else self.getVars.get('a')
        query_a = query_a.lower()

        # get content HTML
        # get content HTML

        if(query_a == "landing"):
            self.dataRootFilePath = self.confObj.os.path.join(self.dataRootFilePath, 'std_deviation')
            self.contentHtml = self.transactionsLanding()
        elif(query_a == "stddev"):
            self.dataRootFilePath = self.confObj.os.path.join(self.dataRootFilePath, 'std_deviation')
            self.contentHtml = self.standardDeviation()
        elif(query_a == "jnks"):
            self.dataRootFilePath = self.confObj.os.path.join(self.dataRootFilePath, 'jenks')
            self.contentHtml = self.jenksNaturalBreaks()
        elif(query_a == "periods"):
            self.dataRootFilePath = self.confObj.os.path.join(self.dataRootFilePath, 'period_margin')
            self.contentHtml = self.periods()
        elif(query_a == "deriv"):
            self.dataRootFilePath = self.confObj.os.path.join(self.dataRootFilePath, 'local_extremes')
            self.contentHtml = self.derivatives()
        elif(query_a == "part"):
            self.dataRootFilePath = self.confObj.os.path.join(self.dataRootFilePath, 'time_periods')
            self.contentHtml = self.partialCumulatives()

        return self.contentHtml

    def transactionsLanding(self):
        '''
        returning transactions landing

        :return: string, html format
        '''

        # generate html view
        # generate html view

        dict = {}
        dict['transactionsMenu'] = self.getTransactionsMenu()

        content = self.confObj.Template(filename='templates/tr_landing.tpl')
        return content.render(data=dict)

    def getTransactionsMenu(self):
        '''
        function returns core transactions menu

        :return: html string
        '''

        # identify active menu
        # identify active menu

        query_a = "landing" if self.getVars.get('a') == None else self.getVars.get('a')
        query_a = query_a.lower()

        # render html
        # render html

        dict = {}
        dict['query_a'] = query_a

        content = self.confObj.Template(filename='templates/tr_menu.tpl')
        return content.render(data=dict)

    def standardDeviation(self):
        '''
        standardDeviation is presenting the most deviating transactions from an average value

        :return: string, html format
        '''

        # get a list of all files of form deviationList*
        # get a list of all files of form deviationList*

        all_files = self.confObj.os.listdir(self.dataRootFilePath)
        sd_files = list(filter(lambda s: 'deviationList' in s, all_files))

        filesDict = {}
        for filename in sd_files:
            numList = (list(filter(str.isdigit, filename)))
            numString = "".join(numList)
            if(numString == ""): numString = "0"
            filesDict[numString] = filename

        # gather final data
        # gather final data

        idfile = "0" if self.getVars.get('idfile') == None else self.getVars.get('idfile')
        selectedFileName = "deviationList.tsv" if idfile == "0" else "deviationList-" + idfile + ".tsv"

        # read file data into dict
        # read file data into dict

        companyList = []
        import csv
        with open(self.confObj.os.path.join(self.dataRootFilePath, selectedFileName), newline='\n') as csvfile:
            fieldnames = ['company_id', 'company_name', 'deviation']
            fileData = csv.DictReader(csvfile, fieldnames=fieldnames,  delimiter='\t')
            for row in fileData:
                companyList.append(row)

        if(len(companyList) > 1): companyList = companyList[1:]

        # generate html view
        # generate html view

        dict = {}
        dict["templateTitle"] = "Average Deviation Anomaly"
        dict["fileList"] = filesDict
        dict["idfile"] = idfile
        dict["companyList"] = companyList
        dict["pageAddress"] = "stddev"

        content = self.confObj.Template(filename='templates/tr_stddev_data.tpl')
        return content.render(data=dict)

    def jenksNaturalBreaks(self):
        '''
        jenks natiral breaks is an upgrade of standard deviation analysis; it groups transaction sums into groups
        and then, within groups, selects the moist deviating numbers from group average (jensk is 1-dim kMeans)

        :return: string, html format
        '''

        # get a list of all files of form jenks*
        # get a list of all files of form jenks*

        all_files = self.confObj.os.listdir(self.dataRootFilePath)
        sd_files = list(filter(lambda s: 'jenks' in s, all_files))

        skdDict = {}
        for filename in sd_files:
            numList = (list(filter(str.isdigit, filename)))
            numString = "".join(numList)
            if(numString == ""):
                numString = ""
            else:
                skdDict[numString] = ''

        # sort skdDict
        # sort skdDict

        skdDict = {k: skdDict[k] for k in sorted(skdDict)}
        skdDict = self.confObj.sharedMethods.getSKDDescriptions(self.confObj, skdDict)

        # gather final data
        # gather final data

        idfile = "0" if self.getVars.get('idfile') == None else self.getVars.get('idfile')
        selectedFileName = "jenks.tsv" if idfile == "0" else "jenks-" + idfile + ".tsv"

        # read file data into dict
        # read file data into dict

        limitListTo = 100
        companyList = []
        import csv
        with open(self.confObj.os.path.join(self.dataRootFilePath, selectedFileName), newline='\n') as csvfile:
            fieldnames = ['company_id', 'company_name', 'deviation']
            fileData = csv.DictReader(csvfile, fieldnames=fieldnames,  delimiter='\t')
            row_n = 0
            for row in fileData:
                companyList.append(row)
                row_n += 1
                if row_n == limitListTo:
                    break

        if(len(companyList) > 1): companyList = companyList[1:]

        # generate html view
        # generate html view

        dict = {}
        dict['transactionsMenu'] = self.getTransactionsMenu()
        dict["idfile"] = idfile
        dict["companyList"] = companyList
        dict["pageAddress"] = "jnks"
        dict["skdDict"] = skdDict
        dict["tsv_file_source"] = self.confObj.urlHost + 'data_results/publicSpending/jenks/' + selectedFileName

        content = self.confObj.Template(filename='templates/tr_jenks.tpl')
        return content.render(data=dict)

    def periods(self):
        '''
        function returns periods analysis results

        :return: string, html format
        '''

        # get a list of all files of form deriv-companies*
        # get a list of all files of form deriv-companies*

        all_files = self.confObj.os.listdir(self.dataRootFilePath)
        sd_files = list(filter(lambda s: 'periods-companies' in s, all_files))

        filesDict = {}
        skdDict = {}
        for filename in sd_files:
            numList = (list(filter(str.isdigit, filename)))
            numString = "".join(numList)
            if(numString == ""):
                numString = ""
            else:
                skdDict[numString] = ''
            filesDict[numString] = filename

        # sort skdDict
        # sort skdDict

        skdDict = {k: skdDict[k] for k in sorted(skdDict)}
        skdDict = self.confObj.sharedMethods.getSKDDescriptions(self.confObj, skdDict)

        # gather final data
        # gather final data

        idfile = "" if self.getVars.get('idfile') == None else self.getVars.get('idfile')
        if idfile == "0":
            idfile = "00"
        selectedCompaniesFileName = "periods-companies.tsv" if idfile == "" else "periods-companies-" + idfile + '.tsv'
        selectedTimelineFileName = "periods-time.tsv" if idfile == "" else "periods-time-" + idfile + '.tsv'

        dict = {}
        dict['transactionsMenu'] = self.getTransactionsMenu()
        dict["fileList"] = filesDict
        dict["skdDict"] = skdDict
        dict["idfile"] = idfile
        dict["tsv_file_companies"] = self.confObj.urlHost + 'data_results/publicSpending/period_margin/' + selectedCompaniesFileName
        dict["tsv_file_timeline"] = self.confObj.urlHost + 'data_results/publicSpending/period_margin/' + selectedTimelineFileName

        content = self.confObj.Template(filename='templates/tr_periods.tpl')
        return content.render(data=dict)

    def derivatives(self):
        '''
        function returns local extreme analysis (which is actually a data set derivative)

        :return: string, html format
        '''

        # get a list of all files of form deriv_cumul*
        # get a list of all files of form deriv_cumul*

        all_files = self.confObj.os.listdir(self.dataRootFilePath)
        sd_files = list(filter(lambda s: 'derivatives-companies' in s, all_files))

        filesDict = {}
        skdDict = {}
        for filename in sd_files:
            numList = (list(filter(str.isdigit, filename)))
            numString = "".join(numList)
            if(numString == ""):
                numString = ""
            else:
                skdDict[numString] = ''
            filesDict[numString] = filename

        # sort skdDict
        # sort skdDict

        skdDict = {k: skdDict[k] for k in sorted(skdDict)}
        skdDict = self.confObj.sharedMethods.getSKDDescriptions(self.confObj, skdDict)

        # gather final data
        # gather final data

        idfile = "" if self.getVars.get('idfile') == None else self.getVars.get('idfile')
        if idfile == "0":
            idfile = "00"
        selectedCompaniesFileName = "derivatives-companies.tsv" if idfile == "" else "derivatives-companies-" + idfile + '.tsv'
        selectedTimelineFileName = "derivatives-time.tsv" if idfile == "" else "derivatives-time-" + idfile + '.tsv'

        dict = {}
        dict['transactionsMenu'] = self.getTransactionsMenu()
        dict["fileList"] = filesDict
        dict["skdDict"] = skdDict
        dict["idfile"] = idfile
        dict["tsv_file_companies"] = self.confObj.urlHost + 'data_results/publicSpending/local_extremes/' + selectedCompaniesFileName
        dict["tsv_file_timeline"] = self.confObj.urlHost + 'data_results/publicSpending/local_extremes/' + selectedTimelineFileName

        content = self.confObj.Template(filename='templates/tr_derivatives.tpl')
        return content.render(data=dict)

    def partialCumulatives(self):
        '''
        function returns partial cumulative analysis results in html format

        :: drty code => to be done again

        :return: string, html format
        '''

        baseFileName = 'part_cumul'

        # get a list of all files of form partialCumulative*
        # get a list of all files of form partialCumulative*

        all_files = self.confObj.os.listdir(self.dataRootFilePath)
        sd_files = list(filter(lambda s: baseFileName in s, all_files))

        filesDict = {}
        skdDict = {}
        for filename in sd_files:
            numList = (list(filter(str.isdigit, filename)))
            numString = "".join(numList)
            if(numString == ""):
                numString = ""
            else:
                skdDict[numString] = ''
            filesDict[numString] = filename

        # sort skdDict
        # sort skdDict

        skdDict = {k: skdDict[k] for k in sorted(skdDict)}
        skdDict = self.confObj.sharedMethods.getSKDDescriptions(self.confObj, skdDict)

        # gather final data
        # gather final data

        idfile = "" if self.getVars.get('idfile') == None else self.getVars.get('idfile')
        if idfile == "0":
            idfile = "00"

        # generate html view
        # generate html view

        dict = {}
        dict['transactionsMenu'] = self.getTransactionsMenu()
        dict["fileList"] = filesDict
        dict["skdDict"] = skdDict
        dict["idfile"] = idfile
        dict["idfile"] = idfile
        dict["tsv_file_source"] = self.confObj.urlHost + 'data_results/publicSpending/time_periods/part_cumul' + idfile + '.tsv'
        dict["pageAddress"] = "part"

        content = self.confObj.Template(filename='templates/tr_partial_cumulative.tpl')
        return content.render(data=dict)

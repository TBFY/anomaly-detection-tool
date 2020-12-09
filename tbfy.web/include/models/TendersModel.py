
'''
TendersModel is a module serving htmls, related to tender analysis
'''

class TendersModel:

    def __init__(self, conf, getVars):
        self.conf = conf
        self.getVars = getVars
        self.dataRootFilePath = self.conf.publicSpendingDataRoot
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
            self.dataRootFilePath = self.conf.os.path.join(self.dataRootFilePath, 'std_deviation')
            self.contentHtml = self.tenderLanding()
        elif(query_a == "dtree"):
            self.dataRootFilePath = self.conf.publicTenderDataRoot
            self.dataRootFilePath = self.conf.os.path.join(self.dataRootFilePath, 'dTree')
            self.contentHtml = self.decisionTreeSchema()
        elif(query_a == "ratios"):
            self.dataRootFilePath = self.conf.publicTenderDataRoot
            self.dataRootFilePath = self.conf.os.path.join(self.dataRootFilePath, 'ratios')
            self.contentHtml = self.tenderRatiosMain()
        elif (query_a == "distributions"):
            self.dataRootFilePath = self.conf.publicTenderDataRoot
            self.dataRootFilePath = self.conf.os.path.join(self.dataRootFilePath, 'distributions')
            self.contentHtml = self.tenderDistributionsMain()
        elif(query_a == "cluster"):
            self.dataRootFilePath = self.conf.publicTenderDataRoot
            self.dataRootFilePath = self.conf.os.path.join(self.dataRootFilePath, 'kMeans')
            self.contentHtml = self.tenderkMeans()
        elif(query_a == "dependencies"):
            self.dataRootFilePath = self.conf.publicTenderDataRoot
            self.dataRootFilePath = self.conf.os.path.join(self.dataRootFilePath, 'relations_bb')
            self.contentHtml = self.dependenciesMain()
        elif(query_a == "stream_story"):
            self.dataRootFilePath = self.conf.publicTenderDataRoot
            self.dataRootFilePath = self.conf.os.path.join(self.dataRootFilePath, 'streamStory')
            self.contentHtml = self.tenderStreamStory()

        return self.contentHtml

    def tenderLanding(self):
        '''
        standardDeviation is presenting the most deviating transactions from an average value

        :return: string, html format
        '''

        # generate html view
        # generate html view

        dict = {}
        dict['tenderMenu'] = self.getTenderMenu()
        dict['commonAnomalyRankFilePath'] = self.conf.publicTenderDataUrl + 'common-anomaly-measure.tsv'

        content = self.conf.Template(filename='templates/te_landing.tpl')
        return content.render(data=dict)

    def getTenderMenu(self):
        '''
        function returns core tender menu

        :return: html string
        '''

        # identify active menu
        # identify active menu

        query_a = "landing" if self.getVars.get('a') == None else self.getVars.get('a')
        query_a = query_a.lower()

        query_t = "" if self.getVars.get('t') == None else self.getVars.get('t')
        query_t = query_t.lower()

        # render html
        # render html

        dict = {}
        dict['query_a'] = query_a
        dict['query_t'] = query_t

        content = self.conf.Template(filename='templates/te_menu.tpl')
        return content.render(data=dict)

    def decisionTreeSchema(self):
        '''
        function displays a certain decision tree schema

        :return: string, html format
        '''

        # get all available fields that can be included into decision tree schema
        # get all available fields that can be included into decision tree schema

        import SharedTenderDataMethods as SharedTenderData
        sharedTenderData = SharedTenderData.SharedTenderDataMethods()

        # define tree depth param
        # define tree depth param

        dTreeDepth = {}
        for i in range(8):
            if i == 0:
                dTreeDepth["0"] = "Show full tree"
            elif i == 1:
                dTreeDepth["1"] = "1 row"
            else:
                strKey = str(i)
                dTreeDepth[strKey] = strKey + " rows"

        # get a list of all files of form partialCumulative
        # get a list of all files of form partialCumulative

        dict = {}
        dict['tenderMenu'] = self.getTenderMenu()
        dict["filePath"] = self.conf.os.path.join(self.conf.publicTenderDataUrl, 'dTree/')
        dict["fileName"] = 'dt_schema.png'
        dict["dTreeParams"] = sharedTenderData.getTenderdataFieldKeys()
        dict["dTreeDepth"] = dTreeDepth

        content = self.conf.Template(filename='templates/te_dtree.tpl')
        return content.render(data=dict)

    def tenderRatiosMain(self):

        query_t = "rev_per_employee" if self.getVars.get('t') == None else self.getVars.get('t')
        query_t = query_t.lower()

        if query_t == 'custom':
            return self.tenderRatiosCustom()
        elif query_t == 'rev_per_employee':
            return self.tenderRatios('revenuePerEmployee')
        elif query_t == 'budget_assesment':
            return self.tenderRatios('budgetAssessment')

    def tenderRatiosCustom(self):

        dict = {}
        dict['tenderMenu'] = self.getTenderMenu()

        content = self.conf.Template(filename='templates/te_ratios_custom.tpl')
        return content.render(data=dict)

    def tenderRatios(self, ratioCategoryDir):
        '''
        function returns html page related to ratio results

        :return: string, html format
        '''

        # get all available country data
        # get all available country data

        dirFullpath = self.conf.os.path.join(self.conf.publicTenderDataRoot, 'ratios/')
        dirFullpath = dirFullpath + ratioCategoryDir + '/'
        allCountryFiles = [f for f in self.conf.os.listdir(dirFullpath) if f.find('data-values.tsv') > 0]

        dataSourceLst = []
        for fileName in allCountryFiles:
            fileNamePieces = fileName.split('-data-values.tsv')
            countryName = fileNamePieces[0]
            if countryName == 'si-ministry':
                dataSourceLst.append(countryName)
            else:
                dataSourceLst.append(countryName.capitalize())
        dataSourceLst = sorted(dataSourceLst, key=str.lower)

        dataSourceLstSelected = 'si-ministry' if self.getVars.get('datasource') == None else self.getVars.get('datasource')

        fullDirPath = self.conf.urlHost + self.conf.os.path.join(self.conf.publicTenderDataUrl, 'ratios/')
        fullDirPath = self.conf.os.path.join(fullDirPath, ratioCategoryDir + "/")

        # get ratio descriptions
        # get ratio descriptions

        ratioDescHTML = ''
        jsMetaDataRenderFunction = 'te_ratios_custom.js'
        if ratioCategoryDir == 'revenuePerEmployee':
            ratioDescHTML = self.conf.Template(filename='templates/te_ratios_rev_per_employee.tpl').render()
            jsMetaDataRenderFunction = 'te_ratios_rev_per_employee.js'
        elif ratioCategoryDir == 'budgetAssessment':
            ratioDescHTML = self.conf.Template(filename='templates/te_ratios_bdg_assessment.tpl').render()
            jsMetaDataRenderFunction = 'te_ratios_bdg_assessment.js'

        # create a template
        # create a template

        dict = {}
        dict['tenderMenu'] = self.getTenderMenu()
        dict["tsvAllRatioPointsFilePath"] = self.conf.os.path.join(fullDirPath, dataSourceLstSelected + '-data-values.tsv')
        dict["tsvPosDevPointsFilePath"] = self.conf.os.path.join(fullDirPath, dataSourceLstSelected + '-pos-deviations.tsv')
        dict["tsvNegDevPointsFilePath"] = self.conf.os.path.join(fullDirPath, dataSourceLstSelected + '-neg-deviations.tsv')
        dict["dataSourceLst"] = dataSourceLst
        dict["dataSourceLstSelected"] = dataSourceLstSelected
        dict["ratioDescHTML"] = ratioDescHTML
        dict["jsMetaDataRenderFunction"] = jsMetaDataRenderFunction
        dict["ratioCategoryDir"] = ratioCategoryDir

        content = self.conf.Template(filename='templates/te_ratios.tpl')
        return content.render(data=dict)

    def tenderDistributionsMain(self):

        query_t = "num_of_offers" if self.getVars.get('t') == None else self.getVars.get('t')
        query_t = query_t.lower()

        if query_t == 'custom':
            return self.tenderDistributionsCustom()
        elif query_t == 'num_of_offers':
            return self.tenderDistributions('offersNum')
        elif query_t == 'budget_assessment':
            return self.tenderDistributions('budgetAssessment')

    def tenderDistributions(self, distributionsCategoryDir):

        # get all available country data
        # get all available country data

        dirFullpath = self.conf.os.path.join(self.conf.publicTenderDataRoot, 'distributions/')
        dirFullpath = dirFullpath + distributionsCategoryDir + '/'
        allCountryFiles = [f for f in self.conf.os.listdir(dirFullpath) if f.find('data-values.tsv') > 0]

        dataSourceLst = []
        for fileName in allCountryFiles:
            fileNamePieces = fileName.split('-data-values.tsv')
            countryName = fileNamePieces[0]
            dataSourceLst.append(countryName)

        dataSourceLstSelected = 'si-ministry' if self.getVars.get('datasource') == None else self.getVars.get('datasource')

        idfile = '' if self.getVars.get('idfile') == None else self.getVars.get('idfile')
        baseFileNameSelected = dataSourceLstSelected + '-' + idfile

        fullDirPath = self.conf.urlHost + self.conf.os.path.join(self.conf.publicTenderDataUrl, 'distributions/')
        fullDirPath = self.conf.os.path.join(fullDirPath, distributionsCategoryDir + "/")

        # get distribution descriptions
        # get distribution descriptions

        distributionDescHTML = ''
        #jsMetaDataRenderFunction = 'te_ratios_custom.js'
        if distributionsCategoryDir == 'offersNum':
            distributionDescHTML = self.conf.Template(filename='templates/te_distributions_offers_num.tpl').render()
            jsMetaDataRenderFunction = 'te_distributions_num_offers.js'
        elif distributionsCategoryDir == 'budgetAssessment':
            distributionDescHTML = self.conf.Template(filename='templates/te_distributions_bdg_assessment.tpl').render()
            jsMetaDataRenderFunction = 'te_distributions_bdg_assessment.js'

        # get common distribution
        # get common distribution

        fullRootPath = self.conf.os.path.join(self.conf.publicTenderDataRoot, 'distributions')
        fullRootPath = self.conf.os.path.join(fullRootPath, distributionsCategoryDir + "/")

        commonDistributionDict = self.conf.sharedCommon.readDataFile2Dict(fullRootPath + baseFileNameSelected +  '-cmn-distribution.tsv', "\t")
        common_distr = commonDistributionDict['data'][0][0]

        # get a list of all files of form partialCumulative*
        # get a list of all files of form partialCumulative*

        all_files = self.conf.os.listdir(fullRootPath)
        my_files = list(filter(lambda s: dataSourceLstSelected in s, all_files))

        cpvDict = {}
        for filename in my_files:
            numList = (list(filter(str.isdigit, filename)))
            numString = "".join(numList)
            if(numString == ""):
                continue
            else:
                cpvDict[numString] = ''

        # get cpv description
        # get cpv description

        cpvDict = {k: cpvDict[k] for k in sorted(cpvDict)}
        cpvDict = self.conf.sharedMethods.getCPVDescriptions(self.conf, cpvDict)

        # get query_t
        # get query_t

        query_t = "num_of_offers" if self.getVars.get('t') == None else self.getVars.get('t')
        query_t = query_t.lower()

        # get html
        # get html

        dict = {}
        dict['tenderMenu'] = self.getTenderMenu()
        dict["tsvAllDistrPointsFilePath"] = self.conf.os.path.join(fullDirPath, baseFileNameSelected + '-data-values.tsv')
        dict["tsvPosDevPointsFilePath"] = self.conf.os.path.join(fullDirPath, baseFileNameSelected + '-pos-deviations.tsv')
        dict["tsvNegDevPointsFilePath"] = self.conf.os.path.join(fullDirPath, baseFileNameSelected + '-neg-deviations.tsv')
        dict["dataSourceLst"] = dataSourceLst
        dict["dataSourceLstSelected"] = dataSourceLstSelected
        dict['distributionDescHTML'] = distributionDescHTML
        dict["jsMetaDataRenderFunction"] = jsMetaDataRenderFunction
        dict["common_distr"] = common_distr
        dict["cpvDict"] = cpvDict
        dict["query_t"] = query_t
        dict["idfile"] = idfile

        content = self.conf.Template(filename='templates/te_distributions.tpl')
        return content.render(data=dict)

    def tenderDistributionsCustom(self):

        dict = {}
        dict['tenderMenu'] = self.getTenderMenu()

        content = self.conf.Template(filename='templates/te_distributions_custom.tpl')
        return content.render(data=dict)

    def dependenciesMain(self):

        query_t = "buyer2bidder" if self.getVars.get('t') == None else self.getVars.get('t')
        query_t = query_t.lower()

        if query_t == 'mutual':
            return self.dependenciesSpecific('mutual')
        elif query_t == 'buyer2bidder':
            return self.dependenciesSpecific('buyer2bidder')
        elif query_t == 'bidder2buyer':
            return self.dependenciesSpecific('bidder2buyer')

    def dependenciesSpecific(self, fileExtension):
        '''
        funtion renders the html for dependencies analysis

        :param fileExtension: string, category of a file
        :return: string, html
        '''

        fullDirPath = self.conf.urlHost + self.conf.os.path.join(self.conf.publicTenderDataUrl, 'relations_bb/')

        dependencieDescHTML = ''
        if fileExtension == 'mutual':
            dependencieDescHTML = self.conf.Template(filename='templates/te_dependencies_mutual_desc.tpl').render()
        elif fileExtension == 'buyer2bidder':
            dependencieDescHTML = self.conf.Template(filename='templates/te_dependencies_buyer2bidder_desc.tpl').render()
        elif fileExtension == 'bidder2buyer':
            dependencieDescHTML = self.conf.Template(filename='templates/te_dependencies_bidder2buyer_desc.tpl').render()

        baseFileNameSelected = 'si-ministry-' + fileExtension + '.tsv'

        dict = {}
        dict['tenderMenu'] = self.getTenderMenu()
        dict['dependencieDescHTML'] = dependencieDescHTML
        dict['dataSourceLstSelected'] = 'si-ministry'
        dict['tsvDependenicesFilePath'] = self.conf.os.path.join(fullDirPath, baseFileNameSelected)

        content = self.conf.Template(filename='templates/te_dependencies.tpl')
        return content.render(data=dict)

    def tenderkMeans(self):
        '''
        function returns kMeans analysis of tender data

        :return: string, html format
        '''

        # first, get cluster id
        # first, get cluster id

        cluster_id_base = '' if self.getVars.get('cid') == None else self.getVars.get('cid')
        cluster_id_base = cluster_id_base.lower()

        cluster_id = '-' + cluster_id_base if len(cluster_id_base) > 0 else ''

        if len(cluster_id) > 36:
            cluster_id = ''

        # then, get all possible datasources
        # then, get all possible datasources

        dirFullpath = self.conf.os.path.join(self.conf.publicTenderDataRoot, 'kMeans/')
        allCountryFiles = [f for f in self.conf.os.listdir(dirFullpath) if f.find('centroids-coordinates.tsv') > 0]

        dataSourceLst = []
        for fileName in allCountryFiles:
            fileNamePieces = fileName.split('-centroids-coordinates.tsv')
            countryName = fileNamePieces[0]
            if countryName == 'si-ministry':
                dataSourceLst.append(countryName)
            else:
                dataSourceLst.append(countryName.capitalize())
        dataSourceLst = sorted(dataSourceLst, key=str.lower)

        # identify data source
        # identify data source

        dataSourceLstSelected = 'si-ministry' if self.getVars.get('datasource') == None else self.getVars.get('datasource').lower()

        # if cluster_id defined, no file prependix is allowed (as prependix is encoded into cluster_id)
        # if cluster_id defined, no file prependix is allowed (as prependix is encoded into cluster_id)

        if len(cluster_id) > 0:
            dataSourceLstSelectedFilePrep = ''
        else:
            dataSourceLstSelectedFilePrep = dataSourceLstSelected + '-'

        # get paths to files
        # get paths to files

        dirPath2Data = self.conf.urlHost + self.conf.os.path.join(self.conf.publicTenderDataUrl, 'kMeans/')
        rootPath2Data = self.conf.os.path.join(self.conf.publicTenderDataRoot, 'kMeans/')

        # define centroids file name
        # define centroids file name

        centroidsFileName = 'centroids-coordinates' + cluster_id + '.tsv'
        if not self.conf.os.path.isfile(self.conf.os.path.join(rootPath2Data, centroidsFileName)):
            cluster_id = ''
            centroidsFileName = 'centroids-coordinates' + cluster_id + '.tsv'
        centroidsFileName = dataSourceLstSelectedFilePrep + centroidsFileName

        gainsFileName = dataSourceLstSelectedFilePrep + 'cluster-gain-values-log' + cluster_id + '.tsv'
        gainsFilePath = self.conf.os.path.join(dirPath2Data, gainsFileName)

        # read in centorids data
        # read in centorids data

        centroidsRootFilePath = self.conf.os.path.join(rootPath2Data, centroidsFileName)
        centroidsDict = self.conf.sharedCommon.readDataFile2Dict(centroidsRootFilePath, "\t")

        # once centroids data are read, selected datasource can be 100% identified (it's written in centroids data file)
        # once centroids data are read, selected datasource can be 100% identified (it's written in centroids data file)

        datasource_index = centroidsDict['head'].index('data_source')
        dataSourceLstSelected = centroidsDict['data'][0][datasource_index]

        #return centroidsDict

        numOfElementsIndex = centroidsDict['head'].index('num_of_elements')

        numOfCentroidElementsMax = max([int(sublist[numOfElementsIndex]) for sublist in centroidsDict['data']])
        numOfCentroidElementsMin = min([int(sublist[numOfElementsIndex]) for sublist in centroidsDict['data']])

        # define all axes labels
        # define all axes labels

        allowedAxisLabelsDict = {}
        if dataSourceLstSelected == 'si-ministry':
            #allowedAxisLabelsDict['centroid_n'] = ''
            #allowedAxisLabelsDict['num_of_elements'] = ''
            #allowedAxisLabelsDict['Narocnik_OBCINA'] = ''
            #allowedAxisLabelsDict['Narocnik_Oblika'] = ''
            #allowedAxisLabelsDict['Narocnik_Glavna_Dejavnost_SKD'] = ''
            allowedAxisLabelsDict['Narocnik_Velik_RS'] = 'Buyer num of employees'
            #allowedAxisLabelsDict['Narocnik_Velik_EU'] = ''
            allowedAxisLabelsDict['Narocnik_Regija'] = 'Company region'
            #allowedAxisLabelsDict['Narocnik_Dejavnost'] = ''
            allowedAxisLabelsDict['VrstaNarocila'] = 'Order type'
            allowedAxisLabelsDict['VrstaPostopka'] = 'Procedure type'
            allowedAxisLabelsDict['VrstaPostopka_EU'] = 'Procedure type, EU'
            allowedAxisLabelsDict['Merila'] = 'Criterion'
            allowedAxisLabelsDict['OkvirniSporazum'] = 'Frame agreement'
            allowedAxisLabelsDict['SkupnoNarocanje'] = 'Joint order'
            allowedAxisLabelsDict['EUsredstva'] = 'EU funds'
            allowedAxisLabelsDict['ObjavaVEU'] = 'Publishes in EU'
            allowedAxisLabelsDict['StPrejetihPonudb'] = 'Num of offers'
            allowedAxisLabelsDict['SkupnaPonudba'] = 'Joint ofer'
            allowedAxisLabelsDict['OcenjenaVrednost'] = 'Estimated tender value'
            allowedAxisLabelsDict['KoncnaVrednost'] = 'Final tender value'
            allowedAxisLabelsDict['OddanoPodizvajalcem'] = 'Subcontractors involved'
            #allowedAxisLabelsDict['CPV_glavni_2mesti'] = ''
            allowedAxisLabelsDict['Podrocje'] = 'Field'
            allowedAxisLabelsDict['VrstaPostopkaIzracunan'] = 'Procedure type calculation'
            allowedAxisLabelsDict['NarocnikPostnaStevilka'] = 'Buyer post office'
            allowedAxisLabelsDict['PonudnikPostnaStevilka'] = 'Bidder post office'
            allowedAxisLabelsDict['Ponudnik_OBCINA'] = 'Bidder municipality'
            #allowedAxisLabelsDict['Ponudnik_Velik_EU'] = ''
            allowedAxisLabelsDict['Ponudnik_Velik_RS'] = 'Bidder num of employees'
            #allowedAxisLabelsDict['OcenjenaVrednostSorazmerno'] = ''
            #allowedAxisLabelsDict['KoncnaVrednostSorazmerno'] = ''
            #allowedAxisLabelsDict['MJU labels'] = ''
        else:
            allowedAxisLabelsDict['cpv'] = 'CPV'
            allowedAxisLabelsDict['publishedOnTed'] = 'Published on TED'
            allowedAxisLabelsDict['amount'] = 'Amount'
            #allowedAxisLabelsDict['currency'] = 'Currency'
            allowedAxisLabelsDict['buyerPostId'] = 'Buyer post'
            allowedAxisLabelsDict['buyerCountry'] = 'Buyer country'
            allowedAxisLabelsDict['supplierCountry'] = 'Supplier country'
            allowedAxisLabelsDict['awardCriteriaDetails'] = 'Award criteria'
            allowedAxisLabelsDict['supplier_num_employees'] = 'Supplier num employees'
            allowedAxisLabelsDict['supplier_jurisdiction'] = 'Supplier jurisdiction'
            allowedAxisLabelsDict['supplier_postal_code'] = 'Supplier post'

        # find available axes labels
        # find available axes labels

        availableFields = centroidsDict['head'].copy()
        availableFields.remove('centroid_n')
        availableFields.remove('num_of_elements')
        availableFields.remove('data_source')

        finalAxesDict = {}
        for key in availableFields:
            if key in allowedAxisLabelsDict:
                finalAxesDict[key] = allowedAxisLabelsDict[key]

        # default values
        # default values

        if dataSourceLstSelected == 'si-ministry':
            defaultXLabel = 'Narocnik_Velik_RS'
        else:
            defaultXLabel = 'supplier_num_employees'

        if defaultXLabel not in finalAxesDict:
            defaultXLabel = availableFields[0]

        defaultXLabelText = allowedAxisLabelsDict[defaultXLabel]

        if dataSourceLstSelected == 'si-ministry':
            defaultYLabel = 'KoncnaVrednost'
        else:
            defaultYLabel = 'amount'

        if defaultYLabel not in finalAxesDict:
            defaultYLabel = availableFields[1]

        if defaultYLabel == defaultXLabel:
            if defaultXLabel == availableFields[0]:
                defaultYLabel = availableFields[1]
            else:
                defaultYLabel = availableFields[0]

        defaultYLabelText = allowedAxisLabelsDict[defaultYLabel]

        # read all mappings into dictionary
        # read all mappings into dictionary

        import json
        valueKeyMaps = self.conf.sharedMethods.getAllValueMaps(self.conf)

        # render html
        # render html

        dict = {}
        dict['tenderMenu'] = self.getTenderMenu()
        dict["gainDataFilePath"] = gainsFilePath
        dict["centroidsDataFileDir"] = dirPath2Data
        dict["numOfCentroidElementsMax"] = numOfCentroidElementsMax
        dict["numOfCentroidElementsMin"] = numOfCentroidElementsMin
        dict["numOfCentroids"] = len(centroidsDict['data']) - 1
        dict["finalAxesDict"] = finalAxesDict
        dict["allowedAxisLabelsDict"] = allowedAxisLabelsDict
        dict["defaultXLabel"] = defaultXLabel
        dict["defaultYLabel"] = defaultYLabel
        dict["defaultXLabelText"] = defaultXLabelText
        dict["defaultYLabelText"] = defaultYLabelText
        dict["valueKeyMaps"] = json.dumps(valueKeyMaps)
        dict["fileAppendix"] = cluster_id_base
        dict["dataSourceLst"] = dataSourceLst
        dict["dataSourceLstSelected"] = dataSourceLstSelected

        content = self.conf.Template(filename='templates/te_kmeans.tpl')
        return content.render(data=dict)

    def tenderStreamStory(self):
        '''
        function returns stream story page

        :return: string, html format
        '''

        import models.FVcustomization as FVC
        viewModel = FVC.FVcustomization(self.conf, self.getVars)
        return viewModel.getView()
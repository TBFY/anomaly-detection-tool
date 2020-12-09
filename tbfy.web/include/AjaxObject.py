'''
central object for executing ajax requests
'''

class AjaxObject:

    def __init__(self, config, fs):
        self.conf = config

        self.inputData = {}
        for k in fs.keys():
            self.inputData[k] = fs.getvalue(k)

        self.response = {}
        self.response['success'] = True
        self.response['message'] = 'Message not generated'
        self.response['inputData'] = self.inputData
        #self.response['outputData'] = []

    def executeMethod(self):
        if self.inputData['action'] == 'dTree':
            self.returnDecisionTree()
        if self.inputData['action'] == 'clustering':
            self.returnCustomClusters()
        if self.inputData['action'] == 'clustering-id':
            self.returnCustomClustersId()
        if self.inputData['action'] == 'clustering-id-exists':
            self.doesClusterExist()
        if self.inputData['action'] == 'retunFFGorupIds':
            self.returnSelectedGroupIds()
        else:
            self.executeTest()

    def executeTest(self):
        self.response['message'] = 'Test executed successfully'

    def returnSelectedGroupIds(self):
        '''
        function returns a joined list of comapny IDs selected based on group identifier;
        group identifier is submitted under self.inputData['groupName'];
        example of a group identifier "Schools" / "Šole" (which retirns all school IDs)

        :return: ajax object
        '''

        # create sql abbreviations
        # create sql abbreviations

        sql = self.conf.cDB.sql
        cur = self.conf.cDB.db.cursor()
        shared = self.conf.sharedCommon

        # get group IDs
        # get group IDs

        groupValue = str(self.inputData['groupName'])
        queryBase = "select {} from {} where {} = %s"
        queryString = sql.SQL(queryBase).format(
            sql.Identifier('maticna'),
            sql.Identifier('su_rpu'),
            sql.Identifier('kategorija'))
        cur.execute(queryString, (groupValue,))
        #print(queryString.as_string(cur))
        contracts = shared.returnSqlDataInDictFormat(cur)

        maticneList = []
        for row in contracts:
            maticneList.append(row['maticna'])

        self.response['ids'] = ','.join(maticneList)

    # START custom clustering functions
    # START custom clustering functions

    def returnCustomClustersId(self):
        '''
        function, retirns file appendix id

         :return: 0
         '''

        # get parameters
        # get parameters

        parameters = []
        for par in self.inputData['parameters[]']:
            parameters.append(par)

        clusterNum = int(self.inputData['clusterNum'])
        if clusterNum != -1:
            if clusterNum < 2:
                clusterNum = 10

        selectedDataset = self.inputData['selectedDataset'].lower()

        self.response['clusterID'] = self.getClusteringFileAppendixString(parameters, clusterNum, selectedDataset)

        return

    def doesClusterExist(self):
        '''
        function, checks whether cluster with given ID exists

         :return: boolean
         '''

        # get file name
        # get file name

        clusterID = self.inputData['clusterID']
        fullFileName = self.conf.publicTenderDataRoot + "kMeans/centroids-coordinates-" + clusterID + '.tsv'

        # file exists?
        # file exists?

        self.response['clusterID'] = self.inputData['clusterID']
        if self.conf.os.path.isfile(fullFileName):
            self.response['clusterExists'] = 1
        else:
            self.response['clusterExists'] = 0

        return

    def returnCustomClusters(self):
        '''
        function, based on received list of parameters, creates a custom decision tree graph

         :return: 0
         '''

        self.response['message'] = 'Clustering data.'

        # get parameters
        # get parameters

        parameters = []
        for par in self.inputData['parameters[]']:
            parameters.append(par)

        clusterNum = int(self.inputData['clusterNum'])
        if clusterNum != -1:
            if clusterNum < 2:
                clusterNum = 10

        selectedDataset = self.inputData['selectedDataset'].lower()

        fileAppendixString = self.getClusteringFileAppendixString(parameters, clusterNum, selectedDataset)

        # return file extension name
        # return file extension name

        self.response['fileAppendixString'] = fileAppendixString

        # return selected x and y axes
        # return selected x and y axes

        defaultXLabel = 'Narocnik_Velik_RS'
        if defaultXLabel in parameters:
            self.response['x_projection_val'] = defaultXLabel
        else:
            self.response['x_projection_val'] = parameters[0]

        defaultYLabel = 'KoncnaVrednost'
        if defaultYLabel in parameters:
            self.response['y_projection_val'] = defaultYLabel
            # avoid duplicate selection
            if self.response['x_projection_val'] == self.response['y_projection_val']:
                self.response['x_projection_val'] = parameters[1]
        else:
            self.response['y_projection_val'] = parameters[1]
            # avoid duplicate selection
            if self.response['x_projection_val'] == self.response['y_projection_val']:
                self.response['y_projection_val'] = parameters[0]

        # check if decision tree already exists
        # check if decision tree already exists

        from pathlib import Path
        centroidCoordinatesFile = Path(self.conf.publicTenderDataRoot + "kMeans/centroids-coordinates-" + fileAppendixString + '.tsv')
        if centroidCoordinatesFile.is_file():
            return

        # crete decision tree graph
        # crete decision tree graph

        self.createCustomClusters(fileAppendixString, parameters, clusterNum, selectedDataset)

        return

    def getClusteringFileAppendixString(self, nameParameters, clusterNum, selectedDataset):
        '''
        function gets in a list of parameters, assembles it in unique way and returns a unique string

        :param nameParameters: parameters defining final name graph image name
        :param clusterNum: number of clusters
        :return:
        '''

        from datetime import date
        today = date.today()

        # parameters are sorted in order to return always the same name
        # parameters are sorted in order to return always the same name

        nameParameters.sort()

        # create parameters string name
        # create parameters string name

        returnString = selectedDataset + '-' + today.strftime("%d/%m/%Y") + '-' + str(clusterNum)
        for param in nameParameters:
            returnString = param + '-' + returnString

        # return md5 hash
        # return md5 hash

        import hashlib
        return hashlib.md5(returnString.encode('utf-8')).hexdigest()

    def createCustomClusters(self, fileAppendixString, parameters, clusterNum, selectedDataset):
        '''
        function calculates clusters according input parameters

        :param fileAppendixString: the appendix to file name string
        :param parameters: parameters to be considered in analysis
        :param clusterNum: number of clusters
        :return: None
        '''

        # configure cluster creation
        # configure cluster creation

        statsConfig = {}

        if selectedDataset == 'si-ministry':
            statsConfig['dataSourceFilePath'] = self.conf.sourceFFTenderDataRoot + 'fullFeatureVectors/'
            statsConfig['dataSourceFileName'] = 'feature-vectors.tsv'
        else:
            statsConfig['dataSourceFilePath'] = self.conf.sourceKGFFTenderDataRoot
            statsConfig['dataSourceFileName'] = selectedDataset + '-tbfy-kg-fullfv-aggregated.tsv'

            # abort operation if file does not exist
            # abort operation if file does not exist

            tmp_fullFileName = statsConfig['dataSourceFilePath'] + statsConfig['dataSourceFileName']
            if not self.conf.os.path.isfile(tmp_fullFileName):
                return None

        statsConfig['dataStorageFilePath'] = self.conf.publicTenderDataRoot + 'kMeans/'
        statsConfig['selectedDataset'] = selectedDataset
        # parameters to generate clustering with definite number of clusters and save results to a specific file
        statsConfig['numOfClusters'] = clusterNum
        statsConfig['fileAppendix'] = '-' + fileAppendixString
        statsConfig['includeFieldsList'] = parameters

        # import all necessary files
        # import all necessary files

        import config_analysis
        import SharedAnalysisMethods
        sharedMethods = SharedAnalysisMethods.SharedAnalysisMethods(config_analysis)

        # cluster
        # cluster

        import KMeansTendersClass as KMeans

        stats = KMeans.KMeansTendersClass(config_analysis, sharedMethods)
        stats.readDataFile(statsConfig)
        stats.analyseClusterTenderVectors()

        return

    # STOP custom clustering functions
    # STOP custom clustering functions


    # START decision tree functions
    # START decision tree functions

    def returnDecisionTree(self):
        '''
        function, based on received list of parameters, creates a custom decision tree graph

        :return: 0
        '''

        self.response['message'] = 'Tree generation.'

        # get parameters
        # get parameters

        parameters = []
        for par in self.inputData['parameters[]']:
            parameters.append(par)

        treeDepth = self.inputData['treeDepth']
        if treeDepth == '0':
            treeDepth = '-1'

        fileNameBase = self.getDTreeImageFileName(parameters, treeDepth)
        fileNameImage = fileNameBase + ".png"

        # return image name
        # return image name

        self.response['fileNameBase'] = fileNameBase
        self.response['fileNameImage'] = fileNameImage

        # check if decision tree already exists
        # check if decision tree already exists

        from pathlib import Path
        dTreeGraphFile = Path(self.conf.publicTenderDataRoot + "dTree/" + fileNameImage)
        if dTreeGraphFile.is_file():
            return

        # crete decision tree graph
        # crete decision tree graph

        self.createCustomDecisionTreeGraph(fileNameBase, parameters, treeDepth)

        return

    def getDTreeImageFileName(self, nameParameters, treeDepth):
        '''
        function gets in a list of parameters, assembles it in unique way and returns a unique graph file name

        :param nameParameters: parameters defining final name graph image name
        :return:
        '''

        from datetime import date
        today = date.today()

        # parameters are sorted in order to return always the same name
        # parameters are sorted in order to return always the same name

        nameParameters.sort()

        # create parameters string name
        # create parameters string name

        fileNameImage = today.strftime("%d/%m/%Y") + treeDepth
        for param in nameParameters:
            fileNameImage = param + fileNameImage

        # return md5 hash
        # return md5 hash

        import hashlib
        return hashlib.md5(fileNameImage.encode('utf-8')).hexdigest()

    def createCustomDecisionTreeGraph(self, fileNameImage, parameters, treeDepth):

        dTreeConfig = {}
        dTreeConfig['dataSourceFilePath'] = self.conf.sourceFFTenderDataRoot + 'fullFeatureVectors/'
        dTreeConfig['dataSourceFileName'] = 'feature-vectors.tsv'
        dTreeConfig['dataStorageFilePath'] = self.conf.publicTenderDataRoot + 'dTree/'
        dTreeConfig['dataStorageFileName'] = fileNameImage
        dTreeConfig['criterion'] = 'gini'  # valid params == entropy, gini
        dTreeConfig['max_depth'] = int(treeDepth)  # -1 denotes no max depth
        dTreeConfig['test_data_sample'] = 0.7  # defines number od test samples => 1 - test_sample == train_sample  //  e.g. if test_data_sample == 0.4 => train_data_sample == 1 - 0.4 = 0.7

        # define data to include
        # define data to include

        import config_analysis
        import SharedAnalysisMethods
        sharedAnalysisMethods = SharedAnalysisMethods.SharedAnalysisMethods()

        dTreeConfig['features2include'] = parameters
        dTreeConfig['features2explore'] = 'StPrejetihPonudb'

        # build tree
        # build tree

        import publicTendersAnalysis.DecisionTreeClass as DTree

        decisionTree = DTree.DecisionTreeClass(config_analysis, sharedAnalysisMethods)
        decisionTree.createDecisionTree(dTreeConfig)

        # print decision tree prediction accuracy
        # print decision tree prediction accuracy

        self.response['decision_tree_accuracy'] = decisionTree.prediction_accuracy

        return

    # STOP decision tree functions
    # STOP decision tree functions
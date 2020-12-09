
# enabling shell exec from any directory
# enabling shell exec from any directory

import os
workingDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../')

import sys
sys.path.append(workingDir)

# import config
# import config

import config_analysis as conf

# import shared modules
# import shared modules

conf.sys.path.append(conf.os.path.join(conf.os.path.dirname(__file__), '../../'))
import SharedAnalysisMethods
sharedMethods = SharedAnalysisMethods.SharedAnalysisMethods(conf)

import SharedTenderDataMethods
sharedTenderMethods = SharedTenderDataMethods.SharedTenderDataMethods(conf)

# for testing purposes to turn on/off specific tasks
# for testing purposes to turn on/off specific tasks

exe_task_dTree = True
exe_task_ratio = True
exe_task_distr = True
exe_task_clstr = True
exe_task_relat = True
exe_cmmn_anmly = True


############################################
############################################
##   ANALYSIS 1: decision tree approach   ##
##   ANALYSIS 1: decision tree approach   ##
##   ANALYSIS 1: decision tree approach   ##
############################################
############################################


if exe_task_dTree:
    print('')
    print('Starting decision tree analysis.')

    dTreeConfig = {}
    dTreeConfig['dataSourceFilePath'] = conf.tenderDataFVPath
    dTreeConfig['dataSourceFileName'] = 'feature-vectors.tsv'
    dTreeConfig['dataStorageFilePath'] = conf.tenderDataResultsPath + 'dTree/'
    dTreeConfig['dataStorageFileName'] = 'dt_schema'
    dTreeConfig['criterion'] = 'gini' # valid params == entropy, gini
    dTreeConfig['max_depth'] = 8 # -1 denotes no max depth
    dTreeConfig['test_data_sample'] = 0.7 # defines number od test samples => 1 - test_sample == train_sample  //  e.g. if test_data_sample == 0.4 => train_data_sample == 1 - 0.4 = 0.7

    # define data to include; if one needs to specify which data to include, list fields in includedParametersList
    # define data to include; if one needs to specify which data to include, list fields in includedParametersList

    includedParametersList = []
    dTreeConfig['features2include'] = sharedTenderMethods.getTenderDataFieldKeysSelected(includedParametersList)
    #dTreeConfig['features2include'] = ["Narocnik_Velik_EU","Ponudnik_Velik_EU","SkupnaPonudba"]
    dTreeConfig['features2explore'] = 'StPrejetihPonudb'

    # build tree
    # build tree

    import DecisionTreeClass as DTree

    decisionTree = DTree.DecisionTreeClass(conf, sharedMethods)
    decisionTree.createDecisionTree(dTreeConfig)

    # print decision tree prediction accuracy
    # print decision tree prediction accuracy

    print("decision tree accuracy is: ", decisionTree.prediction_accuracy)


####################################################
####################################################
##   ANALYSIS 2: various statistical approaches   ##
##   ANALYSIS 2: various statistical approaches   ##
##   ANALYSIS 2: various statistical approaches   ##
####################################################
####################################################


if exe_task_ratio:
    print('')
    print('Starting ratio analysis.')

    import RatiosTendersClass as RatiosAnalysis

    # processing MJU data
    # processing MJU data

    # revenue per employee
    # revenue per employee

    ratiosConfig = {}
    ratiosConfig['dataSourceFilePath'] = conf.tenderDataFVPath
    ratiosConfig['dataSourceFileName'] = 'feature-vectors.tsv'
    ratiosConfig['dataStorageFilePath'] = conf.tenderDataResultsPath + 'ratios/'
    ratiosConfig['ratioCategoryDir'] = 'revenuePerEmployee'
    ratiosConfig['dataStorageFileName'] = 'si-ministry'
    ratiosConfig['dataSourceType'] = 'mju'
    ratiosConfig['fields2Store'] = {'x_val':'',
                                    'y_value':'',
                                    'buyerId':'NarocnikMaticna',
                                    'bidderId':'PonudnikMaticna',
                                    'tender_amount':'KoncnaVrednostSorazmerno',
                                    'bidder_employees': 'Ponudnik_Velik_EU',
                                    'cpv': 'CPV_glavni'}

    ratios = RatiosAnalysis.RatiosTendersClass(conf, sharedMethods)
    ratios.readDataFile(ratiosConfig)
    ratios.analyseSizeVsDealRatioByTender('NarocnikMaticna', 'PonudnikMaticna', 'KoncnaVrednostSorazmerno', 'Ponudnik_Velik_EU')

    # budget assesment
    # budget assesment

    ratiosConfig = {}
    ratiosConfig['dataSourceFilePath'] = conf.tenderDataFVPath
    ratiosConfig['dataSourceFileName'] = 'feature-vectors.tsv'
    ratiosConfig['dataStorageFilePath'] = conf.tenderDataResultsPath + 'ratios/'
    ratiosConfig['ratioCategoryDir'] = 'budgetAssessment'
    ratiosConfig['dataStorageFileName'] = 'si-ministry'
    ratiosConfig['dataSourceType'] = 'mju'
    ratiosConfig['fields2Store'] = {'x_val':'',
                                    'y_value':'',
                                    'buyerId':'NarocnikMaticna',
                                    'bidderId':'PonudnikMaticna',
                                    'tender_assessed': 'OcenjenaVrednostSorazmerno',
                                    'tender_amount':'KoncnaVrednostSorazmerno',
                                    'cpv': 'CPV_glavni'}

    ratios = RatiosAnalysis.RatiosTendersClass(conf, sharedMethods)
    ratios.readDataFile(ratiosConfig)
    ratios.analyseSizeVsDealRatioByTender('NarocnikMaticna', 'PonudnikMaticna', 'OcenjenaVrednostSorazmerno', 'KoncnaVrednostSorazmerno')

    # processing TBFY KG files: 1) find all files to process 2) process file by file
    # processing TBFY KG files: 1) find all files to process 2) process file by file

    allKGFiles = [f for f in conf.os.listdir(conf.tenderTbfyKGFVPath) if f.find('fullfv-aggregated.tsv') > 0]
    for fileName in allKGFiles:

        # get country name
        # get country name

        fileNamePieces = fileName.split('-tbfy-kg-')
        countryName = fileNamePieces[0]

        ratiosConfig = {}
        ratiosConfig['dataSourceFilePath'] = conf.tenderTbfyKGFVPath
        ratiosConfig['dataSourceFileName'] = fileName
        ratiosConfig['dataStorageFilePath'] = conf.tenderDataResultsPath + 'ratios/'
        ratiosConfig['ratioCategoryDir'] = 'revenuePerEmployee'
        ratiosConfig['dataStorageFileName'] = countryName
        ratiosConfig['dataSourceType'] = 'tbgy-kg'
        ratiosConfig['fields2Store'] = {'x_val': '',
                                        'y_value': '',
                                        'buyerId': 'award_id',
                                        'bidderId': 'supplier_company_id',
                                        'tender_amount': 'amount',
                                        'bidder_employees': 'supplier_num_employees',
                                        'cpv': 'cpv',
                                        'ocid': 'ocid',
                                        'currency': 'currency',
                                        'award_id': 'award_id',
                                        'supplier_jurisdiction': 'supplier_jurisdiction'}

        ratios = RatiosAnalysis.RatiosTendersClass(conf, sharedMethods)
        ratios.readDataFile(ratiosConfig)
        ratios.analyseSizeVsDealRatioByTender('award_id', 'supplier_company_id', 'amount', 'supplier_num_employees')


##############################################
##############################################
##   ANALYSIS 3: distribution comparisons   ##
##   ANALYSIS 3: distribution comparisons   ##
##   ANALYSIS 3: distribution comparisons   ##
##############################################
##############################################


if exe_task_distr:
    print('')
    print('Starting distribution analysis')

    import DistributionsTendersClass as DistributionsAnalysis

    # processing MJU data
    # processing MJU data

    # revenue per employee
    # revenue per employee

    distributionsConfig = {}
    distributionsConfig['dataSourceFilePath'] = conf.tenderDataFVPath
    distributionsConfig['dataSourceFileName'] = 'feature-vectors.tsv'
    distributionsConfig['dataStorageFilePath'] = conf.tenderDataResultsPath + 'distributions/'
    distributionsConfig['distributonCategoryDir'] = 'offersNum'
    distributionsConfig['dataStorageFileName'] = 'si-ministry-CPV'
    distributionsConfig['variableFieldName'] = 'StPrejetihPonudb'
    distributionsConfig['companyIdFieldName'] = 'PonudnikMaticna'
    distributionsConfig['cpvFieldName'] = 'CPV_glavni_2mesti'
    distributionsConfig['dataSourceType'] = 'mju'

    distributions = DistributionsAnalysis.DistributionsTendersClass(conf, sharedMethods)
    distributions.setAnalysisParameters(distributionsConfig)
    distributions.compareData2CommonDistribution()

    # estimated and final budged distribution
    # estimated and final budged distribution

    distributionsConfig = {}
    distributionsConfig['dataSourceFilePath'] = conf.tenderDataFVPath
    distributionsConfig['dataSourceFileName'] = 'feature-vectors.tsv'
    distributionsConfig['dataStorageFilePath'] = conf.tenderDataResultsPath + 'distributions/'
    distributionsConfig['distributonCategoryDir'] = 'budgetAssessment'
    distributionsConfig['dataStorageFileName'] = 'si-ministry-CPV'
    distributionsConfig['variableFieldName'] = 'OcenjenaVrednostSorazmerno,KoncnaVrednostSorazmerno'
    distributionsConfig['companyIdFieldName'] = 'PonudnikMaticna'
    distributionsConfig['cpvFieldName'] = 'CPV_glavni_2mesti'
    distributionsConfig['dataSourceType'] = 'mju'

    distributions = DistributionsAnalysis.DistributionsTendersClass(conf, sharedMethods)
    distributions.setAnalysisParameters(distributionsConfig)
    distributions.compareData2CommonDistribution()


#############################################
#############################################
##   ANALYSIS 4: kMeans cluster analysis   ##
##   ANALYSIS 4: kMeans cluster analysis   ##
##   ANALYSIS 4: kMeans cluster analysis   ##
#############################################
#############################################


if exe_task_clstr:
    print('')
    print('Starting cluster analysis')

    import KMeansTendersClass as KMeans

    statsConfig = {}
    statsConfig['dataSourceFilePath'] = conf.tenderDataFVPath
    statsConfig['dataSourceFileName'] = 'feature-vectors.tsv'
    statsConfig['dataStorageFilePath'] = conf.tenderDataResultsPath + 'kMeans/'
    statsConfig['selectedDataset'] = 'si-ministry'
    statsConfig['clearOldResults'] = True
    # parameters to generate clustering with definite number of clusters and save results to a specific file
    # statsConfig['numOfClusters'] = 3
    # statsConfig['fileAppendix'] = '-test'
    statsConfig['includeFieldsList'] = [
        'Narocnik_OBCINA',
        'Narocnik_Oblika',
        'Narocnik_Glavna_Dejavnost_SKD',
        'Narocnik_Velik_RS',
        'Narocnik_Velik_EU',
        'Narocnik_Regija',
        'Narocnik_Dejavnost',
        'VrstaNarocila',
        'VrstaPostopka',
        'VrstaPostopka_EU',
        'Merila',
        'OkvirniSporazum',
        'SkupnoNarocanje',
        'EUsredstva',
        'ObjavaVEU',
        'StPrejetihPonudb',
        'SkupnaPonudba',
        'OcenjenaVrednost',
        'KoncnaVrednost',
        'OddanoPodizvajalcem',
        'CPV_glavni_2mesti',
        'Podrocje',
        'VrstaPostopkaIzracunan',
        'NarocnikPostnaStevilka',
        'PonudnikPostnaStevilka',
        'Ponudnik_OBCINA',
        'Ponudnik_Velik_EU',
        'Ponudnik_Velik_RS',
        'OcenjenaVrednostSorazmerno',
        'KoncnaVrednostSorazmerno'
    ]

    stats = KMeans.KMeansTendersClass(conf, sharedMethods)
    stats.readDataFile(statsConfig)
    stats.analyseClusterTenderVectors()

    # processing TBFY KG files: 1) find all files to process 2) process file by file
    # processing TBFY KG files: 1) find all files to process 2) process file by file

    allKGFiles = [f for f in conf.os.listdir(conf.tenderTbfyKGFVPath) if f.find('fullfv-aggregated.tsv') > 0]
    for fileName in allKGFiles:

        # get country name
        # get country name

        fileNamePieces = fileName.split('-tbfy-kg-')
        countryName = fileNamePieces[0]

        # set config params
        # set config params

        statsConfig = {}
        statsConfig['dataSourceFilePath'] = conf.tenderTbfyKGFVPath
        statsConfig['dataSourceFileName'] = fileName
        statsConfig['dataStorageFilePath'] = conf.tenderDataResultsPath + 'kMeans/'
        statsConfig['selectedDataset'] = countryName

        # parameters to generate clustering with definite number of clusters and save results to a specific file
        # statsConfig['numOfClusters'] = 3
        # statsConfig['fileAppendix'] = '-test',
        statsConfig['includeFieldsList'] = [
            'cpv',
            'publishedOnTed',
            'amount',
            'currency',
            'buyerPostId',
            'buyerCountry',
            'supplierCountry',
            'awardCriteriaDetails',
            'supplier_num_employees',
            'supplier_jurisdiction',
            'supplier_postal_code'
        ]

        stats = KMeans.KMeansTendersClass(conf, sharedMethods)
        stats.readDataFile(statsConfig)
        stats.analyseClusterTenderVectors()


###################################################################
###################################################################
##   ANALYSIS 5: analysing relation between bidders and buyers   ##
##   ANALYSIS 5: analysing relation between bidders and buyers   ##
##   ANALYSIS 5: analysing relation between bidders and buyers   ##
###################################################################
###################################################################


if exe_task_relat:
    print('')
    print('Starting relation analysis between bidders and buyers')

    # bidder buyer relation analysis
    # bidder buyer relation analysis

    import BidderBuyerRelationTendersClass as BBRelationAnalysis

    # revenue per employee
    # revenue per employee

    bbRelationConfig = {}
    bbRelationConfig['dataSourceFilePath'] = conf.tenderDataFVPath
    bbRelationConfig['dataSourceFileName'] = 'feature-vectors.tsv'
    bbRelationConfig['dataStorageFilePath'] = conf.tenderDataResultsPath + 'relations_bb/'
    bbRelationConfig['dataStorageFileName'] = 'si-ministry-CPV'
    bbRelationConfig['variableFieldName'] = 'KoncnaVrednostSorazmerno'
    bbRelationConfig['buyerIdFieldName'] = 'NarocnikMaticna'
    bbRelationConfig['bidderIdFieldName'] = 'PonudnikMaticna'
    bbRelationConfig['cpvFieldName'] = 'CPV_glavni_2mesti'
    bbRelationConfig['dataSourceType'] = 'mju'


    bbRelation = BBRelationAnalysis.BidderBuyerRelationTendersClass(conf, sharedMethods)
    bbRelation.setAnalysisParameters(bbRelationConfig)
    bbRelation.calculateBidderBuyerRelations()
    bbRelation.saveAnomalies2File()


#############################################################################################
#############################################################################################
##   ANALYSIS MERGER: takes in all analysis results and creates a common anomaly measure   ##
##   ANALYSIS MERGER: takes in all analysis results and creates a common anomaly measure   ##
##   ANALYSIS MERGER: takes in all analysis results and creates a common anomaly measure   ##
#############################################################################################
#############################################################################################


if exe_cmmn_anmly:
    print('')
    print('Merging analysis results into a common anomaly measure')

    import CommonAnomalyMeasure as CommonMeasure

    commonMeasureConfig = {}
    commonMeasureConfig['anomalies2include'] = ['distributions.budget', 'distributions.offers', 'ratios.budget', 'ratios.revenue', 'relations']

    commonMesure = CommonMeasure.CommonAnomalyMeasure(conf, sharedMethods)
    commonMesure.configureAnalysis(commonMeasureConfig)
    commonMesure.readAnomlyValues()
    commonMesure.save2File()


# ending script
# ending script

print()
print("script execution time:")
print("--- %s seconds ---" % (conf.time.time() - conf.start_time))



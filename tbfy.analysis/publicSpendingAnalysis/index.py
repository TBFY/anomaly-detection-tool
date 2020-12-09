
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
sharedAnalysis = SharedAnalysisMethods.SharedAnalysisMethods(conf)

import SharedSpendingDataMethods
sharedSpendingMethods = SharedSpendingDataMethods.SharedSpendingDataMethods(conf)

# for testing purposes to turn on/off specific tasks
# for testing purposes to turn on/off specific tasks

testModeON         = False
exe_task_jensk     = True
exe_task_periods   = True
exe_task_derivs    = True
exe_task_cumul     = True


##########################################
##########################################
##   ANALYSIS 1: Jenks natural breaks   ##
##   ANALYSIS 1: Jenks natural breaks   ##
##   ANALYSIS 1: Jenks natural breaks   ##
##########################################
##########################################

if exe_task_jensk:
    print('')
    print('Starting 1D (Jenks) cluster analysis')

    # Jenks natural breaks optimization analysis
    # Jenks natural breaks optimization analysis

    import JenksNBAnomaliesClass as JNBAC

    jenksAnomalies = JNBAC.JenksNBAnomaliesClass(conf, sharedSpendingMethods)
    jenksAnomalies.dataSourceFilePath = conf.spendingDataFormattedPath + 'erarFeatureVectors/'
    jenksAnomalies.dataSourceFileName = 'ts-trans-months.csv'
    jenksAnomalies.sharedAnalysis = sharedAnalysis
    jenksAnomalies.findAnomaliesThroughJenksNaturalBreaks()
    jenksAnomalies.saveAnomalies2File()


#########################################
#########################################
##   ANALYSIS 2: Analysis of periods   ##
##   ANALYSIS 2: Analysis of periods   ##
##   ANALYSIS 2: Analysis of periods   ##
#########################################
#########################################

if exe_task_periods:
    print('')
    print('Starting periods analysis')

    import PeriodsAnomalyClass as PeriodsAC

    periodsAnomalies = PeriodsAC.PeriodsAnomalyClass(conf, sharedSpendingMethods)
    periodsAnomalies.dataSourceFilePath = conf.spendingDataFormattedPath + 'erarFeatureVectors/'
    periodsAnomalies.dataSourceFileName = 'ts-trans-months.csv'
    periodsAnomalies.sharedAnalysis = sharedAnalysis
    if testModeON:
        periodsAnomalies.test_limit_rows = 10000
        periodsAnomalies._breaks_activation_window_size = 2
    periodsAnomalies.findAnomaliesThroughPeriodMargin()
    periodsAnomalies.saveAnomalies2File()


#############################################
#############################################
##   ANALYSIS 3: Analysis of derivatives   ##
##   ANALYSIS 3: Analysis of derivatives   ##
##   ANALYSIS 3: Analysis of derivatives   ##
#############################################
#############################################

if exe_task_derivs:
    print('')
    print('Starting derivatives analysis')

    import DerivativesAnomalyClass as DerAC

    derivAnomalies = DerAC.DerivativesAnomalyClass(conf, sharedSpendingMethods)
    derivAnomalies.dataSourceFilePath = conf.spendingDataFormattedPath + 'erarFeatureVectors/'
    derivAnomalies.dataSourceFileName = 'ts-trans-months.csv'
    derivAnomalies.sharedAnalysis = sharedAnalysis
    if testModeON:
        derivAnomalies.test_limit_rows = 10000
        derivAnomalies.plotSingleDerivativesGraph = True
    derivAnomalies.findAnomaliesThroughDerivatives()
    derivAnomalies.saveAnomalies2File()


#############################################
#############################################
##   ANALYSIS 4: Analysis of derivatives   ##
##   ANALYSIS 4: Analysis of derivatives   ##
##   ANALYSIS 4: Analysis of derivatives   ##
#############################################
#############################################

if exe_task_cumul:
    print('')
    print('Starting partial cumulative analysis')

    import PartialCumulativeClass as ParCumAC

    partialAnomalies = ParCumAC.PartialCumulativeClass(conf, sharedSpendingMethods)
    partialAnomalies.dataSourceFilePath = conf.spendingDataFormattedPath + 'erarFeatureVectors/'
    partialAnomalies.dataSourceFileName = 'ts-trans-months.csv'
    partialAnomalies.sharedAnalysis = sharedAnalysis
    if testModeON:
        partialAnomalies.test_limit_rows = 100000
    partialAnomalies.findAnomaliesThroughPartialCumulation()
    partialAnomalies.saveAnomalies2File()

# ending script
# ending script

print('')
print('script execution time:')
print('--- %s seconds ---' % (conf.time.time() - conf.start_time))
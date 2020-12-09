
# import libraries
# import libraries

import sys
import os
import time
import json
import io
import datetime

# define base paths
# define base paths

baseUrl                     = 'http://local.tbfy/'
baseRoot                    = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../')

# define include paths
# define include paths

sys.path.append(os.path.join(baseRoot))

# import common files
# import common files

import configMJU_hidden as MJUhidden
import configDB as cDB
import SharedCommonMethods

# init modules
# init modules

sharedCommon = SharedCommonMethods.SharedCommonMethods()

# define os specific particularities
# define os specific particularities

datetimeLeadingZeroRemovalChar = '-'

# vars for converting mju raw data into ocds format
# vars for converting mju raw data into ocds format

tenderDataRawPath             = baseRoot + 'tbfy.data/data/rawData/tenderRawData/'
tenderDataOCDSFormatPath      = baseRoot + 'tbfy.data/data/OCDSdata/'

tenderMethodsPath             = baseRoot + 'tbfy.data/tenderDataProcessing/'
transactionsMethodsPath       = baseRoot + 'tbfy.data/transactionsDataProcessing/'

# vars for converting mju raw data into feature vectors
# vars for converting mju raw data into feature vectors

featureVectorRawPath          = baseRoot + 'tbfy.data/data/rawData/tenderRawData/'

fullFeatureVectorFormatPath   = baseRoot + 'tbfy.data/data/tenderFeatureVectors/fullFeatureVectors/'
ssFeatureVectorFormatPath     = baseRoot + 'tbfy.data/data/tenderFeatureVectors/SSFeatureVectors/'
featureVectorMapPath          = baseRoot + 'tbfy.data/data/tenderFeatureVectors/mappings/'

erarDataRawPath               = baseRoot + 'tbfy.data/data/rawData/spendingRawData/erarRawData/'
erarFeatureVectorsDataPath    = baseRoot + 'tbfy.data/data/erarFeatureVectors/'

tbfyKGRawDataPath             = baseRoot + 'tbfy.data/data/rawData/tbfyKG/'
tbfyKGFeatureVectorsDataPath  = baseRoot + 'tbfy.data/data/tbfyKGFV/'
tbfyKGFeatureVectorMapPath    = baseRoot + 'tbfy.data/data/tbfyKGFV/mappings/'

# script execution time
# script execution time

start_time = time.time()

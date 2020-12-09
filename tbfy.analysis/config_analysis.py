
# import libraries
# import libraries

import sys
import os
import time
import matplotlib.pyplot as plt
import numpy
import statistics

# define base path
# define base path

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

# tender paths
# tender paths

tenderDataFVPath            = baseRoot + "tbfy.analysis/data/data_source/tenderFeatureVectors/fullFeatureVectors/"
tenderTbfyKGFVPath          = baseRoot + "tbfy.analysis/data/data_source/tbfyKGFV/"
tenderDataResultsPath       = baseRoot + "tbfy.analysis/data/data_results/publicTenders/"

# spending paths
# spending paths

spendingDataRawPath         = baseRoot + "tbfy.analysis/data/data_source/rawData/"
spendingDataFormattedPath   = baseRoot + "tbfy.analysis/data/data_source/"
transactionsDataResultsPath = baseRoot + "tbfy.analysis/data/data_results/publicSpending/"

# default configurations
# default configurations

plt.figure(figsize=(8, 6))
plt.style.use('seaborn-poster')

# script execution time
# script execution time

start_time = time.time()


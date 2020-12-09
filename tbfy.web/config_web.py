
# import libraries
# import libraries

import sys
import os
import _locale
import urllib

from mako.template import Template
import re

# this hack forces utf8 encoding in Windows environment and prevents "UnicodeEncodeError" issues
# this hack forces utf8 encoding in Windows environment and prevents "UnicodeEncodeError" issues

_locale._getdefaultlocale = (lambda *args: ['en_US', 'utf_8_sig'])
#print(locale.getpreferredencoding())
#print(conf.sys.getfilesystemencoding())

# define base paths
# define base paths

urlHost                     = 'http://local.tbfy/'
baseRoot                    = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../')

# define include paths
# define include paths

sys.path.append(os.path.join(baseRoot))
sys.path.append(os.path.join(baseRoot, 'tbfy.web/include'))
sys.path.append(os.path.join(baseRoot, 'tbfy.analysis'))
sys.path.append(os.path.join(baseRoot, 'tbfy.analysis/publicSpendingAnalysis'))
sys.path.append(os.path.join(baseRoot, 'tbfy.analysis/publicTendersAnalysis'))

# import common files
# import common files

import configDB as cDB
import SharedCommonMethods

# init modules
# init modules

sharedCommon = SharedCommonMethods.SharedCommonMethods()

# define variables
# define variables

publicTenderDataUrl       = "/data_results/publicTenders/"
publicTenderDataRoot      = baseRoot + "tbfy.web/data_results/publicTenders/"
publicSpendingDataUrl     = "/data_results/publicSpending/"
publicSpendingDataRoot    = baseRoot + "tbfy.web/data_results/publicSpending/"

sourceFFTenderDataRoot    = baseRoot + "tbfy.data/data/tenderFeatureVectors/"
sourceKGFFTenderDataRoot  = baseRoot + "tbfy.data/data/tbfyKGFV/"
sourceSpendingDataRoot    = baseRoot + "tbfy.analysis/data/formattedData/"

featureVectorMapPath      = baseRoot + 'tbfy.data/data/tenderFeatureVectors/mappings/'

# import local libraries
# import local libraries

import TbfyController as Tbfy
import SharedWebMethods

sharedMethods = SharedWebMethods.SharedWebMethods()
sharedMethods.cDB = cDB
sharedMethods.sharedCommon = sharedCommon



# enabling shell exec from any directory
# enabling shell exec from any directory

import os
workingDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../')

import sys
sys.path.append(workingDir)

# run tender data processing
# run tender data processing

localPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'publicTendersAnalysis')
sys.path.append(localPath)
import publicTendersAnalysis.index

# run transactions data processing
# run transactions data processing

localPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'publicSpendingAnalysis')
sys.path.append(localPath)
import publicSpendingAnalysis.index
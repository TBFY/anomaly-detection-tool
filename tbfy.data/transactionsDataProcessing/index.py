
# enabling shell exec from any directory
# enabling shell exec from any directory

import os
workingDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../')

import sys
sys.path.append(workingDir)

# configure params
# configure params

import config_data as conf
import SharedDataMethods as Shared

sharedMethods = Shared.SharedDataMethods(conf)

# for testing purposes to turn on/off specific tasks
# for testing purposes to turn on/off specific tasks

testModeON         = False
exe_task_download  = True
exe_task_erar2FV   = True
exe_task_transSer  = True

# run script
# run script

# ******************************************************************** #
# ******************************************************************** #
# *********** download Erar transactions data to localhost *********** #
# *********** download Erar transactions data to localhost *********** #
# ******************************************************************** #
# ******************************************************************** #

if exe_task_download:
    print("")
    print("Erar Data transfer to IJS: start")

    import DownloadErarData2Localhost as Erar2Lh

    dataDL = Erar2Lh.DownloadErarData2Localhost(conf, sharedMethods)
    dataDL.downloadLastAvailableErarDataDump()

# ************************************************************ #
# ************************************************************ #
# *********** raw Erar data 2 FV format conversion *********** #
# *********** raw Erar data 2 FV format conversion *********** #
# ************************************************************ #
# ************************************************************ #

if exe_task_erar2FV:
    print("")
    print("Erar Data conversion into FV format: start")

    import ErarData2FVConversion as ED2FV

    convertErarTransactions2FV = ED2FV.ErarData2FVConversion(conf, sharedMethods)
    convertErarTransactions2FV.convertRawData2FV()

# ************************************************************ #
# ************************************************************ #
# *********** raw Erar data 2 FV format conversion *********** #
# *********** raw Erar data 2 FV format conversion *********** #
# ************************************************************ #
# ************************************************************ #

if exe_task_transSer:
    print("")
    print("Erar FV file to transactions time series conversion: start")

    import ErarFV2TransTimeSeries as EFV2TS

    timeSeries = EFV2TS.ErarFV2TransTimeSeries(conf, sharedMethods)
    if testModeON:
        timeSeries.rawDataLimit = 1000000
    timeSeries.convertFV2TimeSeries()

# ending script
# ending script

print("")
print("script execution time:")
print("--- %s seconds ---" % (conf.time.time() - conf.start_time))


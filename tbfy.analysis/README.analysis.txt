This scripts are part of TBFY project. TBFY project is divided into three layers:
(*) tbfy.data
(*) tbfy.analysis
(*) tbfy.web

Every TBFY layer has a more detailed description available in its own README.xxx.txt located in its base directory. This README.txt file is describing the role of "tbfy.analysis" scripts.

Scrips in "tbfy.analysis" are responsible for:
(*) analysis of public spending data
(*) analysis of public tenders data

Every analysis is written as an independent module. In such a way, not only analysis script can be reused, but whole analysis tool can be easily expended with new approaches. Preprocessed data are available in "data/data_source", while analysis results are stored in "data/data_results".

[AUTOMATIZATION]

Processes are automated through cronjob_data.py script. Script is run once per day (during the night) and it analyses data, prepocessed by tbfy.data.
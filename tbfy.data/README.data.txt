This scripts are part of TBFY project. TBFY project is divided into three layers:
(*) tbfy.data
(*) tbfy.analysis
(*) tbfy.web

Every TBFY layer has a more detailed description available in its own README.xxx.txt located in its base directory. This README.data.txt file is describing the role of "tbfy.data" scripts.

Scrips in "tbfy.data" are responsible for:
(*) data aggregation and
(*) data processing in order to be ready for later analysis.


[DATA AGGREGATION]

All data are stored in "data/rawData" directory. Three sources are currently being explotied:
(*) erar data: this are publicly available data encompassing all transactions that happend between Slovenian public entities and any other entities;
(*) MJU data: this are data provided by Slovenian ministry of public procurement and encompass all data related to public procurement processes;
(*) TBFY knowledge graph: this are data downloaded from the TBFY knowledge graph, which is an aggregation of public procurements from all over the world.

Data are then stored in:
(*) erar data in "data/rawData/spendingRawData"
(*) MJU data in "data/rawData/tenderRawData"
(*) TBFY knowledge graph in "data/rawData/tbfyKG"


[DATA PREPROCESSING]

After being downloaded, raw data are preprocessed in a form, required by analysis scripts. Data are preprocessed in various formats:
(*) erar data are converted into feature vectors and are available in "data/erarFeatureVectors"
(*) MJU data are converted in ocds format (https://www.open-contracting.org/) and are available in "data/OCDSdata"
(*) tbfy knowledge graph data are converted into feature vectors and are available in "data/tbfyKGFV"
(*) MJU data are converted into feature vectors and available in "data/tenderFeatureVectors".

MJU data are converted in two slightly different formats:
(*) for a later analysis, MJU data are converted into feature vectors and available in "data/tenderFeatureVectors/fullFeatureVectors"
(*) for a StreamStory tool, MJU data are converted into feature vectors adapted to Stream Story requirements and are available in "data/tenderFeatureVectors/SSFeatureVectors".


[AUTOMATIZATION]

Processes are automated through cronjob_data.py script. Script is run once per day (during the night) and it downloads and preprocesses all newly appeared data.


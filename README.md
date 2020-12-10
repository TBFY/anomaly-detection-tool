<p align="center"><img width=50% src="https://github.com/TBFY/general/blob/master/figures/tbfy-logo.png"></p>

[![License](https://img.shields.io/badge/license-Apache2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)


# Basic Overview

Code, available here, is the TBFY anomaly detection tool, powering http://tbfy.ijs.si/ The TBFY anomaly detection tool is part of the TBFY platform, described in more detail here: https://theybuyforyou.eu/ The goal of the TBFY anomaly detection tool is to identify anomalies within the public procurement processes.

The TBFY anomaly tool is composed of three layers:
- data processing, available in tbfy.data;
- data analysis, available in tbfy.analysis;
- results interface, available in tbfy.web.

Each of the layers is processed independently from other layers, which means that in order to execute a script within a given layer, no other scripts from other layers need to be run. However, the logic behind the three layers expects, that one:
- first executes tbfy.data, which in priciple downloads and transforms data into a format required by the analysis;
- then executes tbfy.analysis, which analyses data;
- and then runs a web application, tbfy.web, where results are presented in human readable format.


# Anomaly detection architecture

This chapter describes the three anomaly detecion layers in more detail.


## Data processing (tbfy.data)

Scrips in tbfy.data are responsible for:
- data aggregation and
- data processing in required format for later analysis.


### Data aggregation

All data are stored in "data/rawData" directory. Three sources are currently being exploited:
- erar data: this are publicly available data encompassing all transactions between Slovenian public entities and any other entities;
- MJU data: this are data provided by Slovenian ministry of public procurement and encompass all data related to public procurement processes in Slovenia;
- TBFY knowledge graph: this are data downloaded from the TBFY knowledge graph, which is a data aggregator over public procurements from all over the world.

Data are then stored in:
- erar data in "data/rawData/spendingRawData";
- MJU data in "data/rawData/tenderRawData";
- TBFY knowledge graph in "data/rawData/tbfyKG".


### Data preprocessing

After being downloaded, raw data are preprocessed in a form, required by analysis scripts. Data are preprocessed in various formats:
- erar data are converted into feature vectors and are available in "data/erarFeatureVectors";
- MJU data are converted in ocds format (https://www.open-contracting.org/) and are available in "data/OCDSdata";
- TBFY knowledge graph data are converted into feature vectors and are available in "data/tbfyKGFV";
- MJU data are converted into feature vectors and available in "data/tenderFeatureVectors".

MJU data are converted in two slightly different formats:
- for a later analysis, MJU data are converted into feature vectors and available in "data/tenderFeatureVectors/fullFeatureVectors";
- for a StreamStory tool, MJU data are converted into feature vectors adapted to Stream Story requirements and are available in "data/tenderFeatureVectors/SSFeatureVectors".


### Process automation

Processes are automated through cronjob_data.py script. Script is run once per day (during the night) and it downloads and preprocesses all newly appeared data.


## Data analysis (tbfy.analysis)

Scrips in tbfy.analysis are responsible for:
- analysis of public spending data;
- analysis of public tenders data.

Every analysis is written as an independent module. In such a way, not only analysis script can be reused, but whole analysis tool can be easily expended with new approaches. Preprocessed data are available in "tbfy.analysis/data/data_source", while analysis results are stored in "tbfy.analysis/data/data_results".


### Process automation

Processes are automated through cronjob_data.py script. Script is run once per day (during the night) and it analyses data, preprocessed by tbfy.data layer.


### Adding new analysis module

New modules can be aded to:
- tbfy.analysis/publicSpendingAnalysis if analysing erar spending data;
- tbfy.analysis/publicTendersAnalysis if analysing public procurement data;

The analysis is included through index.py file:
- tbfy.analysis/publicSpendingAnalysis/index.py or
- tbfy.analysis/publicTendersAnalysis/index.py
By including analysis in index.py, the porcess is instantly automated and is periodically executed (once per day for procurement analysis, once per week for spending analysis).

Analysis results are stored in:
- tbfy.analysis/data/data_results/publicSpending/ANALYSIS-ASSOCIATED-DIR for spending analysis;
- tbfy.analysis/data/data_results/publicTenders/ANALYSIS-ASSOCIATED-DIR for procurement analysis.
The tbfy.web, when servign analysis results, pulls results directly from above mentioned directories. 


## Results display (tbfy.web)

The role of the tbfy.web layer is to serve analysis results in a human readable format. This is done through http protocol in a form of webpage.

The HTML is created first by being:
- modelled in tbfy.web/include/models
- and, with the help of mako template library, joined with a selected template in tbfy.web/templates.


# Technical specifications

All of the three layers of the TBFY anomaly detection tool is run by a python 3.7 interpreter. Python requires additional libraries to be installed:

- mako 1.1.3
- psycopg2-binary 2.8.6
- matplotlib 3.1.3
- pandas 1.0.1
- sklearn
- sklearn-json 0.1.0
- scikit-learn 0.22.1
- IPython 7.12.0
- pydotplus 2.0.2
- GraphViz 0.13.2
- jenkspy 0.1.5
- requests 2.24.0


# Installation specifications

Every of the three layers have an associated config file, that needs to be adapted to a local environment:
- tbfy.data/config_data.py
- tbfy.analysis/config_analysis.py
- tbfy.web/config_web.py

Every of the three layers are provided with additional installation instructions:
- tbfy.data/INSTALL.data.txt
- tbfy.analysis/INSTALL.analysis.txt
- tbfy.web/INSTALL.web.txt


# Script execution

Once the installation process is over, it's time for execution.

Data aggregation is executed by running:
- data preprocess for spending data: tbfy.data/transactionsDataProcessing/index.py
- data preprocess for tender data: tbfy.data/tenderDataProcessing/index.py

Data analysis is executed by running:
- data analysis of spending data: tbfy.analysis/publicSpendingAnalysis/index.py
- data analysis of tender data: tbfy.analysis/publicTendersAnalysis/index.py

Every index.py, at the beginning of the file, has several switches, enabling or disabling a specific part of the code. For example, due to lack of credentials to connect to MJU server, one can turn off MJU data download by setting exe_task_mju_download to False


# Contributing

Please take a look at our [contributing](https://github.com/TBFY/general/blob/master/guides/how-to-contribute.md) guidelines if you're interested in helping!


# MISC

## graphWix installation

Python's graphwiz library does not come with the actual executable. Which is why one needs to install it on its own:

- install graphviz (https://graphviz.org/download/);
- update global path to graphwiz executable.


## MJU password

For security reasons the MJU (Slovenian ministry of public procurement) credentials for a ftp connect to MJU servers are not provided.









#!/Users/matej/PycharmProjects/tbfy/venv3.7/bin/python
# -*- coding: utf-8 -*-#

# import ajax specific libraries
# import ajax specific libraries

import sys
import json
import cgi

# get access to project libs and vars
# get access to project libs and vars

import config_web as conf
import AjaxObject as ajaxObj

# for some reason, this variable needs to be set :: this may be redundant in more recent python versions
# for some reason, this variable needs to be set :: this may be redundant in more recent python versions

conf.os.environ['HOME'] = '/Users/matej/PycharmProjects/tbfy/venv3.7/bin'

sys.stdout.write("Content-Type: application/json")
sys.stdout.write("\n\n")

ajax = ajaxObj.AjaxObject(conf, cgi.FieldStorage())

# dTree simulation data:
# ajax.inputData['action'] = 'dTree'
# ajax.inputData['treeDepth'] = '4'
# ajax.inputData['parameters[]'] = ["Narocnik_Velik_EU","Ponudnik_Velik_EU","SkupnaPonudba"]

# clustering simulation data:
# ajax.inputData['action'] = 'clustering-id'
# ajax.inputData['clusterNum'] = '3'
# # ajax.inputData['selectedDataset'] = 'si-ministry'
# # ajax.inputData['parameters[]'] = ["Narocnik_Velik_EU","Ponudnik_Velik_EU","SkupnaPonudba", "Narocnik_OBCINA", "Narocnik_Oblika"]
# ajax.inputData['selectedDataset'] = 'Germany'
# ajax.inputData['parameters[]'] = ["cpv","publishedOnTed","amount", "awardCriteriaDetails"]

ajax.executeMethod()

sys.stdout.write(json.dumps(ajax.response,indent=1))
sys.stdout.write("\n")
sys.stdout.close()


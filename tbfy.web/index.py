#!/Users/matej/PycharmProjects/tbfy/venv3.7/bin/python
# -*- coding: utf-8 -*-#

# enable cgi execution
# enable cgi execution

import cgitb
cgitb.enable()

print("Content-Type: text/html;charset=utf-8")
print()

# configure params
# configure params

import config_web as conf

# run script
# run script

pageObj = conf.Tbfy.TbfyController(conf)
print(pageObj.getHTML())

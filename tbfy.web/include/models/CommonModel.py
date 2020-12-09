
'''
CommonModel is a module serving htmls, related common content like landing, info, about, gdpr etc. pages.
'''

class CommonModel:

    def __init__(self, conf, getVars):

        self.confObj = conf
        self.getVars = getVars
        self.contentHtml = 'Error: SearchModel HTML nof found.'

    def getView(self):
        '''
        core function to serve a correct / selected view

        :return: string, html format
        '''

        query_a = "landing" if self.getVars.get('a') == None else self.getVars.get('a')
        query_a = query_a.lower()

        # get content HTML
        # get content HTML

        if(query_a == "landing"):
            self.contentHtml = self.getMainLanding()
        elif(query_a == "query_string"):
            self.contentHtml = self.getContractorsSearchView()
        else:
            self.contentHtml = self.confObj.sharedMethods.getErrorView(self.confObj)

        return self.contentHtml

    def getMainLanding(self):
        '''
        function returns main landing page

        :return: string, html format
        '''


        # generate html view
        # generate html view

        dict = {}
        # dict["id"] = idEntity

        content = self.confObj.Template(filename='templates/main_landing.tpl')
        return content.render(data=dict)

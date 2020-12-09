class TbfyController:
    def __init__(self, conf):
        self.html = "Error: HTML not loaded."
        self.confObj = conf

        # create getVars dict
        # create getVars dict

        url = self.confObj.urlHost
        url += "?"
        url += self.confObj.os.getenv("QUERY_STRING")

        from urllib import parse
        self.getVars = dict(parse.parse_qsl(parse.urlsplit(url).query))

    def getHTML(self):
        '''
        Selects associated Model and generates html out of it.

        :return: html string
        '''

        query_m = "landing" if self.getVars.get('m') == None else self.getVars.get('m')

        if(query_m == "transactions"):
            # transactions model
            import models.TransactionsModel as TM
            viewModel = TM.TransactionsModel(self.confObj, self.getVars)
        elif(query_m == "tenders"):
            # tenders model
            import models.TendersModel as TM
            viewModel = TM.TendersModel(self.confObj, self.getVars)
        elif(query_m == "orgs"):
            # tenders model
            import models.OrganizationsModel as ORGS
            viewModel = ORGS.OrganizationsModel(self.confObj, self.getVars)
        else:
            # main landing and other general pages
            import models.CommonModel as CommonModel
            viewModel = CommonModel.CommonModel(self.confObj, self.getVars)

        self.html = self.frameHTML(viewModel.getView())
        return self.html

    def frameHTML(self, contentHTML):
        '''
        Function merges dynamic html to static frame.

        :param contentHTML: dynamic html
        :return: fully generated html page
        '''

        dict = {}
        if self.getVars.get('m') == 'tenders':
            dict['query_m'] = 'tenders'
        elif self.getVars.get('m') == 'transactions':
            dict['query_m'] = 'transactions'
        else:
            dict['query_m'] = ''

        fullHtml = self.confObj.Template(filename='templates/frame.tpl')
        return fullHtml.render(contentHtml=contentHTML,data=dict)

'''
Series of methods shared by various analytical approaches
'''

class SharedTenderDataMethods:

    def __init__(self, conf = None):

        self.conf = conf

    # shared tender functions
    # shared tender functions

    def getTenderdataFieldKeys(self):
        '''
        function returns a dictionary defining parameters needed for decision tree buildup

        :return: dictionary
        '''

        dataFields = {
            'buyerSize': {
                'humanText': 'Buyer size',
                'dataFieldKey': 'Narocnik_Velik_EU'
            },
            'bidderSize': {
                'humanText': 'Bidder size',
                'dataFieldKey': 'Ponudnik_Velik_EU'
            },
            'groupBid': {
                'humanText': 'Group bid?',
                'dataFieldKey': 'SkupnoNarocanje'
            },
            'buyerMncplty': {
                'humanText': 'Buyer municipality',
                'dataFieldKey': 'Narocnik_OBCINA'
            },
            'bidderMncplty': {
                'humanText': 'Bidder municipality',
                'dataFieldKey': 'Ponudnik_OBCINA'
            },
            'buyerRegion': {
                'humanText': 'Buyer region',
                'dataFieldKey': 'Narocnik_Regija'
            },
            'estimatedValue': {
                'humanText': 'Est. tender value',
                'dataFieldKey': 'OcenjenaVrednost'
            },
            'finalValue': {
                'humanText': 'Tender value',
                'dataFieldKey': 'KoncnaVrednost'
            },
            'buyerOrganizationType': {
                'humanText': 'Buyer org. type',
                'dataFieldKey': 'Narocnik_Oblika'
            },
            # 'bidderPostNum': {
            #     'humanText': 'Bidder post num',
            #     'dataFieldKey': 'PonudnikPostnaStevilka'
            # },
            'tenderGoodsType': {
                'humanText': 'Purchase type',
                'dataFieldKey': 'VrstaNarocila'
            },
            'processType': {
                'humanText': 'Tender goods type',
                'dataFieldKey': 'VrstaPostopka'
            },
            # 'processType_EU': {
            #     'humanText': 'Process type',
            #     'dataFieldKey': 'VrstaPostopka_EU'
            # },
            'tenderCriterion': {
                'humanText': 'Criterions',
                'dataFieldKey': 'Merila'
            },
            'euFunds': {
                'humanText': 'EU funding',
                'dataFieldKey': 'EUsredstva'
            },
            'euPublished': {
                'humanText': 'Published in EU',
                'dataFieldKey': 'ObjavaVEU'
            },
            'numOfOffers': {
                'humanText': 'Num of offers',
                'dataFieldKey': 'StPrejetihPonudb'
            },
            'groupBid': {
                'humanText': 'Group Bid',
                'dataFieldKey': 'SkupnaPonudba'
            },
            'cpvNum': {
                'humanText': 'CPV number',
                'dataFieldKey': 'CPV_glavni_2mesti'
            },
            'tenderField': {
                'humanText': 'Tender field',
                'dataFieldKey': 'Podrocje'
            },
            'involvingSubcontractors': {
                'humanText': 'Involving subcontractors',
                'dataFieldKey': 'OddanoPodizvajalcem'
            },
            'buyerMainOccupation': {
                'humanText': 'Buyer main occupation',
                'dataFieldKey': 'Narocnik_Dejavnost'
            }
        }

        return dataFields

    def getTenderDataFieldKeysSelected(self, parameterList = []):
        '''
        function returns a dictionary defining preselected parameters needed for decision tree buildup

        :return: dictionary of selected  to build a decision tree
        '''

        allDataDict = self.getTenderdataFieldKeys()
        returnList = []

        for key in allDataDict:
            if key in parameterList or len(parameterList) == 0:
                returnList.append(allDataDict[key]['dataFieldKey'])

        return returnList

    def getTenderdataFieldKeysSelectedHRFormat(self, parameterList = []):
        '''
        function returns list of parameters as defined in parameterList in human readable format

        :param parameterList: list of parameters with their base identification names
        :return: list of parameters as defined in parameterList in human readable format
        '''

        allDataDict = self.getTenderdataFieldKeys()
        returnList = []

        for key in allDataDict:
            addElement = False
            if len(parameterList) == 0:
                addElement = True
            elif key in parameterList:
                addElement = True

            if addElement:
                returnList.append(allDataDict[key]['humanText'])

        return returnList
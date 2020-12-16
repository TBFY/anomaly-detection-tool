
'''
OrganizationModel is a module serving htmls, related to organizations. Main purpose is to explore bidders or buyers in more detail.
'''

class OrganizationsModel:

    def __init__(self, conf, getVars):

        self.conf = conf
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
            self.contentHtml = self.getSearchOrgView()
        elif(query_a == "source_mju"):
            self.contentHtml = self.getMJUSourceOrgsView()
        else:
            self.contentHtml = self.conf.sharedMethods.getErrorView(self.conf)

        return self.contentHtml

    def getSearchOrgView(self):
        '''
        function returns an organization search interface

        :return: string, html format
        '''

        # get company id
        # get company id

        id_bidder_string = '' if self.getVars.get('id') == None else self.getVars.get('id')

        # generate html view
        # generate html view

        dict = {}
        dict['id_company'] = id_company_string

        content = self.conf.Template(filename='templates/orgs_search.tpl')
        return content.render(data=dict)

    def getMJUSourceOrgsView(self):
        '''
        function returns mju (ministrstvo za javno upravo) sourced organization data

        :return: string, html format
        '''

        company_id = '' if self.getVars.get('id') == None else self.getVars.get('id')
        id_bidder_string = '' if self.getVars.get('id') == None else self.getVars.get('id')

        if id_bidder_string == '':
            return self.getSearchOrgView()

        # verify id
        # verify id
        
        import re
        id_bidder = re.findall("\d+", id_bidder_string)

        if len(id_bidder) == 0:
            return self.getSearchOrgView()
        else:
            id_bidder = id_bidder[0]

        # set sql vars
        # set sql vars

        sql = self.conf.cDB.sql
        cur = self.conf.cDB.db.cursor()

        # define examined company data
        # define examined company data

        companyProfileDict = {}

        # BEGIN won tenders data aggregation
        # BEGIN won tenders data aggregation

        # final data structure passed to template is:
        # wonTenders[idizpobrazca]['tender'] = list of lots
        # wonTenders[idizpobrazca]['winners'] = list of winners

        wonTenders = {}

        # data structure:
        # wonTendersChartData = {}
        # wonTendersChartData['byValue'] =     {}
        # wonTendersChartData['byTenderNum'] = {}}

        # wonTendersChartData['byValue']['id_company']['company_name'] = name of winners
        # wonTendersChartData['byValue']['id_company']['share']        = tender's share value
        # wonTendersChartData['byValue']['id_company']['abssum']       = absolute tender value

        wonTendersChartData = {}
        wonTendersChartData['byValue'] = {}
        wonTendersChartData['byTenderNum'] = {}

        # find all awards for a company
        # find all awards for a company

        queryBase = "select * from {} WHERE {} = '%s'"
        queryString = sql.SQL(queryBase).format(
            # set queried fields
            sql.Identifier('cst_postopki_jn_izvajalci'),
            sql.Identifier('ponudnikmaticna'))
        cur.execute(queryString, (int(id_bidder),))
        companyAwards = self.conf.sharedCommon.returnSqlDataInDictFormat(cur, 'idizppriloge')

        if len(companyAwards) > 0:

            # define examined company data
            # define examined company data

            id = list(companyAwards.keys())[0]
            companyProfileDict = companyAwards[id]

            # if we have winners, find all winners's tenders
            # if we have winners, find all winners's tenders

            idString = "','".join(str(x) for x in companyAwards.keys())
            idString = "'" + idString + "'"

            queryBase = "select * from {} WHERE idizppriloge IN (" + idString + ")"
            queryString = sql.SQL(queryBase).format(
                # set queried fields
                sql.Identifier('cst_postopki_jn'),
                sql.Identifier('ponudnikmaticna'))
            cur.execute(queryString)
            winnersTenders = self.conf.sharedCommon.returnSqlDataInDictFormat(cur, 'idizppriloge')

            tendersWonAwardsSum = 0.0
            for id,row in winnersTenders.items():
                tendersWonAwardsSum += float(row['koncnavrednost'])
                # add tender data
                tender_key = row['idizpobrazca']
                if tender_key not in wonTenders:
                    wonTenders[tender_key] = {}
                    wonTenders[tender_key]['tender'] = []
                    wonTenders[tender_key]['winners'] = []
                wonTenders[tender_key]['tender'].append(row)

            # add tender winners to wonTenders structure
            # add tender winners to wonTenders structure

            idString = "','".join(str(x) for x in winnersTenders.keys())
            idString = "'" + idString + "'"

            queryBase = "select * from {} WHERE idizppriloge IN (" + idString + ")"
            queryString = sql.SQL(queryBase).format(
                # set queried fields
                sql.Identifier('cst_postopki_jn_izvajalci'))
            cur.execute(queryString)
            tenderWinnersList = self.conf.sharedCommon.returnSqlDataInDictFormat(cur)

            tendersWonWinnersNum = len(tenderWinnersList)
            tenderWonAwardsSum = 0.0

            for row in tenderWinnersList:
                tender_key = row['idizpobrazca']
                wonTenders[tender_key]['winners'].append(row)

            # get chart data for won tenders
            # get chart data for won tenders

            # first convert wonTenders into wonLots
            # wonLots[id_lot][lot] = lot
            # wonLots[id_lot][lot_winners] = list of lot winners
            # wonLots[id_lot][share] = (num of company wons) / (num of all lot winners)

            # wonLots[id_lot][share]: there can be multiple lot winners, for example 3,
            # where one of them is observed company. Share than equals 1/3

            wonLots = {}

            if len(wonTenders) > 0:
                for idTender,row in wonTenders.items():

                    # organise lots in wonLots
                    # organise lots in wonLots

                    for lot in row['tender']:
                        id_lot = str(lot['idizppriloge'])

                        # initiate new wonLots entry
                        # initiate new wonLots entry

                        if id_lot not in wonLots:
                            wonLots[id_lot] = {}
                            wonLots[id_lot]['lot'] = lot
                            wonLots[id_lot]['winners'] = []
                            wonLots[id_lot]['share_value'] = 0.0

                    # organise winners in wonLots
                    # organise winners in wonLots

                    for winner in row['winners']:
                       id_lot = str(winner['idizppriloge'])
                       wonLots[id_lot]['winners'].append(winner)


                # calculate amount share that belongs to observed company
                # calculate amount share that belongs to observed company

                for id_lot,lot in wonLots.items():
                    i_all = len(lot['winners'])
                    i_won = 0
                    for winner in lot['winners']:
                        if str(winner['ponudnikmaticna']) == id_bidder_string:
                            i_won += 1

                    share = 1 if i_all == i_won else i_won / i_all
                    wonLots[id_lot]['share'] = share

            # then, convert wonLots into chart data
            # then, convert wonLots into chart data

            # fill byValue list
            # fill byValue list

            tmp_byValueDict = {}
            tmp_byTenderNumDict = {}
            if len(wonLots) > 0:
                for id_lot,lot in wonLots.items():

                    # get buter id
                    # get buter id

                    tmp_companyID = lot['lot']['narocnikmaticna']
                    if tmp_companyID not in wonTendersChartData['byTenderNum']:

                        # init byValue
                        # init byValue

                        wonTendersChartData['byValue'][tmp_companyID] = {}
                        wonTendersChartData['byValue'][tmp_companyID]['share'] = 0.0
                        wonTendersChartData['byValue'][tmp_companyID]['abssum'] = 0.0
                        if len(lot['lot']['narocnikorganizacijakratko']) > 0:
                            wonTendersChartData['byValue'][tmp_companyID]['company_name'] = lot['lot']['narocnikorganizacijakratko']
                        else:
                            wonTendersChartData['byValue'][tmp_companyID]['company_name'] = lot['lot']['narocnikorganizacija']

                        # init byTenderNum
                        # init byTenderNum

                        wonTendersChartData['byTenderNum'][tmp_companyID] = {}
                        wonTendersChartData['byTenderNum'][tmp_companyID]['share'] = 0.0
                        wonTendersChartData['byTenderNum'][tmp_companyID]['abssum'] = 0
                        wonTendersChartData['byTenderNum'][tmp_companyID]['company_name'] = wonTendersChartData['byValue'][tmp_companyID]['company_name']

                        # for sorting purposes
                        # for sorting purposes

                        tmp_byValueDict[tmp_companyID] = 0.0
                        tmp_byTenderNumDict[tmp_companyID] = 0


                    # add byValue values
                    # add byValue values

                    tmp_totalLotValue = lot['lot']['koncnavrednost'] * lot['share']

                    tenderWonAwardsSum += tmp_totalLotValue
                    wonTendersChartData['byValue'][tmp_companyID]['abssum'] += tmp_totalLotValue

                    wonTendersChartData['byTenderNum'][tmp_companyID]['share'] += 1 / tendersWonWinnersNum
                    wonTendersChartData['byTenderNum'][tmp_companyID]['abssum'] += 1
                    tmp_byTenderNumDict[tmp_companyID] = wonTendersChartData['byTenderNum'][tmp_companyID]['share']


                # calculate value shares
                # calculate value shares

                for tmp_companyID, row in wonTendersChartData['byValue'].items():
                    wonTendersChartData['byValue'][tmp_companyID]['share'] = wonTendersChartData['byValue'][tmp_companyID]['abssum'] / tenderWonAwardsSum
                    tmp_byValueDict[tmp_companyID] = wonTendersChartData['byValue'][tmp_companyID]['share']

                # sort list
                # sort list

                tmp_byValueDictSorted = {k: tmp_byValueDict[k] for k in sorted(tmp_byValueDict, key=tmp_byValueDict.get, reverse=True)}
                tmp_byTenderNumDictSorted = {k: tmp_byTenderNumDict[k] for k in sorted(tmp_byTenderNumDict, key=tmp_byTenderNumDict.get,reverse=True)}

                # by value
                # by value

                tmp_byValueDictFinal = {}
                tmp_share_cumulative = 0.0
                tmp_abs_cumulative = 0.0
                i = 0
                i_max = len(tmp_byValueDictSorted)
                for tmp_companyID,tmp_share in tmp_byValueDictSorted.items():
                    i += 1
                    tmp_share_cumulative += tmp_share
                    tmp_abs_cumulative += wonTendersChartData['byValue'][tmp_companyID]['abssum']
                    tmp_byValueDictFinal[tmp_companyID] = wonTendersChartData['byValue'][tmp_companyID]
                    if tmp_share_cumulative > 0.75 and i < i_max:
                        tmp_dict = {}
                        tmp_dict['company_name'] = 'others'
                        tmp_dict['share'] = 1 - tmp_share_cumulative
                        tmp_dict['abssum'] = tendersWonAwardsSum - tmp_abs_cumulative
                        tmp_byValueDictFinal['others'] = tmp_dict
                        break;
                wonTendersChartData['byValue'] = tmp_byValueDictFinal

                # by tender num
                # by tender num

                tmp_byTenderNumDictFinal = {}
                tmp_share_cumulative = 0.0
                tmp_abs_cumulative = 0
                i = 0
                i_max = len(tmp_byTenderNumDictSorted)
                for tmp_companyID,tmp_share in tmp_byTenderNumDictSorted.items():
                    i += 1
                    tmp_share_cumulative += tmp_share
                    tmp_abs_cumulative += wonTendersChartData['byTenderNum'][tmp_companyID]['abssum']
                    tmp_byTenderNumDictFinal[tmp_companyID] = wonTendersChartData['byTenderNum'][tmp_companyID]
                    if tmp_share_cumulative > 0.75 and i < i_max:
                        tmp_dict = {}
                        tmp_dict['company_name'] = 'others'
                        tmp_dict['share'] = 1 - tmp_share_cumulative
                        tmp_dict['abssum'] = tendersWonWinnersNum - tmp_abs_cumulative
                        tmp_byTenderNumDictFinal['others'] = tmp_dict
                        break;
                wonTendersChartData['byTenderNum'] = tmp_byTenderNumDictFinal

        # END won tenders data aggregation
        # END won tenders data aggregation

        # BEGIN issued tenders data aggregation
        # BEGIN issued tenders data aggregation

        # final data structure passed to template is:
        # issuedTenders[idizpobrazca]['tender'] = list of lots
        # issuedTenders[idizpobrazca]['winners'] = list of winners

        issuedTenders = {}

        # find all issued tenders for a company
        # find all issued tenders for a company

        queryBase = "select * from {} WHERE {} = '%s'"
        queryString = sql.SQL(queryBase).format(
            # set queried fields
            sql.Identifier('cst_postopki_jn'),
            sql.Identifier('narocnikmaticna'))
        cur.execute(queryString, (int(id_bidder),))
        companyTenders = self.conf.sharedCommon.returnSqlDataInDictFormat(cur, 'idizppriloge')

        tenderIssuedWinnersNum = 0
        tenderIssuedAwardsSum = 0.0
        for id,row in companyTenders.items():
            tenderIssuedAwardsSum += float(row['koncnavrednost'])
            # add tender data
            tender_key = row['idizpobrazca']
            if tender_key not in issuedTenders:
                issuedTenders[tender_key] = {}
                issuedTenders[tender_key]['tender'] = []
                issuedTenders[tender_key]['winners'] = []
            issuedTenders[tender_key]['tender'].append(row)

        # add tender winners to issuedTenders structure
        # add tender winners to issuedTenders structure

        if len(companyTenders) > 0:

            # define examined company data if not yed defined
            # define examined company data if not yed defined

            if len(companyProfileDict) == 0:
                 id = list(companyTenders.keys())[0]
                 companyProfileDict = companyTenders[id]

            # find issued tenders winners
            # find issued tenders winners

            idString = "','".join(str(x) for x in companyTenders.keys())
            idString = "'" + idString + "'"

            queryBase = "select * from {} WHERE idizppriloge IN (" + idString + ")"
            queryString = sql.SQL(queryBase).format(
                # set queried fields
                sql.Identifier('cst_postopki_jn_izvajalci'))
            cur.execute(queryString)
            tenderWinnersList = self.conf.sharedCommon.returnSqlDataInDictFormat(cur)

            tenderIssuedWinnersNum = len(tenderWinnersList)

            for row in tenderWinnersList:
                tender_key = row['idizpobrazca']
                issuedTenders[tender_key]['winners'].append(row)

        # get chart data for issues tenders
        # get chart data for issues tenders

        # data structure:
        # issuedTendersChartData = {}
        # issuedTendersChartData['byValue'] =     {}
        # issuedTendersChartData['byTenderNum'] = {}}

        # issuedTendersChartData['byValue']['id_company']['company_name'] = name of winners
        # issuedTendersChartData['byValue']['id_company']['share']        = tender's share value
        # issuedTendersChartData['byValue']['id_company']['abssum']       = absolute tender value

        issuedTendersChartData = {}
        issuedTendersChartData['byValue'] = {}
        issuedTendersChartData['byTenderNum'] = {}

        # fill byValue list
        # fill byValue list

        tmp_byValueDict = {}
        tmp_byTenderNumDict = {}
        if len(issuedTenders) > 0:
            for idTender,row in issuedTenders.items():
                # get total tender value
                tmp_totalTenderValue = 0.0
                for lot in row['tender']:
                    tmp_totalTenderValue += lot['koncnavrednost']
                # get number of tender winners
                numWinners = float(len(row['winners']))
                for rowWinner in row['winners']:
                    tmp_companyID = rowWinner['ponudnikmaticna']
                    if tmp_companyID not in issuedTendersChartData['byValue']:
                        # init byValue
                        # init byValue

                        issuedTendersChartData['byValue'][tmp_companyID] = {}
                        issuedTendersChartData['byValue'][tmp_companyID]['share'] = 0.0
                        issuedTendersChartData['byValue'][tmp_companyID]['abssum'] = 0.0
                        if len(rowWinner['ponudnikorganizacijakratko']) > 0:
                            issuedTendersChartData['byValue'][tmp_companyID]['company_name'] = rowWinner['ponudnikorganizacijakratko']
                        else:
                            issuedTendersChartData['byValue'][tmp_companyID]['company_name'] = rowWinner['ponudnikorganizacija']

                        # init byTenderNum
                        # init byTenderNum

                        issuedTendersChartData['byTenderNum'][tmp_companyID] = {}
                        issuedTendersChartData['byTenderNum'][tmp_companyID]['share'] = 0.0
                        issuedTendersChartData['byTenderNum'][tmp_companyID]['abssum'] = 0
                        issuedTendersChartData['byTenderNum'][tmp_companyID]['company_name'] = issuedTendersChartData['byValue'][tmp_companyID]['company_name']

                        ## for sorting purposes

                        tmp_byValueDict[tmp_companyID] = 0.0
                        tmp_byTenderNumDict[tmp_companyID] = 0

                    # add byValue values
                    # add byValue values

                    tenderValuePerCompany = float(tmp_totalTenderValue) / numWinners
                    issuedTendersChartData['byValue'][tmp_companyID]['share'] += tenderValuePerCompany / tenderIssuedAwardsSum
                    issuedTendersChartData['byValue'][tmp_companyID]['abssum'] += tenderValuePerCompany
                    tmp_byValueDict[tmp_companyID] = issuedTendersChartData['byValue'][tmp_companyID]['share']

                    # add byTenderNum values
                    # add byTenderNum values

                    issuedTendersChartData['byTenderNum'][tmp_companyID]['share'] += 1 / tenderIssuedWinnersNum
                    issuedTendersChartData['byTenderNum'][tmp_companyID]['abssum'] += 1
                    tmp_byTenderNumDict[tmp_companyID] = issuedTendersChartData['byTenderNum'][tmp_companyID]['share']

            # sort list
            # sort list

            tmp_byValueDictSorted = {k: tmp_byValueDict[k] for k in sorted(tmp_byValueDict, key=tmp_byValueDict.get, reverse=True)}
            tmp_byTenderNumDictSorted = {k: tmp_byTenderNumDict[k] for k in sorted(tmp_byTenderNumDict, key=tmp_byTenderNumDict.get, reverse=True)}

            # create final version of lists
            # create final version of lists

            # by value
            # by value

            tmp_byValueDictFinal = {}
            tmp_share_cumulative = 0.0
            tmp_abs_cumulative = 0.0
            i = 0
            i_max = len(tmp_byValueDictSorted)
            for tmp_companyID,tmp_share in tmp_byValueDictSorted.items():
                i += 1
                tmp_share_cumulative += tmp_share
                tmp_abs_cumulative += issuedTendersChartData['byValue'][tmp_companyID]['abssum']
                tmp_byValueDictFinal[tmp_companyID] = issuedTendersChartData['byValue'][tmp_companyID]
                if tmp_share_cumulative > 0.75 and i < i_max:
                    tmp_dict = {}
                    tmp_dict['company_name'] = 'others'
                    tmp_dict['share'] = 1 - tmp_share_cumulative
                    tmp_dict['abssum'] = tenderIssuedAwardsSum - tmp_abs_cumulative
                    tmp_byValueDictFinal['others'] = tmp_dict
                    break;
            issuedTendersChartData['byValue'] = tmp_byValueDictFinal

            # by tender num
            # by tender num

            tmp_byTenderNumDictFinal = {}
            tmp_share_cumulative = 0.0
            tmp_abs_cumulative = 0
            i = 0
            i_max = len(tmp_byTenderNumDictSorted)
            for tmp_companyID,tmp_share in tmp_byTenderNumDictSorted.items():
                i += 1
                tmp_share_cumulative += tmp_share
                tmp_abs_cumulative += issuedTendersChartData['byTenderNum'][tmp_companyID]['abssum']
                tmp_byTenderNumDictFinal[tmp_companyID] = issuedTendersChartData['byTenderNum'][tmp_companyID]
                if tmp_share_cumulative > 0.75 and i < i_max:
                    tmp_dict = {}
                    tmp_dict['company_name'] = 'others'
                    tmp_dict['share'] = 1 - tmp_share_cumulative
                    tmp_dict['abssum'] = tenderIssuedWinnersNum - tmp_abs_cumulative
                    tmp_byTenderNumDictFinal['others'] = tmp_dict
                    break;
            issuedTendersChartData['byTenderNum'] = tmp_byTenderNumDictFinal

        if 'ponudnikorganizacijakratko' in companyProfileDict:
            companyProfileDict['ajpesnaziv'] = companyProfileDict['ponudnikorganizacijakratko'].replace(' ', '_')
            companyProfileDict['erardavcna'] = companyProfileDict['ponudnikdavcna']

        if 'narocnikorganizacijakratko' in companyProfileDict:
            companyProfileDict['erardavcna'] = companyProfileDict['narocnikdavcna']
            if len(companyProfileDict['narocnikorganizacijakratko']) > len(companyProfileDict['narocnikorganizacija']):
                companyProfileDict['ajpesnaziv'] = companyProfileDict['narocnikorganizacijakratko'].replace(' ', '_')
            else:
                companyProfileDict['ajpesnaziv'] = companyProfileDict['narocnikorganizacija'].replace(' ', '_')


        # END issued tenders data aggregation
        # END issued tenders data aggregation

        # look for anomalies
        # look for anomalies

        anomaliesDict = {}

        # find company cpv
        # find company cpv

        cpv2digits = 0
        if len(wonTenders) > 0:
            tmp_lot = list(wonTenders.values())[0]
            cpv2digits = tmp_lot['tender'][0]['cpv_glavni_2mesti']

        # anomaly 1 :: distributions offersNum
        # anomaly 1 :: distributions offersNum

        distrFilePath = self.conf.publicTenderDataRoot + 'distributions/offersNum/'
        distrFileNameNeg = 'si-ministry--neg-deviations.tsv'
        cmnDistrFileName = 'si-ministry--cmn-distribution.tsv'
        cmnCPVDistrFileName = 'si-ministry-' + str(cpv2digits) + '-cmn-distribution.tsv'
        distrNegativeDevs = self.conf.sharedCommon.readDataFile2Dict(distrFilePath + distrFileNameNeg, "\t")

        numOfAnomalies = 0
        for row in distrNegativeDevs['data']:
            if row[1] == company_id:
                anomaliesDict['distribution-offersnum'] = {}
                anomaliesDict['distribution-offersnum']['anomaly'] = row
                anomaliesDict['distribution-offersnum']['avgdistr'] = self.conf.sharedCommon.readDataFile2Dict(distrFilePath + cmnDistrFileName, "\t")
                anomaliesDict['distribution-offersnum']['cpv'] = cpv2digits
                anomaliesDict['distribution-offersnum']['cpvdistr'] = self.conf.sharedCommon.readDataFile2Dict(distrFilePath + cmnCPVDistrFileName, "\t")
                numOfAnomalies += 1

        # anomaly 2 :: distributions budget assess
        # anomaly 2 :: distributions budget assess

        distrBdgFilePath = self.conf.publicTenderDataRoot + 'distributions/budgetAssessment/'
        distrBdgFileName = 'si-ministry--data-values.tsv'
        distrDataValues = self.conf.sharedCommon.readDataFile2Dict(distrBdgFilePath + distrBdgFileName, "\t")

        for row in distrDataValues['data']:
            if row[1] == company_id:
                if abs(float(row[0])) > 0.5:
                    anomaliesDict['distribution-bdgasses'] = {}
                    anomaliesDict['distribution-bdgasses']['anomaly'] = row
                    numOfAnomalies += 1

        # anomaly 3 :: ratios - revenue per employee
        # anomaly 3 :: ratios - revenue per employee

        ratioRevFilePath = self.conf.publicTenderDataRoot + 'ratios/revenuePerEmployee/'

        # read negative deviations
        # read negative deviations

        anomalyFound = 0
        ratioRevNegFileName = 'si-ministry-neg-deviations.tsv'
        ratioRevNegDataValues = self.conf.sharedCommon.readDataFile2Dict(ratioRevFilePath + ratioRevNegFileName, "\t")
        anomalyKey = 'ratio-rev-per-employee-neg'
        for row in ratioRevNegDataValues['data']:
            # company as buyer id
            if row[2] == company_id:
                if anomalyKey not in anomaliesDict:
                    anomaliesDict[anomalyKey] = {}

                if 'buyers' not in anomaliesDict[anomalyKey]:
                    anomaliesDict[anomalyKey]['buyers'] = []
                anomaliesDict[anomalyKey]['buyers'].append(row)
                anomalyFound = 1
            # company as bidder id
            if row[3] == company_id:
                if anomalyKey not in anomaliesDict:
                    anomaliesDict[anomalyKey] = {}

                if 'bidders' not in anomaliesDict[anomalyKey]:
                    anomaliesDict[anomalyKey]['bidders'] = []
                anomaliesDict[anomalyKey]['bidders'].append(row)
                anomalyFound = 1
        numOfAnomalies += anomalyFound

        # read positive deviations
        # read positive deviations

        anomalyFound = 0
        ratioRevPosFileName = 'si-ministry-pos-deviations.tsv'
        ratioRevPosDataValues = self.conf.sharedCommon.readDataFile2Dict(ratioRevFilePath + ratioRevPosFileName, "\t")
        anomalyKey = 'ratio-rev-per-employee-pos'
        for row in ratioRevPosDataValues['data']:
            # company as buyer id
            if row[2] == company_id:
                if anomalyKey not in anomaliesDict:
                    anomaliesDict[anomalyKey] = {}

                if 'buyers' not in anomaliesDict[anomalyKey]:
                    anomaliesDict[anomalyKey]['buyers'] = []
                anomaliesDict[anomalyKey]['buyers'].append(row)
                anomalyFound = 1
            # company as bidder id
            if row[3] == company_id:
                if anomalyKey not in anomaliesDict:
                    anomaliesDict[anomalyKey] = {}

                if 'bidders' not in anomaliesDict[anomalyKey]:
                    anomaliesDict[anomalyKey]['bidders'] = []
                anomaliesDict[anomalyKey]['bidders'].append(row)
                anomalyFound = 1
        numOfAnomalies += anomalyFound

        # anomaly 4 :: ratios - revenue per employee
        # anomaly 4 :: ratios - revenue per employee

        ratioRevFilePath = self.conf.publicTenderDataRoot + 'ratios/budgetAssessment/'

        # read negative deviations
        # read negative deviations

        anomalyFound = 0
        ratioRevNegFileName = 'si-ministry-neg-deviations.tsv'
        ratioRevNegDataValues = self.conf.sharedCommon.readDataFile2Dict(ratioRevFilePath + ratioRevNegFileName, "\t")
        anomalyKey = 'ratio-assessed-final-bdg-neg'
        for row in ratioRevNegDataValues['data']:
            # company as buyer id
            if row[2] == company_id:
                if anomalyKey not in anomaliesDict:
                    anomaliesDict[anomalyKey] = {}

                if 'buyers' not in anomaliesDict[anomalyKey]:
                    anomaliesDict[anomalyKey]['buyers'] = []
                anomaliesDict[anomalyKey]['buyers'].append(row)
                anomalyFound = 1
            # company as bidder id
            if row[3] == company_id:
                if anomalyKey not in anomaliesDict:
                    anomaliesDict[anomalyKey] = {}

                if 'bidders' not in anomaliesDict[anomalyKey]:
                    anomaliesDict[anomalyKey]['bidders'] = []
                anomaliesDict[anomalyKey]['bidders'].append(row)
                anomalyFound = 1
        numOfAnomalies += anomalyFound

        # read positive deviations
        # read positive deviations

        anomalyFound = 0
        ratioRevPosFileName = 'si-ministry-pos-deviations.tsv'
        ratioRevPosDataValues = self.conf.sharedCommon.readDataFile2Dict(ratioRevFilePath + ratioRevPosFileName, "\t")
        anomalyKey = 'ratio-assessed-final-bdg-pos'
        for row in ratioRevPosDataValues['data']:
            # company as buyer id
            if row[2] == company_id:
                if anomalyKey not in anomaliesDict:
                    anomaliesDict[anomalyKey] = {}

                if 'buyers' not in anomaliesDict[anomalyKey]:
                    anomaliesDict[anomalyKey]['buyers'] = []
                anomaliesDict[anomalyKey]['buyers'].append(row)
                anomalyFound = 1
            # company as bidder id
            if row[3] == company_id:
                if anomalyKey not in anomaliesDict:
                    anomaliesDict[anomalyKey] = {}

                if 'bidders' not in anomaliesDict[anomalyKey]:
                    anomaliesDict[anomalyKey]['bidders'] = []
                anomaliesDict[anomalyKey]['bidders'].append(row)
                anomalyFound = 1
        numOfAnomalies += anomalyFound

        # anomaly 5 :: dependencies
        # anomaly 5 :: dependencies

        ratioRevFilePath = self.conf.publicTenderDataRoot + 'relations_bb/'

        # dependencies bidder2buyer
        # dependencies bidder2buyer

        anomalyFound = 0
        ratioRevNegFileName = 'si-ministry-bidder2buyer.tsv'
        ratioRevNegDataValues = self.conf.sharedCommon.readDataFile2Dict(ratioRevFilePath + ratioRevNegFileName, "\t")
        anomalyKey = 'dependency-bidder2buyer'
        for row in ratioRevNegDataValues['data']:
            # company as buyer id
            if row[0] == company_id:
                if anomalyKey not in anomaliesDict:
                    anomaliesDict[anomalyKey] = {}

                if 'buyers' not in anomaliesDict[anomalyKey]:
                    anomaliesDict[anomalyKey]['buyers'] = []
                anomaliesDict[anomalyKey]['buyers'].append(row)
                anomalyFound = 1
            # company as bidder id
            if row[1] == company_id:
                if anomalyKey not in anomaliesDict:
                    anomaliesDict[anomalyKey] = {}

                if 'bidders' not in anomaliesDict[anomalyKey]:
                    anomaliesDict[anomalyKey]['bidders'] = []
                anomaliesDict[anomalyKey]['bidders'].append(row)
                anomalyFound = 1
        numOfAnomalies += anomalyFound

        # dependencies buyer2bidder
        # dependencies buyer2bidder

        anomalyFound = 0
        ratioRevNegFileName = 'si-ministry-buyer2bidder.tsv'
        ratioRevNegDataValues = self.conf.sharedCommon.readDataFile2Dict(ratioRevFilePath + ratioRevNegFileName, "\t")
        anomalyKey = 'dependency-buyer2bidder'
        for row in ratioRevNegDataValues['data']:
            # company as buyer id
            if row[0] == company_id:
                if anomalyKey not in anomaliesDict:
                    anomaliesDict[anomalyKey] = {}

                if 'buyers' not in anomaliesDict[anomalyKey]:
                    anomaliesDict[anomalyKey]['buyers'] = []
                anomaliesDict[anomalyKey]['buyers'].append(row)
                anomalyFound = 1
            # company as bidder id
            if row[1] == company_id:
                if anomalyKey not in anomaliesDict:
                    anomaliesDict[anomalyKey] = {}

                if 'bidders' not in anomaliesDict[anomalyKey]:
                    anomaliesDict[anomalyKey]['bidders'] = []
                anomaliesDict[anomalyKey]['bidders'].append(row)
                anomalyFound = 1
        numOfAnomalies += anomalyFound

        # dependencies mutual
        # dependencies mutual

        anomalyFound = 0
        ratioRevNegFileName = 'si-ministry-mutual.tsv'
        ratioRevNegDataValues = self.conf.sharedCommon.readDataFile2Dict(ratioRevFilePath + ratioRevNegFileName, "\t")
        anomalyKey = 'dependency-mutual'
        for row in ratioRevNegDataValues['data']:
            # company as buyer id
            if row[0] == company_id:
                if anomalyKey not in anomaliesDict:
                    anomaliesDict[anomalyKey] = {}

                if 'buyers' not in anomaliesDict[anomalyKey]:
                    anomaliesDict[anomalyKey]['buyers'] = []
                anomaliesDict[anomalyKey]['buyers'].append(row)
                anomalyFound = 1
            # company as bidder id
            if row[1] == company_id:
                if anomalyKey not in anomaliesDict:
                    anomaliesDict[anomalyKey] = {}

                if 'bidders' not in anomaliesDict[anomalyKey]:
                    anomaliesDict[anomalyKey]['bidders'] = []
                anomaliesDict[anomalyKey]['bidders'].append(row)
                anomalyFound = 1
        numOfAnomalies += anomalyFound

        # check distributions
        # check distributions
        # check distributions

        # construct html
        # construct html

        dict = {}
        # company profile
        dict['companyProfileDict'] = companyProfileDict
        # issued tender data
        dict['issuedTenders'] = issuedTenders
        dict['issuedTendersChartData'] = issuedTendersChartData
        # won tender data
        dict['wonTenders'] = wonTenders
        dict['wonTendersChartData'] = wonTendersChartData
        # anomalies data
        dict['numOfAnomalies'] = numOfAnomalies
        dict['anomaliesDict'] = anomaliesDict

        content = self.conf.Template(filename='templates/orgs_overview_mju.tpl')
        return content.render(data=dict)
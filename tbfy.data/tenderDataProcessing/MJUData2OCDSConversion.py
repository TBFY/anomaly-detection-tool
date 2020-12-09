
'''
Module takes data in raw format from the ministry of public administration and converts it into ocds format
'''

class MJUData2OCDSConversion:

    def __init__(self, conf, shared):

        self.conf = conf
        self.shared = shared

        # various data vars
        # various data vars

        self.ocdsId = 'ocds-mnnhvj'
        self.ocdsJsonObj = {}

        # set date string to identify correct files // example: 6th of January 2020 => 202016
        # set date string to identify correct files // example: 6th of January 2020 => 202016

        #self.dateString = (self.conf.datetime.datetime.now() - self.conf.datetime.timedelta(days=1)).strftime("%Y%" + self.conf.datetimeLeadingZeroRemovalChar + "m%" + self.conf.datetimeLeadingZeroRemovalChar + "d")
        self.dateString = ''

        # data storage variables
        # data storage variables

        self.rawData = {}
        self.ocdsData = {}
        self.missingDataStopScript = False

        # file variables
        # file variables

        self.rawTenderDataFileName = 'PostopkiJN_DATE.csv'
        #self.rawTenderDataFileName = 'PostopkiJN_DATE.csv'
        self.rawTenderDataFilePath = conf.tenderDataRawPath

        self.rawAwardsDataFileName = 'PostopkiJNIzvajalci_DATE.csv'
        #self.rawAwardsDataFileName = 'PostopkiJNIzvajalci_DATE.csv'
        self.rawAwardsDataFilePath = conf.tenderDataRawPath

        self.ocdsDataFileName = 'DATE-ocds-si-public-tenders.json'
        self.ocdsDataFilePath = conf.tenderDataOCDSFormatPath

    def convertRawFiles2OCDS(self):
        '''
        function finds all non converted files and sends them into conversion

        :return: None
        '''

        # test purposes - datestring is already set
        # test purposes - datestring is already set

        if len(self.dateString) > 0:
            self.readRawFile()
            self.convertRaw2OCDS()
            self.exportOcdsJson2File()
            return None

        # normal execution
        # normal execution

        allRawFilesList = [f for f in self.conf.os.listdir(self.conf.tenderDataRawPath) if self.conf.os.path.isfile(self.conf.os.path.join(self.conf.tenderDataRawPath, f)) and 'PostopkiJN_' in f]

        for fileName in allRawFilesList:
            filePieces = fileName.split('_')
            filePieces = filePieces[1].split('.')

            # get converted ff
            # get converted ff

            self.dateString = filePieces[0]
            fulFilePath = self.conf.os.path.join(self.conf.tenderDataOCDSFormatPath, self.ocdsDataFileName.replace('DATE', self.dateString))

            if self.conf.os.path.isfile(fulFilePath):
                continue
            else:
                #print('converting: ', fulFilePath)
                self.missingDataStopScript = False
                self.readRawFile()
                self.convertRaw2OCDS()
                self.exportOcdsJson2File()

        return None

    def sourcefilesExist(self, fullFilePath):
        '''
        function checks whether files exist

        :return: boolean
        '''

        if self.conf.os.path.exists(fullFilePath):
            return True
        else:
            return False

    def readRawFile(self):
        '''
        Function takes in raw data in csv format and stores the data in self.rawData variable

        :return: void
        '''

        # read tenders and awards file
        # read tenders and awards file

        rawTenderDataFileName = self.rawTenderDataFileName.replace('DATE', self.dateString)
        tenderFilePath = self.conf.os.path.join(self.rawTenderDataFilePath, rawTenderDataFileName)
        if self.sourcefilesExist(tenderFilePath):
            tendersData = self.conf.sharedCommon.readDataFile2Dict(tenderFilePath, splitChar = ';')
        else:
            self.missingDataStopScript = True
            return None

        if len(tendersData['data']) == 0:
            self.missingDataStopScript = True
            return None

        rawAwardsDataFileName = self.rawAwardsDataFileName.replace('DATE', self.dateString)
        awardsFilePath = self.conf.os.path.join(self.rawAwardsDataFilePath, rawAwardsDataFileName)
        if self.sourcefilesExist(awardsFilePath):
            awardsData = self.conf.sharedCommon.readDataFile2Dict(awardsFilePath, splitChar = ';')
        else:
            self.missingDataStopScript = True
            return None

        if len(awardsData['data']) == 0:
            self.missingDataStopScript = True
            return None

        # init data structure:
        # self.rawData
        # self.rawData['head']
        # self.rawData['head']['tender'] => tender head data
        # self.rawData['head']['award'] => award head data
        # self.rawData['data']
        # self.rawData['data'][id_tender]
        # self.rawData['data'][id_tender][id_subtender]['tender'] => data about subtender
        # self.rawData['data'][id_tender][id_subtender]['award'] => data about awarded company

        # init data varable
        # init data varable

        self.rawData['head'] = {}
        self.rawData['head']['tender'] = tendersData['head']
        self.rawData['head']['award'] = awardsData['head']

        self.rawData['data'] = {}

        # assign awards data into a dataset
        # assign awards data into a dataset

        id_tender_n = self.rawData['head']['award'].index('IDIzpObrazca')
        id_subtender_n = self.rawData['head']['award'].index('IDIzpPriloge')

        for awardsRow in awardsData['data']:

            id_tender = awardsRow[id_tender_n]
            id_subtender = awardsRow[id_subtender_n]

            # init vars
            # init vars

            if id_tender not in self.rawData['data']:
                self.rawData['data'][id_tender] = {}

            if id_subtender not in self.rawData['data'][id_tender]:
                self.rawData['data'][id_tender][id_subtender] = {}
                self.rawData['data'][id_tender][id_subtender]['tender'] = []
                self.rawData['data'][id_tender][id_subtender]['award'] = []

            # add data
            # add data

            self.rawData['data'][id_tender][id_subtender]['award'].append(awardsRow)

        # add tender data
        # add tender data

        id_tender_n = self.rawData['head']['tender'].index('IDIzpObrazca')
        id_subtender_n = self.rawData['head']['tender'].index('IDIzpPriloge')

        for tenderRow in tendersData['data']:

            id_tender = tenderRow[id_tender_n]
            id_subtender = tenderRow[id_subtender_n]

            # non-existing tender - trigger an alert
            # non-existing tender - trigger an alert

            if id_tender not in self.rawData['data']:
                #print("Tender not found: ", id_tender)
                continue

            if id_subtender not in self.rawData['data'][id_tender]:
                #print("Subtender not found: ", id_subtender)
                continue

            # add data
            # add data

            self.rawData['data'][id_tender][id_subtender]['tender'] = tenderRow

        return None

    def convertRaw2OCDS(self):
        '''
        Function converts raw data in ocds format stored in self.ocdsJsonObj

        :return: void
        '''

        # continue if data available
        # continue if data available

        if self.missingDataStopScript:
            return None

        # continue
        # continue

        now = self.conf.datetime.date.today()

        self.ocdsJsonObj['version'] = "1.1"
        self.ocdsJsonObj['uri'] = self.conf.baseUrl + 'TO-BE-UPDATED'
        self.ocdsJsonObj['publishedDate'] = self.convertDate2OcdsDate(now.strftime('%Y-%m-%d %H:%M:%S'))
        self.ocdsJsonObj['publisher'] = {}
        self.ocdsJsonObj['license'] = 'http://opendatacommons.org/licenses/pddl/1.0/'
        self.ocdsJsonObj['publicationPolicy'] = 'https://github.com/open-contracting/sample-data/'
        self.ocdsJsonObj['releases'] = []

        # add publisher data
        # add publisher data

        publisherData = {}
        publisherData['scheme'] = 'SI-PRS'
        publisherData['uid'] = '2482762000'
        publisherData['name'] = 'Ministry of Public Administration Slovenia'
        publisherData['uri'] = 'https://www.ajpes.si/podjetje/MINISTRSTVO_ZA_JAVNO_UPRAVO?enota=593030&EnotaStatus=1'

        self.ocdsJsonObj['publisher'] = publisherData

        # adding data
        # adding data

        tmp_i = 0
        for tenderId, tenderRow in self.rawData['data'].items():

            # tmp_i += 1
            # if tmp_i == 2:
            #     break

            # init curent release
            # init curent release

            curr_release = {}
            curr_release['ocid'] = self.ocdsId
            curr_release['id'] = ''
            curr_release['date'] = ''
            curr_release['tag'] = ['award']
            curr_release['initiationType'] = 'tender'
            curr_release['parties'] = []
            curr_release['buyer'] = {}
            curr_release['planning'] = {}
            curr_release['tender'] = {}
            curr_release['awards'] = []
            curr_release['contracts'] = []

            companyIdsList = []
            tendererIdsList = []
            numFieldsHead = len(self.rawData['head']['tender'])
            for subtenderId, subtenderRow in tenderRow.items():

                # for some reason it may happen that the reader reads an empty vector => that case needs to be ignored
                # for some reason it may happen that the reader reads an empty vector => that case needs to be ignored

                numFieldsData = len(subtenderRow['tender'])
                if numFieldsHead != numFieldsData:
                   return curr_release

                # all good, continue
                # all good, continue

                # set release id & date only once
                # set release id & date only once

                curr_release = self.addIdAndDate2Release(curr_release, subtenderRow)

                # create party-buyer object
                # create party-buyer object

                curr_release = self.addBuyerObj2Release(curr_release, subtenderRow)

                # create party-supplier objects
                # create party-supplier objects

                curr_release, companyIdsList = self.addPartyObj2Release(curr_release, subtenderRow, companyIdsList)

                # set planning object
                # set planning object

                curr_release = self.addPlanningObj2Release(curr_release, subtenderRow)

                # set tender object
                # set tender object

                curr_release, tendererIdsList = self.addTenderObj2Release(curr_release, subtenderRow, tendererIdsList)

                # set awards object
                # set awards object

                curr_release = self.addAwardObj2Release(curr_release, subtenderRow)

                # set contract object
                # set contract object

                curr_release = self.addContractObj2Release(curr_release, subtenderRow)

            # append current release
            # append current release

            self.ocdsJsonObj['releases'].append(curr_release)

        return None

    def addContractObj2Release(self, curr_release, subtenderRow):
        '''
        Function adds contract object to data

        :param curr_release: dictionary
        :param subtenderRow: dictionary
        :return: dictionary
        '''

        curr_contracts = {}

        # set award id
        # set award id

        curr_awards_id_n1 = self.rawData['head']['tender'].index('JNStevilka')
        curr_awards_id_n2 = self.rawData['head']['tender'].index('IDIzpPriloge')

        awardID = self.ocdsId + '-' + subtenderRow['tender'][curr_awards_id_n1] + '-' + subtenderRow['tender'][curr_awards_id_n2]
        contractID = self.ocdsId + '-' + subtenderRow['tender'][curr_awards_id_n1] + '-' + subtenderRow['tender'][curr_awards_id_n2]

        # contract value
        # contract value

        curr_contracts_value_n = self.rawData['head']['tender'].index('KoncnaVrednost')
        curr_contracts_curr_n = self.rawData['head']['tender'].index('KoncnaVrednostValuta')

        curr_contracts_value = {}
        curr_contracts_value['amount'] = self.convertString2Float(subtenderRow['tender'][curr_contracts_value_n])
        curr_contracts_value['currency'] = subtenderRow['tender'][curr_contracts_curr_n]

        # create contract categories
        # create contract categories

        curr_contract_items = {}
        curr_contract_items_unit = {}
        curr_contract_items_unit_val = {}

        curr_contract_items_unit_val['amount'] = self.convertString2Float(curr_contracts_value['amount'])
        curr_contract_items_unit_val['currency'] = curr_contracts_value['currency']

        curr_contract_items_unit['value'] = curr_contract_items_unit_val
        curr_contract_items['id'] = 1
        curr_contract_items['unit'] = curr_contract_items_unit

        # contracts date
        # contracts date

        curr_contracts_date_n = self.rawData['head']['tender'].index('DatumOddajeSklopa')
        curr_contracts['dateSigned'] = self.convertDate2OcdsDate(subtenderRow['tender'][curr_contracts_date_n])

        # contracts data assembly
        # contracts data assembly

        curr_contracts['id'] = contractID
        curr_contracts['awardID'] = awardID
        curr_contracts['value'] = curr_contracts_value
        curr_contracts['items'] = []
        curr_contracts['items'].append(curr_contract_items)
        curr_release['contracts'].append(curr_contracts)

        return curr_release

    def addAwardObj2Release(self, curr_release, subtenderRow):
        '''
        Function adds award object to data

        :param curr_release: dictionary
        :param subtenderRow: dictionary
        :return: dictionary
        '''

        curr_awards_id_n1 = self.rawData['head']['tender'].index('JNStevilka')
        curr_awards_id_n2 = self.rawData['head']['tender'].index('IDIzpPriloge')
        curr_awards_date_n = self.rawData['head']['tender'].index('DatumOddajeSklopa')

        curr_awards = {}
        curr_awards['id'] = subtenderRow['tender'][curr_awards_id_n1] + '-' + subtenderRow['tender'][curr_awards_id_n2]
        curr_awards['date'] = self.convertDate2OcdsDate(subtenderRow['tender'][curr_awards_date_n])

        # award value
        # award value

        curr_award_value_amnt_n = self.rawData['head']['tender'].index('KoncnaVrednost')
        curr_award_value_curr_n = self.rawData['head']['tender'].index('KoncnaVrednostValuta')

        curr_award_value = {}
        curr_award_value['amount'] = self.convertString2Float(subtenderRow['tender'][curr_award_value_amnt_n])
        curr_award_value['currency'] = subtenderRow['tender'][curr_award_value_curr_n]

        # award suppliers
        # award suppliers

        curr_award_supplier_name_n = self.rawData['head']['award'].index('PonudnikOrganizacija')
        curr_award_supplier_id_n = self.rawData['head']['award'].index('PonudnikMaticna')

        curr_award_supplier_list = []
        curr_award_supplier_ids_list = []
        for currAwards in subtenderRow['award']:

            # do not add supplier to the list if already there
            # do not add supplier to the list if already there
            supplier_id = currAwards[curr_award_supplier_id_n]
            if supplier_id in curr_award_supplier_ids_list:
                continue
            else:
                curr_award_supplier_ids_list.append(supplier_id)

            curr_award_supplier = {}
            curr_award_supplier['id'] = supplier_id
            curr_award_supplier['name'] = currAwards[curr_award_supplier_name_n]

            # curr_award_supplier['identifier'] = {}
            # curr_award_supplier['identifier']['id'] = currAwards[curr_award_supplier_id_n]
            # curr_award_supplier['identifier']['legalName'] = currAwards[curr_award_supplier_name_n]

            # Address should be defined only in /parties section. Otherwise the ocds review tool, available at
            # https://standard.open-contracting.org/review/ returns a warning:
            # From version 1.1, organizations should be referenced by their identifier and name in a document, and address
            # information should only be provided in the relevant cross-referenced entry in the parties
            # section at the top level of a release.

            # curr_award_supplier_address_street_n = self.rawData['head']['award'].index('PonudnikNaslov')
            # curr_award_supplier_address_locality_n = self.rawData['head']['award'].index('PonudnikKraj')
            # curr_award_supplier_address_post_n = self.rawData['head']['award'].index('PonudnikPostnaStevilka')
            # curr_award_supplier_address_country_n = self.rawData['head']['award'].index('PonudnikDrzava')
            # curr_award_supplier_address = {}
            # curr_award_supplier_address['streetAddress'] = currAwards[curr_award_supplier_address_street_n]
            # curr_award_supplier_address['locality'] = currAwards[curr_award_supplier_address_locality_n]
            # #curr_award_supplier_address['region'] = ''
            # curr_award_supplier_address['postalCode'] = currAwards[curr_award_supplier_address_post_n]
            # curr_award_supplier_address['countryName'] = currAwards[curr_award_supplier_address_country_n]
            # curr_award_supplier['address'] = curr_award_supplier_address

            # curr_award_supplier_contact = {}
            # curr_award_supplier_contact['name'] = ''
            # curr_award_supplier_contact['email'] = ''
            # curr_award_supplier_contact['telephone'] = ''
            # curr_award_supplier['contactPoint'] = curr_award_supplier_contact

            # add to the list of suppliers
            # add to the list of suppliers

            curr_award_supplier_list.append(curr_award_supplier)

        curr_award_items_desc_n = self.rawData['head']['tender'].index('OpisNarocilaNarocnik')
        curr_award_items_class_desc_n = self.rawData['head']['tender'].index('CPV_NaslovObjave')

        curr_award_items = {}
        curr_award_items['id'] = 1
        curr_award_items['description'] = subtenderRow['tender'][curr_award_items_desc_n]
        curr_award_items['classification'] = {}
        curr_award_items['classification']['description'] = subtenderRow['tender'][curr_award_items_class_desc_n]

        curr_award_items_unit_name_n = self.rawData['head']['tender'].index('ObrazecPredmetSklop_Naslov')
        curr_award_items_unit_amnt_n = self.rawData['head']['tender'].index('KoncnaVrednost')
        curr_award_items_unit_curr_n = self.rawData['head']['tender'].index('KoncnaVrednostValuta')

        curr_award_items_unit = {}
        curr_award_items_unit['name'] = subtenderRow['tender'][curr_award_items_unit_name_n]
        curr_award_items_unit['value'] = {}
        curr_award_items_unit['value']['amount'] = self.convertString2Float(subtenderRow['tender'][curr_award_items_unit_amnt_n])
        curr_award_items_unit['value']['currency'] = subtenderRow['tender'][curr_award_items_unit_curr_n]
        curr_award_items['unit'] = curr_award_items_unit

        # award data assembly
        # award data assembly

        curr_awards['value'] = curr_award_value
        curr_awards['suppliers'] = curr_award_supplier_list
        curr_awards['items'] = []
        curr_awards['items'].append(curr_award_items)
        curr_release['awards'].append(curr_awards)

        return curr_release

    def addTenderObj2Release(self, curr_release, subtenderRow, tendererIdsList):
        '''
        Function adds tender object to data

        :param curr_release: dictionary
        :param subtenderRow: dictionary
        :return: dictionary
        '''

        # init tender
        # init tender

        tender_id_n = self.rawData['head']['tender'].index('JNStevilka')
        tender_title_n = self.rawData['head']['tender'].index('NaslovNarocilaNarocnik')
        tender_description_n = self.rawData['head']['tender'].index('OpisNarocilaNarocnik')

        curr_release_tender_is_new = False
        if len(curr_release['tender']) == 0:
            curr_tender = {}
            curr_tender['id'] = subtenderRow['tender'][tender_id_n]
            curr_tender['title'] = subtenderRow['tender'][tender_title_n]
            curr_tender['description'] = subtenderRow['tender'][tender_description_n]
            curr_release_tender_is_new = True
        else:
            curr_tender = curr_release['tender']

        # tender - procuring object
        # tender - procuring object

        if curr_release_tender_is_new:
            curr_procuring_entity = {}
            curr_procuring_entity['id'] = curr_release['buyer']['id']
            curr_procuring_entity['name'] = curr_release['buyer']['name']

            # tender - procuring identifier
            # tender - procuring identifier

            curr_procuring_entity_identifier = {}
            curr_procuring_entity_identifier['id'] = curr_release['buyer']['id']
            curr_procuring_entity_identifier['legalName'] = curr_release['buyer']['name']

            # tender - procuring address
            # tender - procuring address

            # Address should be defined only in /parties section. Otherwise the ocds review tool, available at
            # https://standard.open-contracting.org/review/ returns a warning:
            # From version 1.1, organizations should be referenced by their identifier and name in a document, and address
            # information should only be provided in the relevant cross-referenced entry in the parties
            # section at the top level of a release.

            # curr_procuring_entity_address = {}
            # curr_procuring_entity_address['streetAddress'] = curr_release['buyer']['address']['streetAddress']
            # curr_procuring_entity_address['locality'] = curr_release['buyer']['address']['locality']
            # curr_procuring_entity_address['region'] = curr_release['buyer']['address']['region']
            # curr_procuring_entity_address['postalCode'] = curr_release['buyer']['address']['postalCode']
            # curr_procuring_entity_address['countryName'] = curr_release['buyer']['address']['countryName']

            # tender - procuring contact
            # tender - procuring contact

            # procuring_entity_contact_name_n = self.rawData['head']['tender'].index('NarocnikKontaktTocka')
            # procuring_entity_contact_email_n = self.rawData['head']['tender'].index('Narocnik_Email')
            # procuring_entity_contact_telephone_n = self.rawData['head']['tender'].index('Narocnik_Telefon')

            #curr_procuring_entity_contact = {}
            #curr_procuring_entity_contact['name'] = ''
            #curr_procuring_entity_contact['email'] = ''
            #curr_procuring_entity_contact['telephone'] = ''

        # tender - items
        # tender - items

        curr_tender_item = {}

        subtender_id_n1 = self.rawData['head']['tender'].index('JNStevilka')
        subtender_id_n2 = self.rawData['head']['tender'].index('IDIzpPriloge')
        curr_tender_item['id'] = self.ocdsId + '-' + subtenderRow['tender'][subtender_id_n1]  + '-' + subtenderRow['tender'][subtender_id_n2]

        #tender_item_description_n = self.rawData['head']['tender'].index('OpisNarocilaNarocnik')
        tender_item_description_n = self.rawData['head']['tender'].index('NaslovSklopa')
        curr_tender_item['description'] = subtenderRow['tender'][tender_item_description_n]

        # tender - classification
        # tender - classification

        #tender/items/classification
        #tender/items/classification/scheme
        #tender/items/classification/id V JSON-U NI TE ZNAČKE AMPAK 'TITLE', KI PA JE TU NI
        #tender/items/classification/description
        #tender/items/classification/uri

        tender_item_class_cpv_id_n = self.rawData['head']['tender'].index('CPV_glavni')
        tender_item_class_cpv_desc_n = self.rawData['head']['tender'].index('CPV_NaslovObjave')

        curr_tender_item_classification = {}
        curr_tender_item_classification['id'] = subtenderRow['tender'][tender_item_class_cpv_id_n]
        curr_tender_item_classification['uri'] = 'http://cpv.data.ac.uk/code-' + subtenderRow['tender'][tender_item_class_cpv_id_n] + '.html'
        curr_tender_item_classification['scheme'] = 'CPV'
        curr_tender_item_classification['description'] = subtenderRow['tender'][tender_item_class_cpv_desc_n]

        # tender - unit
        # tender - unit

        tender_item_unit_name_n = self.rawData['head']['tender'].index('NaslovSklopa')
        tender_item_unit_val_amnt_n = self.rawData['head']['tender'].index('OcenjenaVrednost')
        tender_item_unit_val_curr_n = self.rawData['head']['tender'].index('OcenjenaVrednostValuta')

        curr_tender_item_unit = {}
        curr_tender_item_unit['name'] = subtenderRow['tender'][tender_item_unit_name_n]
        curr_tender_item_unit['value'] = {}
        curr_tender_item_unit['value']['amount'] = self.convertString2Float(subtenderRow['tender'][tender_item_unit_val_amnt_n])
        curr_tender_item_unit['value']['currency'] = subtenderRow['tender'][tender_item_unit_val_curr_n]
        curr_tender_item['classification'] = curr_tender_item_classification
        curr_tender_item['unit'] = curr_tender_item_unit

        #curr_tender_item_list = []
        #curr_tender_item_list.append(curr_tender_item)

        # tender - value
        # tender - value

        tender_item_unit_val_amnt_n = self.rawData['head']['tender'].index('OcenjenaVrednost')
        tender_item_unit_val_amnt = self.convertString2Float(subtenderRow['tender'][tender_item_unit_val_amnt_n])

        if curr_release_tender_is_new:
            tender_item_unit_val_curr_n = self.rawData['head']['tender'].index('OcenjenaVrednostValuta')

            curr_tender_value = {}
            curr_tender_value['amount'] = tender_item_unit_val_amnt
            curr_tender_value['currency'] = subtenderRow['tender'][tender_item_unit_val_curr_n]
        else:
            curr_tender_value = curr_release['tender']['value']
            curr_tender_value['amount'] = curr_tender_value['amount'] + tender_item_unit_val_amnt
            #print(curr_release)

        # tender procurement method
        # tender procurement method

        curr_tender_procur_details_n = self.rawData['head']['tender'].index('VrstaPostopka')
        curr_tender_procur_category_n = self.rawData['head']['tender'].index('VrstaNarocila')

        curr_tender['procurementMethodDetails'] = subtenderRow['tender'][curr_tender_procur_details_n]
        curr_tender['mainProcurementCategory'] = self.getMainProcurementCategory(subtenderRow['tender'][curr_tender_procur_category_n])

        # tender award details
        # tender award details

        curr_tender_award_details_n = self.rawData['head']['tender'].index('Merila')
        curr_tender_submission_details_n = self.rawData['head']['tender'].index('ElektronskaDrazba')

        curr_tender['awardCriteriaDetails'] = subtenderRow['tender'][curr_tender_award_details_n]
        curr_tender['submissionMethodDetails'] = subtenderRow['tender'][curr_tender_submission_details_n]

        # tender - tenderers
        # tender - tenderers

        tendererList = []
        for currAwards in subtenderRow['award']:

            curr_tender_tenderere_name_n = self.rawData['head']['award'].index('PonudnikOrganizacija')
            curr_tender_tenderere_id_n = self.rawData['head']['award'].index('PonudnikMaticna')

            curr_tenderer = {}
            curr_tenderer['name'] = currAwards[curr_tender_tenderere_name_n]
            curr_tenderer['id'] = currAwards[curr_tender_tenderere_id_n]

            # company can make it to the list only once
            # company can make it to the list only once

            if curr_tenderer['id'] in tendererIdsList:
                continue
            else:
                tendererIdsList.append(curr_tenderer['id'])

            # tender - tenderer identifier
            # tender - tenderer identifier

            #curr_tenderer_identifier = {}
            #curr_tenderer_identifier['legalName'] = currAwards[curr_tender_tenderere_name_n]

            # tender - tenderer address
            # tender - tenderer address

            # Address should be defined only in /parties section. Otherwise the ocds review tool, available at
            # https://standard.open-contracting.org/review/ returns a warning:
            # From version 1.1, organizations should be referenced by their identifier and name in a document, and address
            # information should only be provided in the relevant cross-referenced entry in the parties
            # section at the top level of a release.

            # curr_tender_tenderere_street_n = self.rawData['head']['award'].index('PonudnikNaslov')
            # curr_tender_tenderere_locality_n = self.rawData['head']['award'].index('PonudnikKraj')
            # curr_tender_tenderere_post_n = self.rawData['head']['award'].index('PonudnikPostnaStevilka')
            # curr_tender_tenderere_country_n = self.rawData['head']['award'].index('PonudnikDrzava')
            #
            # curr_tenderer_address = {}
            # curr_tenderer_address['streetAddress'] = currAwards[curr_tender_tenderere_street_n]
            # curr_tenderer_address['locality'] = currAwards[curr_tender_tenderere_locality_n]
            # curr_tenderer_address['postalCode'] = currAwards[curr_tender_tenderere_post_n]
            # curr_tenderer_address['countryName'] = currAwards[curr_tender_tenderere_country_n]

            #curr_tenderer['identifier'] = curr_tenderer_identifier
            #curr_tenderer['address'] = curr_tenderer_address

            # create tenderer object
            # create tenderer object

            tendererList.append(curr_tenderer)

        # tender - data assembly
        # tender - data assembly

        if curr_release_tender_is_new:
            #curr_procuring_entity['identifier'] = curr_procuring_entity_identifier
            #curr_procuring_entity['address'] = curr_procuring_entity_address
            #curr_procuring_entity['contactPoint'] = curr_procuring_entity_contact
            curr_tender['procuringEntity'] = curr_procuring_entity

        if 'items' not in curr_tender:
            curr_tender['items'] = []
        curr_tender['items'].append(curr_tender_item)
        # the amount need to be summarized
        curr_tender['value'] = curr_tender_value

        if curr_release_tender_is_new:
            curr_tender['tenderers'] = []
        else:
            curr_release['tender']['tenderers'] = curr_tender['tenderers']
        curr_tender['tenderers'] = curr_tender['tenderers'] + tendererList

        # set release
        # set release

        curr_release['tender'] = curr_tender
        return curr_release, tendererIdsList

    def addPlanningObj2Release(self, curr_release, subtenderRow):
        '''
        Function adds planning object to data; planning budget amount is summarized over several lots

        :param curr_release: dictionary
        :param subtenderRow: dictionary
        :return: dictionary
        '''

        plan_bdg_amount_n = self.rawData['head']['tender'].index('OcenjenaVrednost')
        planning_amount = self.convertString2Float(subtenderRow['tender'][plan_bdg_amount_n])

        if len(curr_release['planning']) == 0:

            plan_bdg_curr_n = self.rawData['head']['tender'].index('OcenjenaVrednostValuta')

            curr_planning_bdg = {}
            curr_planning_bdg['amount'] = {}
            curr_planning_bdg['amount']['amount'] = planning_amount
            curr_planning_bdg['amount']['currency'] = subtenderRow['tender'][plan_bdg_curr_n]

            plan_doc_url_n = self.rawData['head']['tender'].index('wwwObjave')
            plan_doc_date_n = self.rawData['head']['tender'].index('DatumOddajeSklopa')

            curr_planning_docs = {}
            curr_planning_docs['id'] = 1
            curr_planning_docs['url'] = subtenderRow['tender'][plan_doc_url_n]
            #curr_planning_docs['datePublished'] = self.convertDate2OcdsDate(subtenderRow['tender'][plan_doc_date_n])
            curr_planning_docs['datePublished'] = self.convertDate2OcdsDate(subtenderRow['tender'][plan_doc_date_n])

            curr_planning = {}
            curr_planning['budget'] = curr_planning_bdg
            curr_planning['documents'] = []
            curr_planning['documents'].append(curr_planning_docs)
            curr_release['planning'] = curr_planning
        else:
            curr_release['planning']['budget']['amount']['amount'] = curr_release['planning']['budget']['amount']['amount'] + planning_amount

        return curr_release

    def addPartyObj2Release(self, curr_release, subtenderRow, companyIdsList):
        '''
        Function adds buyer object to data

        :param curr_release: dictionary
        :param subtenderRow: dictionary
        :param companyIdsList: list of companies already added to the list
        :return: dictionary
        '''

        for currAward in subtenderRow['award']:

            # start assembling current party
            # start assembling current party

            curr_party = {}

            legalId_n = self.rawData['head']['award'].index('PonudnikMaticna')
            curr_party['id'] = currAward[legalId_n]

            # company can be added only once
            # company can be added only once

            if curr_party['id'] in companyIdsList:
                continue
            else:
                companyIdsList.append(curr_party['id'])

            # all is good, continue
            # all is good, continue

            legalName_n = self.rawData['head']['award'].index('PonudnikOrganizacija')
            curr_party['name'] = currAward[legalName_n]

            curr_party['roles'] = []
            curr_party['roles'].append('supplier')

            # set bidder identifier
            # set bidder identifier

            legalName_n = self.rawData['head']['award'].index('PonudnikOrganizacija')

            cur_identifier = {}
            cur_identifier['id'] = curr_party['id']
            cur_identifier['legalName'] = curr_party['name']

            # set bider name
            # set bider name

            curr_party['name'] = cur_identifier['legalName']

            # set bidder address
            # set bidder address

            streetAddress_n = self.rawData['head']['award'].index('PonudnikNaslov')
            locality_n = self.rawData['head']['award'].index('PonudnikKraj')
            region_n = self.rawData['head']['award'].index('Ponudnik_Regija')
            postalCode_n = self.rawData['head']['award'].index('PonudnikPostnaStevilka')
            countryName_n = self.rawData['head']['award'].index('PonudnikDrzava')

            cur_address = {}
            cur_address['streetAddress'] = currAward[streetAddress_n]
            cur_address['locality'] = currAward[locality_n]
            cur_address['region'] = currAward[region_n]
            cur_address['postalCode'] = currAward[postalCode_n]
            cur_address['countryName'] = currAward[countryName_n]

            # set contact point
            # set contact point

            # name_n = self.rawData['head']['tender'].index('NarocnikKontaktTocka')
            # email_n = self.rawData['head']['tender'].index('Narocnik_Email')
            # telephone_n = self.rawData['head']['tender'].index('Narocnik_Telefon')

            # cur_contact = {}
            # cur_contact['name'] = ''
            # cur_contact['email'] = ''
            # cur_contact['telephone'] = ''

            # assemble bidder data
            # assemble bidder data

            curr_party['identifier'] = cur_identifier
            curr_party['address'] = cur_address
            #curr_party['contactPoint'] = cur_contact
            curr_release['parties'].append(curr_party)

        return curr_release, companyIdsList

    def addBuyerObj2Release(self, curr_release, subtenderRow):
        '''
        Function adds buyer object to data

        :param curr_release: dictionary
        :param subtenderRow: dictionary
        :return: dictionary
        '''

        # add buyer only once
        # add buyer only once

        if len(curr_release['buyer']) == 0:

            buyer = {}
            party_id_n = self.rawData['head']['tender'].index('NarocnikMaticna')
            buyer['id'] = subtenderRow['tender'][party_id_n]
            legalName_n = self.rawData['head']['tender'].index('NarocnikOrganizacija')
            buyer['name'] = subtenderRow['tender'][legalName_n]
            buyer['roles'] = []
            buyer['roles'].append('buyer')

            # set buyer identifier
            # set buyer identifier

            cur_identifier = {}
            cur_identifier['id'] = buyer['id']
            cur_identifier['legalName'] = buyer['name']

            # set buyer address
            # set buyer address

            streetAddress_n = self.rawData['head']['tender'].index('NarocnikNaslov')
            locality_n = self.rawData['head']['tender'].index('NarocnikKraj')
            # region_n = self.rawData['head']['tender'].index('Narocnik_id_SifNuts_Koda')
            region_n = self.rawData['head']['tender'].index('Narocnik_Regija')
            postalCode_n = self.rawData['head']['tender'].index('NarocnikPostnaStevilka')

            cur_address = {}
            cur_address['streetAddress'] = subtenderRow['tender'][streetAddress_n]
            cur_address['locality'] = subtenderRow['tender'][locality_n]
            cur_address['region'] = subtenderRow['tender'][region_n]
            cur_address['postalCode'] = subtenderRow['tender'][postalCode_n]
            cur_address['countryName'] = 'Slovenia'

            # set contact point
            # set contact point

            # name_n = self.rawData['head']['tender'].index('NarocnikKontaktTocka')
            # email_n = self.rawData['head']['tender'].index('Narocnik_Email')
            # telephone_n = self.rawData['head']['tender'].index('Narocnik_Telefon')

            # cur_contact = {}
            # cur_contact['name'] = ''
            # cur_contact['email'] = subtenderRow[email_n]
            # cur_contact['telephone'] = subtenderRow[telephone_n]

            # set buyer object
            # set buyer object

            curr_party = {}
            curr_party['id'] = buyer['id']
            curr_party['name'] = cur_identifier['legalName']
            #curr_party['identifier'] = cur_identifier
            #curr_party['address'] = cur_address
            # curr_party['contactPoint'] = cur_contact
            curr_release['buyer'] = curr_party

            # add buyer among parties
            # add buyer among parties

            buyer['identifier'] = cur_identifier
            buyer['address'] = cur_address
            # buyer['contactPoint'] = cur_contact
            curr_release['parties'].append(buyer)

        return curr_release

    def addIdAndDate2Release(self, curr_release, subtenderRow):
        '''
        Function adds id & release date to tender data

        :param curr_release: dictionary
        :param subtenderRow: dictionary
        :return: dictionary
        '''

        # add data only once
        # add data only once

        if len(curr_release['id']) == 0:

            id_n = self.rawData['head']['tender'].index('JNStevilka')
            id_val = subtenderRow['tender'][id_n]
            curr_release['id'] = self.ocdsId + "-" + id_val

            party_date_n = self.rawData['head']['tender'].index('DatumObjaveObvestila')
            curr_release['date'] = self.convertDate2OcdsDate(subtenderRow['tender'][party_date_n])

        return curr_release

    def convertString2Float(self, stringValue, thousandSepareator = '.', decimalSeparator = ','):
        '''
        function takes in stringValue and converts it into float value

        :param stringValue:
        :return: float
        '''

        if stringValue == '':
            return 0.0

        if isinstance(stringValue, float):
            return stringValue

        stringNoThousand = stringValue.replace(thousandSepareator, "")
        return float(stringNoThousand.replace(decimalSeparator, "."))

    def convertDate2OcdsDate(self, dateString):
        '''
        Function takes in date in format 'YYYY-MM-DD HH:MM:SS' and returns 'YYYY-MM-DDYHH:MM:SSZ'

        :return: formated date
        '''

        dateLength = len(dateString)
        if dateLength == 10:
            if dateString.find('-'):
                date_time_obj = self.conf.datetime.datetime.strptime(dateString, '%Y-%m-%d')
            else:
                date_time_obj = self.conf.datetime.datetime.strptime(dateString, '%d/%m/%Y')
        elif dateLength == 16:
            date_time_obj = self.conf.datetime.datetime.strptime(dateString, '%d/%m/%Y %H:%M')
        else:
            date_time_obj = self.conf.datetime.datetime.strptime(dateString, '%Y-%m-%d %H:%M:%S')

        dateString = str(date_time_obj)
        dateString = dateString.replace(' ', 'T')

        return dateString + 'Z'

    def listOfDictsContainsValue(self, key, value, listOfDicts):
        '''
        Function returns true if exists listOfDicts[][key] = value

        :return: boolean
        '''

        for dict in listOfDicts:
            if dict[key] == value:
                return True

        return False

    def exportOcdsJson2File(self):
        '''
        Function saves ocds data into a file

        :return: void
        '''

        # export only if there is anything to export
        # export only if there is anything to export

        if len(self.ocdsJsonObj) == 0:
            return None

        # continue export
        # continue export

        ocdsDataFileName = self.ocdsDataFileName.replace('DATE', self.dateString)

        filePath = self.conf.os.path.join(self.ocdsDataFilePath, ocdsDataFileName)
        json_data = self.conf.json.dumps(self.ocdsJsonObj)

        myfile = open(filePath, "w+")
        myfile.write(json_data)

        return None

    def getMainProcurementCategory(self, parameter):
        '''
        function takes in VrstaNarocila field from MJU database and returns OCDS cirrect definition

        :param parmeter: string, VrstaNarocila value
        :return: string, OCDS definition
        '''

        parameter = parameter.lower()

        if parameter == 'blago':
            return 'goods'
        elif parameter == 'storitve':
            return 'services'
        else:
            return 'works'

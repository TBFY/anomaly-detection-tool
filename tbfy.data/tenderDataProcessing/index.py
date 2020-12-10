
# enabling shell exec from any directory
# enabling shell exec from any directory

import os
workingDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../')

import sys
sys.path.append(workingDir)

# configure params
# configure params

import config_data as conf
import SharedDataMethods as Shared

sharedMethods = Shared.SharedDataMethods(conf)

# for testing purposes to turn on/off specific tasks
# for testing purposes to turn on/off specific tasks

dateString              = '20200611'
dateStringKG            = '2019-01-03'
testModeON              = False
exe_task_mju_download   = True
exe_task_mju2ocds       = True
exe_task_mju2fv         = True
exe_task_kg2fv          = True


# ************************************************************* #
# ************************************************************* #
# *********** download MJU tender data to localhost *********** #
# *********** download MJU tender data to localhost *********** #
# ************************************************************* #
# ************************************************************* #

if exe_task_mju_download:
    print('MJU Data transfer to IJS script start')
    print('')

    import DownloadMJUData2Localhost as MJU2Lh

    dataDL = MJU2Lh.DownloadMJUData2Localhost(conf, sharedMethods)
    if testModeON:
        print('ALERT! TEST MODE ON.')
        dataDL.dateString = dateString
    dataDL.connect2MJU()
    dataDL.downloadDailyUpdate()
    dataDL.disconnect()


# ************************************************************* #
# ************************************************************* #
# *********** MJU raw data 2 OCDS format conversion *********** #
# *********** MJU raw data 2 OCDS format conversion *********** #
# ************************************************************* #
# ************************************************************* #
# ocds example: https://standard.open-contracting.org/latest/en/implementation/amendments/#worked-example


if exe_task_mju2ocds:
    print('MJU Data conversion into OCDS format script start')
    print('')

    import MJUData2OCDSConversion as Raw2OCDS

    createOcds = Raw2OCDS.MJUData2OCDSConversion(conf, sharedMethods)
    if testModeON:
        print('ALERT! TEST MODE ON.')
        createOcds.dateString = dateString
    createOcds.convertRawFiles2OCDS()


# ************************************************************************* #
# ************************************************************************* #
# *********** MJU raw data 2 feature vectors formats conversion *********** #
# *********** MJU raw data 2 feature vectors formats conversion *********** #
# ************************************************************************* #
# ************************************************************************* #


if exe_task_mju2fv:
    print('MJU raw data conversion into feature vectors')
    print('')

    import MJURaw2FeatureVectors as Raw2FV

    ##   CONVERSION 1: MJU raw data 2 full feature vectors   ##
    ##   CONVERSION 1: MJU raw data 2 full feature vectors   ##

    selectedFieldList = {
        'IDIzpObrazca': 'int',
        'DatumObjaveObvestila': 'datetime',
        'NarocnikMaticna': 'str',
        'Narocnik_OBCINA': 'cat',
        'Narocnik_Oblika': 'cat',
        'Narocnik_Glavna_Dejavnost_SKD': 'cat',
        'Narocnik_Velik_RS': 'nempl_byr_rs',
        'Narocnik_Velik_EU': 'nempl_byr',
        'Narocnik_Regija': 'cat',
        'Narocnik_Dejavnost': 'cat',
        'VrstaNarocila': 'cat',
        'VrstaPostopka': 'cat',
        'VrstaPostopka_EU': 'cat',
        'Merila': 'cat',
        'OkvirniSporazum': '',
        'SkupnoNarocanje': 'cat',
        'EUsredstva': 'cat',
        'ObjavaVEU': 'cat',
        'StPrejetihPonudb': 'int',
        'SkupnaPonudba': 'cat',
        'OcenjenaVrednost': 'float',
        'OcenjenaVrednostValuta': 'cat',
        'KoncnaVrednost': 'float',
        'KoncnaVrednostValuta': 'cat',
        'OddanoPodizvajalcem': 'cat',
        'CPV_glavni': 'int',
        'CPV_glavni_2mesti': 'int',
        'Podrocje': 'cat',
        'VrstaPostopkaIzracunan': 'cat',
        'NarocnikPostnaStevilka': 'str',
        'PonudnikMaticna': 'str',
        'PonudnikPostnaStevilka': 'str',
        'Ponudnik_OBCINA': 'cat',
        'Ponudnik_Velik_EU': 'nempl_bidr',
        'Ponudnik_Velik_RS': 'nempl_bidr_rs'
    }
    entryOverlapInstructions = {}

    createFeatureVectors = Raw2FV.MJURaw2FeatureVectors(conf, sharedMethods)
    if testModeON:
        print('ALERT! TEST MODE ON.')
        createFeatureVectors.dateString = dateString
    createFeatureVectors.setFieldsLists(selectedFieldList, entryOverlapInstructions)
    createFeatureVectors.convertRawFiles('IDIzpObrazca', 'fullFV', sortByFirstField=False, queryDatabase=True)

    ##   CONVERSION 2: MJU raw data 2 stream story feature vectors   ##
    ##   CONVERSION 2: MJU raw data 2 stream story feature vectors   ##

    selectedFieldList = {
        'DatumObjaveObvestila': 'datetime',
        'NarocnikMaticna': 'int',
        'Narocnik_OBCINA': 'cat',
        'Narocnik_Oblika': 'cat',
        'Narocnik_Glavna_Dejavnost_SKD': 'cat',
        'Narocnik_Velik_RS': 'nempl_byr_rs',
        'Narocnik_Velik_EU': 'nempl_byr',
        'Narocnik_Regija': 'cat',
        'Narocnik_Dejavnost': 'cat',
        'VrstaNarocila': 'cat',
        'VrstaPostopka': 'cat',
        'VrstaPostopka_EU': 'cat',
        'Merila': 'cat',
        'OkvirniSporazum': '',
        'SkupnoNarocanje': 'cat',
        'EUsredstva': 'cat',
        'ObjavaVEU': 'cat',
        'StPrejetihPonudb': 'int',
        'SkupnaPonudba': 'cat',
        'OcenjenaVrednost': 'float',
        'OcenjenaVrednostValuta': 'cat',
        'KoncnaVrednost': 'float',
        'KoncnaVrednostValuta': 'cat',
        'OddanoPodizvajalcem': 'cat',
        'CPV_glavni_2mesti': 'int',
        'Podrocje': 'cat',
        'VrstaPostopkaIzracunan': 'cat',
        'PonudnikMaticna': 'str',
        'PonudnikPostnaStevilka': 'str',
        'Ponudnik_OBCINA': 'cat',
        'Ponudnik_Velik_EU': 'nempl_bidr',
        'Ponudnik_Velik_RS': 'nempl_bidr_rs'
    }
    entryOverlapInstructions = {
        'sum': ['OcenjenaVrednost', 'KoncnaVrednost']
    }

    createFeatureVectors = Raw2FV.MJURaw2FeatureVectors(conf, sharedMethods)
    if testModeON:
        print('ALERT! TEST MODE ON.')
        createFeatureVectors.dateString = dateString
    createFeatureVectors.setFieldsLists(selectedFieldList, entryOverlapInstructions)
    createFeatureVectors.convertRawFiles('DatumObjaveObvestila', 'ssFV')

    #createFeatureVectors.readRawFile()
    #createFeatureVectors.convertRaw2FV('DatumObjaveObvestila')
    #createFeatureVectors.save2File('ssFV')


# ************************************************************************* #
# ************************************************************************* #
# *********** TBFY KG data 2 feature vectors formats conversion *********** #
# *********** TBFY KG data 2 feature vectors formats conversion *********** #
# ************************************************************************* #
# ************************************************************************* #

if exe_task_kg2fv:
    print('TBFY KG conversion into feature vectors')
    print('')

    import TbfyKGRawJSON2FeatureVectors as TBFYKG2FV

    kg2fv = TBFYKG2FV.TbfyKGRawJSON2FeatureVectors(conf, sharedMethods)
    if testModeON:
        print('ALERT! TEST MODE ON.')
        kg2fv.rawFilesDirs2ProcessList = [dateStringKG]
    kg2fv.convertRaw2FV()
    kg2fv.save2File()

'''
if exe_task_kg2fv:
    print('TBFY KG conversion into feature vectors')
    print('')

    import TbfyKGRawTTL2FeatureVectors as TBFYKG2FV

    kg2fv = TBFYKG2FV.TbfyKGRawTTL2FeatureVectors(conf, sharedMethods)
    if testModeON:
        print('ALERT! TEST MODE ON.')
        kg2fv.rawFilesDirs2ProcessList = [dateStringKG]
    kg2fv.convertRaw2FV()
    kg2fv.save2File()
'''

# ending script
# ending script

print('')
print("script execution time:")
print("--- %s seconds ---" % (conf.time.time() - conf.start_time))


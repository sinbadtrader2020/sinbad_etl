#!/usr/bin/env python3
import argparse
from pathlib import Path
import configparser
from config import Config

from src.etl.filter import TradingProcessor
from src.sharedobj import SharedObject

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config_path', default='./config.ini', help='Absolute Config Path')
    args = parser.parse_args()

    config_file = Path(args.config_path)
    if not config_file.is_file():
        print("ERROR: Provide valid config file")
        print("You provide '{0}'".format(args.config_path))
        exit(1)

    config = configparser.ConfigParser()
    config.read(args.config_path)

    # [API]
    # COMPANIES = 'https://pkgstore.datahub.io/core/nyse-other-listings/7/datapackage.json'
    # REPORT = 'https://www.alphavantage.co/query'
    # KEY = 'AOYGBU6J7IN09PCE'
    #
    # [LOOKUP]
    # DIRECTORY = '/home/maruf/Documents/tirzokcodebase/sinbad_finance_etl/file/lookup/'

    Config.COMPANIES = config.get('API', 'COMPANIES',
                                  fallback='https://pkgstore.datahub.io/core/nyse-other-listings/7/datapackage.json')

    Config.REPORT = config.get('API', 'REPORT', fallback='https://www.alphavantage.co/query')
    Config.KEY = config.get('API', 'KEY', fallback='AOYGBU6J7IN09PCE')
    Config.DIRECTORY = config.get('LOOKUP', 'DIRECTORY',
                                    fallback='/home/maruf/Documents/tirzokcodebase/sinbad_finance_etl/file/lookup/')

    SharedObject.APP_Config = Config

    processor = TradingProcessor()
    processor.load_companies()
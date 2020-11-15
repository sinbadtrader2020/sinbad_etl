#!/usr/bin/env python3
import argparse
from pathlib import Path
import configparser

from src.dbconn import connection
from src.etl.filter import TradingProcessor
from src.remote.company_loader import CompanyLoader
from src.utils import logger

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

    logger.config_logger(config)

    connection.config_database(config)

    company_loader = CompanyLoader(config)
    company_loader.load_companies()

    processor = TradingProcessor(config)
    processor.load_companies()
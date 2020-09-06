#!/usr/bin/env python3
from src.etl.filter import TradingProcessor

processor = TradingProcessor()
processor.load_companies()


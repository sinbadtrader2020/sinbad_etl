from datetime import datetime
import requests
import socket

from src.etl import common
from src.etl.config import CompliantConfig


class FilterIATR:
    """
    IATR: Illiquid asset to total asset ratio
    """

    def __init__(self, url_string=None, function="", apikey=""):
        if url_string is None \
                or function is None \
                or apikey is None:
            raise Exception("FilterIATR")  # TODO give proper message

        self.formatted_url = common.get_formatted_aaoifi_url(url_string, function, apikey)

    def __call__(self, company=None):
        url = self.formatted_url.format(company.sf_act_symbol)

        try:
            result = requests.get(url)

            data = result.json()
            if not data:
                return CompliantConfig.YELLOW, \
                       common.get_nc_reason_string(common.NonCompliantReasonCode.IATR,
                                                   "No Data ({0})".format(url))

            financial_reports = data.get("quarterlyReports", None)
            if financial_reports is None:
                financial_reports = data["annualReports"]
                print("[CAUSE]", self.__class__.__name__, company.sf_act_symbol, url,
                      "No 'quarterlyReports', used 'annualReports'")

            financial_report_latest = None
            date_latest = datetime.strptime("1970-01-01", '%Y-%m-%d')
            for financial_report in financial_reports:
                date = datetime.strptime(financial_report["fiscalDateEnding"], '%Y-%m-%d')
                if date > date_latest:
                    financial_report_latest = financial_report
                    date_latest = date

            if financial_report_latest is None:
                return CompliantConfig.YELLOW, \
                       common.get_nc_reason_string(common.NonCompliantReasonCode.IATR,
                                                   "Empty Annual or Querterly Reports ({0})".format(url))

            totalAssets = common.get_string_to_float(financial_report_latest["totalAssets"])

            cash = common.get_string_to_float(financial_report_latest["cash"])
            longTermInvestments = common.get_string_to_float(financial_report_latest["longTermInvestments"])
            shortTermInvestments = common.get_string_to_float(financial_report_latest["shortTermInvestments"])
            netReceivables = common.get_string_to_float(financial_report_latest["netReceivables"])
            inventory = common.get_string_to_float(financial_report_latest["inventory"])
            totalLongTermDebt = common.get_string_to_float(financial_report_latest["totalLongTermDebt"])

            company._iatr_totalLongTermDebt = totalLongTermDebt  # will be used in FilterDR
            company._iatr_longTermInvestments = longTermInvestments  # will be used in FilterNIR
            company._iatr_shortTermInvestments = shortTermInvestments  # will be used in FilterNIR

            if totalAssets <= 0:
                return CompliantConfig.YELLOW, \
                       common.get_nc_reason_string(common.NonCompliantReasonCode.IATR,
                                                   "Zero or Negetive 'totalAssets' ({0})".format(url))

            liquid_asset = cash + longTermInvestments + shortTermInvestments + netReceivables + inventory
            illiquid_asset = totalAssets - liquid_asset

            # Business Logic: Illiquid asset to total asset ratio (IATR)
            ratio = illiquid_asset / totalAssets
            if ratio <= 0.3:
                return CompliantConfig.NONCOMPLIANT, \
                       common.get_nc_reason_string(common.NonCompliantReasonCode.IATR,
                                                   "According to Business Logic ({0})".format(url))

        except KeyError as key_error:
            return CompliantConfig.YELLOW, \
                   common.get_nc_reason_string(common.NonCompliantReasonCode.IATR,
                                               "Not found parameter {0} ({1})".format(key_error, url))

        except (TimeoutError, socket.gaierror, ConnectionError, OSError) as  newtork_error:
            return CompliantConfig.NETWORK_ERR, \
                   common.get_nc_reason_string(common.NonCompliantReasonCode.IATR,
                                               "Network problem {0} ({1})".format(newtork_error, url))

        return CompliantConfig.COMPLIANT, common.CMP_CODE

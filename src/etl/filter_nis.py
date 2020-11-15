from datetime import datetime
import requests
import socket
import inspect

from src.etl import common
from src.etl.config import CompliantConfig
from src.utils import logger


class FilterNIS:
    """
    NIS: Non-compliant income source (NIS)
    """

    def __init__(self, url_string=None, function="", apikey=""):
        if url_string is None \
                or function is None \
                or apikey is None:
            raise Exception("FilterNIS")  # TODO give proper message

        self.formatted_url = common.get_formatted_aaoifi_url(url_string, function, apikey)

    def __call__(self, company=None):
        url = self.formatted_url.format(company.sf_act_symbol)

        try:
            result = requests.get(url)

            data = result.json()
            if not data:
                return CompliantConfig.YELLOW, \
                       common.get_nc_reason_string(common.NonCompliantReasonCode.NIS,
                                                   "No Data ({0})".format(url))

            financial_reports = data.get("quarterlyReports", None)
            if financial_reports is None:
                financial_reports = data["annualReports"]
                logger.info("CAUSE --> " + self.__class__.__name__ + ", " +
                            company.sf_act_symbol + ", " + url + ", No 'quarterlyReports', used 'annualReports'")

            financial_report_latest = None
            date_latest = datetime.strptime("1970-01-01", '%Y-%m-%d')
            for financial_report in financial_reports:
                date = datetime.strptime(financial_report["fiscalDateEnding"], '%Y-%m-%d')
                if date > date_latest:
                    financial_report_latest = financial_report
                    date_latest = date

            if financial_report_latest is None:
                return CompliantConfig.YELLOW, \
                       common.get_nc_reason_string(common.NonCompliantReasonCode.NIS,
                                                   "Empty Annual or Querterly Reports ({0})".format(url))

            net_interest_income = common.get_string_to_float(financial_report_latest["netInterestIncome"])
            net_income = common.get_string_to_float(financial_report_latest["netIncome"])

            if net_income <= 0:
                net_income = 0

            if net_interest_income <= 0:
                net_interest_income = 0

            if net_income == 0:
                if net_interest_income == 0:
                    return CompliantConfig.YELLOW, \
                           common.get_nc_reason_string(common.NonCompliantReasonCode.NIS,
                                                   "Zero or Negetive 'netIncome' and 'netInterestIncome' ({0})".format(url))
                else:
                    return CompliantConfig.NONCOMPLIANT, \
                           common.get_nc_reason_string(common.NonCompliantReasonCode.NIS,
                                                   "Zero or Negetive 'netIncome' ({0})".format(url))
            else:
                # Business Logic: Non-compliant Income Source (NIS)
                ratio = net_interest_income / net_income
                if ratio >= 0.05:
                    return CompliantConfig.NONCOMPLIANT, \
                           common.get_nc_reason_string(common.NonCompliantReasonCode.NIS,
                                                       "According to Business Logic ({0})".format(url))

        except KeyError as key_error:
            return CompliantConfig.YELLOW, \
                   common.get_nc_reason_string(common.NonCompliantReasonCode.NIS,
                                               "Not found parameter {0} ({1})".format(key_error, url))

        except (TimeoutError, socket.gaierror, ConnectionError, OSError) as  newtork_error:
            return CompliantConfig.NETWORK_ERR, \
                   common.get_nc_reason_string(common.NonCompliantReasonCode.NIS,
                                               "Network problem {0} ({1})".format(newtork_error, url))
        # except Exception as exception:
        #     print("[ERROR][Exception]", self.__class__.__name__, company.sf_act_symbol, exception, url)
        #     return CompliantConfig.YELLOW, \
        #            common.get_nc_reason_string(common.NonCompliantReasonCode.NIS,
        #                                        "Unknown Exception found: {0} ({1})".format(exception, url))

        return CompliantConfig.COMPLIANT, common.CMP_CODE

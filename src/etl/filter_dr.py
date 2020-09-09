from datetime import datetime
import requests

from src.etl import common


class FilterDR:
    """
    DR: interest bearing debt to total asset ratio
    """

    def __init__(self, url_string=None, function="", apikey=""):
        if url_string is None \
                or function is None \
                or apikey is None:
            raise Exception("FilterDR")  # TODO give proper message

        self.formatted_url = common.get_formatted_aaoifi_url(url_string, function, apikey)

    def __call__(self, company=None):
        url = self.formatted_url.format(company.sf_act_symbol)

        try:
            result = requests.get(url)

            data = result.json()
            if not data:
                return False, \
                       common.get_nc_reason_string(common.NonCompliantReasonCode.DR,
                                                   "No Data ({0})".format(url))

            total_longterm_debt = common.get_string_to_float(company._iatr_totalLongTermDebt)
            market_capitalization = common.get_string_to_float(data["MarketCapitalization"])

            if market_capitalization <= 0:
                return False, \
                       common.get_nc_reason_string(common.NonCompliantReasonCode.DR,
                                                   "Zero or Negetive 'totalLongTermDebt' ({0})".format(url))

            # Business Logic: DR: interest bearing debt to total asset ratio
            ratio = total_longterm_debt / market_capitalization
            if ratio >= 0.3:
                return False, \
                       common.get_nc_reason_string(common.NonCompliantReasonCode.DR,
                                                   "According to Business Logic ({0})".format(url))

        except KeyError as key_error:
            return False, \
                   common.get_nc_reason_string(common.NonCompliantReasonCode.DR,
                                               "Not found parameter {0} ({1})".format(key_error, url))

        return True, common.CMP_CODE

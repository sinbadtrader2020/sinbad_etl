import requests

from src.etl import common
from src.etl.config import CompliantConfig


class FilterDR:
    """
    DR: interest bearing debt to total asset ratio
    Depends on FilterIATR
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
                return CompliantConfig.YELLOW, \
                       common.get_nc_reason_string(common.NonCompliantReasonCode.DR,
                                                   "No Data ({0})".format(url))

            total_longterm_debt = common.get_string_to_float(company._iatr_totalLongTermDebt)
            market_capitalization = common.get_string_to_float(data["MarketCapitalization"])

            if market_capitalization < 0:
                market_capitalization = 0

            if total_longterm_debt < 0:
                total_longterm_debt = -total_longterm_debt

            company._iatr_MarketCapitalization = market_capitalization  # will be used in FilterNIR

            if market_capitalization == 0:
                return CompliantConfig.YELLOW, \
                       common.get_nc_reason_string(common.NonCompliantReasonCode.DR,
                                                   "Zero or Negetive 'MarketCapitalization' ({0})".format(url))

            # Business Logic: DR: interest bearing debt to total asset ratio
            ratio = total_longterm_debt / market_capitalization
            if ratio >= 0.3:
                return CompliantConfig.NONCOMPLIANT, \
                       common.get_nc_reason_string(common.NonCompliantReasonCode.DR,
                                                   "According to Business Logic ({0})".format(url))

        except KeyError as key_error:
            return CompliantConfig.YELLOW, \
                   common.get_nc_reason_string(common.NonCompliantReasonCode.DR,
                                               "Not found parameter {0} ({1})".format(key_error, url))
        # except Exception as exception:
        #     print("[ERROR][Exception]", self.__class__.__name__, company.sf_act_symbol, exception, url)
        #     return CompliantConfig.YELLOW, \
        #            common.get_nc_reason_string(common.NonCompliantReasonCode.DR,
        #                                        "Unknown Exception found: {0} ({1})".format(exception, url))

        return CompliantConfig.COMPLIANT, common.CMP_CODE

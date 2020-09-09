from src.etl import common


class FilterNIR:
    """
    NIR: Non-compliant investment to total asset ratio
    Depends on FilterIATR and FilterDR
    """

    def __call__(self, company=None):

        longterm_investments = common.get_string_to_float(company._iatr_longTermInvestments)
        shortterm_investments = common.get_string_to_float(company._iatr_shortTermInvestments)
        market_capitalization = common.get_string_to_float(company._iatr_MarketCapitalization)

        # Business Logic: NIR: Non-compliant investment to total asset ratio.
        ratio = (longterm_investments + shortterm_investments) / market_capitalization
        if ratio >= 0.33:
            return False, \
                   common.get_nc_reason_string(common.NonCompliantReasonCode.NIR, "According to Business Logic")

        return True, common.CMP_CODE

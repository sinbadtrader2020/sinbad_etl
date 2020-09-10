class DBClassName:
    COMPANY                     = 'sf_companies'


class DBAbstract:
    def get_key_value_format(self):
        """
        Returns those attributes' list, values and str_format for which value is not none and attribute's name does not
        start with '_'. '_' indicates that the attribute is not a table's column.
        :return: str, list, str
        """
        str_keys = ''
        values = list()
        str_format = ''
        for attr, value in self.__dict__.items():
            if value is not None and not attr.startswith('_'):
                if str_keys:
                    str_keys += ', '
                    str_format += ', '

                str_keys += attr
                values.append(value)
                str_format += '%s'

        return str_keys, values, str_format

class Company(DBAbstract):
    def __init__(self,
                 sf_act_symbol=None,
                 sf_company_name=None,
                 sf_security_name=None,
                 sf_exchange=None,
                 sf_cqs_symbol=None,
                 sf_etf=None,
                 sf_round_lot_size=None,
                 sf_test_issue=None,
                 sf_nasdaq_symbol=None,
                 sf_last_screened=None,
                 sf_aaoifi_compliant=None,
                 sf_nc_reason=None,
                 **kwargs):
        self.sf_act_symbol = sf_act_symbol
        self.sf_company_name = sf_company_name
        self.sf_security_name = sf_security_name
        self.sf_exchange = sf_exchange
        self.sf_cqs_symbol = sf_cqs_symbol
        self.sf_etf = sf_etf
        self.sf_round_lot_size = sf_round_lot_size
        self.sf_test_issue = sf_test_issue
        self.sf_nasdaq_symbol = sf_nasdaq_symbol
        self.sf_last_screened = sf_last_screened
        self.sf_aaoifi_compliant = sf_aaoifi_compliant
        self.sf_nc_reason = sf_nc_reason

        # private attributes not POJO
        self._sf_company_id = None

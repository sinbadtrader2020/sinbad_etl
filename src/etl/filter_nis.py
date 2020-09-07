from datetime import datetime
import requests


class FilterNIS:
    """
    NIS: Non-compliant income source (NIS)
    """
    def __init__(self, url_string=None, function="INCOME_STATEMENT", apikey="demo"):
        if url_string is None \
                or function is None \
                or apikey is None:
            raise Exception("FilterNIS") # TODO give proper message

        self.formatted_url = url_string + '?function=' + function + '&symbol={0}' + '&apikey=' + apikey

    def __call__(self, company=None):
        url = self.formatted_url.format(company.sf_act_symbol)
        # url = self.formatted_url.format('IBM')

        try:
            result = requests.get(url)
            data = result.json()
            quarterly_reports = data["quarterlyReports"]

            quarterly_report_latest = None
            date_latest = datetime.strptime("1970-01-01", '%Y-%m-%d')
            for quarterly_report in quarterly_reports:
                date = datetime.strptime(quarterly_report["fiscalDateEnding"], '%Y-%m-%d')
                if date > date_latest:
                    quarterly_report_latest = quarterly_report
                    date_latest = date

                if quarterly_report_latest is None:
                    raise Exception('FilterNIS')

                interest_income_str = quarterly_report_latest["interestIncome"]
                if interest_income_str == 'None':
                    interest_income_str = None

                interest_income = float(interest_income_str or 0)
                net_income = float(quarterly_report_latest["netIncome"])
                ratio = interest_income / net_income

                if ratio < 0.05:
                    company.sf_aaoifi_compliant = False

                    print('Print NIS: Non-compliant income source (NIS) --> ' + url, date)

                    return False
        except KeyError as key_error:
            print(data)
            print(self.__class__.__name__, company.sf_act_symbol, key_error, url)
            # TODO handle exception


        return True
def get_formatted_aaoifi_url(base_url, function, apikey):
    return base_url + '?function=' + function + '&symbol={0}' + '&apikey=' + apikey


CMP_CODE = "COMPLIANT"

class NonCompliantReasonCode:
    NCL = "NCL"
    NIS = "NIS"
    IATR = "IATR"
    DR = "DR"
    NIR = "NIR"

def get_nc_reason_string(reason_code, reason_string=''):
    if reason_string:
        return reason_code + " -> " + reason_string
    return reason_code
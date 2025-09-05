
from get_best_match_rest_sdk_example import get_best_match_rest_sdk_go
from get_best_match_soap_sdk_example import get_best_match_soap_sdk_go

if __name__ =="__main__":

    # Your license key from Service Objects.  
    # Trial license keys will only work on the trial environments and production  
    # license keys will only work on production environments.
    #   
    license_key = "LICENSE KEY"  
    is_live = True

    # FastTax – GetBestMatch - REST SDK
    get_best_match_rest_sdk_go(is_live, license_key)

    # FastTax – GetBestMatch - SOAP SDK
    get_best_match_soap_sdk_go(is_live, license_key)
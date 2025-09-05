import sys
import os

sys.path.insert(0, os.path.abspath("../fast-tax-python/SOAP"))

from get_best_match_soap import GetBestMatchSoap


def get_best_match_soap_sdk_go(is_live: bool, license_key: str) -> None:
    print("\r\n---------------------------------")
    print("FastTax - GetBestMatch - SOAP SDK")
    print("---------------------------------")

    address = "136 W Canon Perdido St Ste D"
    address2 = ""
    city = "Santa Barbara"
    state = "CA"
    zip = "93101"
    tax_type = "sales"
    timeout_seconds = 15

    print("\r\n* Input *\r\n")
    print(f"Address        : {address}")
    print(f"Address2       : {address2}")
    print(f"City           : {city}")
    print(f"State          : {state}")
    print(f"Zip            : {zip}")
    print(f"Tax Type       : {tax_type}")
    print(f"License Key    : {license_key}")
    print(f"Is Live        : {is_live}")
    print(f"Timeout Seconds: {timeout_seconds}")

    try:
        service = GetBestMatchSoap(license_key, is_live, timeout_seconds * 1000)
        response = service.get_best_match(address, address2, city, state, zip, tax_type)

        if not hasattr(response, 'Error') or not response.Error:
            print("\r\n* Tax Info *\r\n")
            print(f"Match Level      : {response.MatchLevel}")
            if hasattr(response, 'TaxInfoItems') and response.TaxInfoItems:
                items = response.TaxInfoItems.BestMatchTaxInfo if hasattr(response.TaxInfoItems, 'BestMatchTaxInfo') else []
                if not isinstance(items, list):
                    items = [items]
                for tax_info in items:
                    print(f"Zip              : {getattr(tax_info, 'Zip', None)}")
                    print(f"City             : {getattr(tax_info, 'City', None)}")
                    print(f"County           : {getattr(tax_info, 'County', None)}")
                    print(f"State Abbrev     : {getattr(tax_info, 'StateAbbreviation', None)}")
                    print(f"State Name       : {getattr(tax_info, 'StateName', None)}")
                    print(f"Total Tax Rate   : {getattr(tax_info, 'TaxRate', None)}")
                    print(f"State Rate       : {getattr(tax_info, 'StateRate', None)}")
                    print(f"City Rate        : {getattr(tax_info, 'CityRate', None)}")
                    print(f"County Rate      : {getattr(tax_info, 'CountyRate', None)}")
                    print(f"County Dist Rate : {getattr(tax_info, 'CountyDistrictRate', None)}")
                    print(f"City Dist Rate   : {getattr(tax_info, 'CityDistrictRate', None)}")
                    print(f"Special Dist Rate: {getattr(tax_info, 'SpecialDistrictRate', None)}")
                    print(f"Total Tax Exempt : {getattr(tax_info, 'TotalTaxExempt', None)}")
                    print(f"Notes Codes      : {getattr(tax_info, 'NotesCodes', None)}")
                    print(f"Notes Desc       : {getattr(tax_info, 'NotesDesc', None)}")

                    print("\r\n* Information Components *\r\n")
                    if hasattr(tax_info, 'InformationComponents') and tax_info.InformationComponents:
                        components = tax_info.InformationComponents.InformationComponent
                        if not isinstance(components, list):
                            components = [components]
                        for component in components:
                            print(f"{getattr(component, 'Name', None)}: {getattr(component, 'Value', None)}")
                    else:
                        print("No information components found.")
            else:
                print("No tax info items found.")
        else:
            print("No tax info found.")

        if hasattr(response, 'Error') and response.Error:
            print("\r\n* Error *\r\n")
            print(f"Error Desc    : {response.Error.Desc}")
            print(f"Error Number  : {response.Error.Number}")
            print(f"Error Location: {response.Error.Location}")

    except Exception as e:
        print("\r\n* Error *\r\n")
        print(f"Exception occurred: {str(e)}")

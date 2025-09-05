import sys
import os

sys.path.insert(0, os.path.abspath("../fast-tax-python/REST"))

from get_best_match_rest import get_best_match


def get_best_match_rest_sdk_go(is_live: bool, license_key: str) -> None:
    print("\r\n---------------------------------")
    print("FastTax - GetBestMatch - REST SDK")
    print("---------------------------------")

    address = "27 E Cota St"
    address2 = ""
    city = "Santa Barbara"
    state = "CA"
    zip = "93101"
    tax_type = "sales"

    print("\r\n* Input *\r\n")
    print(f"Address    : {address}")
    print(f"Address2   : {address2}")
    print(f"City       : {city}")
    print(f"State      : {state}")
    print(f"Zip        : {zip}")
    print(f"Tax Type   : {tax_type}")
    print(f"License Key: {license_key}")
    print(f"Is Live    : {is_live}")

    try:
        response = get_best_match(address, address2, city, state, zip, tax_type, license_key, is_live)

        print("\r\n* Tax Info *\r\n")
        if response and not response.Error:
            print(f"Match Level      : {response.MatchLevel}")
            if response.TaxInfoItems and len(response.TaxInfoItems) > 0:
                for tax_info in response.TaxInfoItems:
                    print(f"Zip              : {tax_info.Zip}")
                    print(f"City             : {tax_info.City}")
                    print(f"County           : {tax_info.County}")
                    print(f"State Abbrev     : {tax_info.StateAbbreviation}")
                    print(f"State Name       : {tax_info.StateName}")
                    print(f"Total Tax Rate   : {tax_info.TaxRate}")
                    print(f"State Rate       : {tax_info.StateRate}")
                    print(f"City Rate        : {tax_info.CityRate}")
                    print(f"County Rate      : {tax_info.CountyRate}")
                    print(f"County Dist Rate : {tax_info.CountyDistrictRate}")
                    print(f"City Dist Rate   : {tax_info.CityDistrictRate}")
                    print(f"Special Dist Rate: {tax_info.SpecialDistrictRate}")
                    print(f"Total Tax Exempt : {tax_info.TotalTaxExempt}")
                    print(f"Notes Codes      : {tax_info.NotesCodes}")
                    print(f"Notes Desc       : {tax_info.NotesDesc}")

                    print("\r\n* Information Components *\r\n")
                    if tax_info.InformationComponents and len(tax_info.InformationComponents) > 0:
                        for component in tax_info.InformationComponents:
                            print(f"{component.Name}: {component.Value}")
                    else:
                        print("No information components found.")
            else:
                print("No tax info items found.")
        else:
            print("No tax info found.")

        if response.Error:
            print("\r\n* Error *\r\n")
            print(f"Error Desc    : {response.Error.Desc}")
            print(f"Error Number  : {response.Error.Number}")
            print(f"Error Location: {response.Error.Location}")

    except Exception as e:
        print("\r\n* Error *\r\n")
        print(f"Error Message: {str(e)}")

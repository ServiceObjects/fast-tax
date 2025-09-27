![Service Objects Logo](https://www.serviceobjects.com/wp-content/uploads/2021/05/SO-Logo-with-TM.gif "Service Objects Logo")

# FT - FastTax

DOTS FastTax (referred to as FastTax or FT) is a publicly available XML and JSON web service that provides sales tax rate information for all US areas based on several different inputs. The service provides zip, city, county, county fips codes, state, tax rates and exemptions. 

FastTax can provide instant sales tax rates for any address, zip code, city or county in the United States.

## [Service Objects Website](https://serviceobjects.com)

# FT - GetBestMatch

This operation will return the best available tax rate match with the given input. If the given address input cannot be resolved or found, the operation will provide a Zip level match if the given zip code is valid. 

The service will provide a total tax rate for the given input as well as the different CountryDistrict, CityDistrict, City, County and State rates that the comprise the total rate returned. 

This operation also has the ability to determine whether or not a given address may be in an unincorporated area.  If the IsUnicorporated flag is returned in the NotesDesc field, then appropriate logic should be implemented to remove the city and city district rates from the total rate as those would not apply for the given input.

If the MatchLevel returned is “Zip” then this operation can also return multiple tax rates for the different tax jurisdictions combinations within the particular zip code. In this case, it would be up the user to determine what tax rate would prove to be the best match for the given input.

### [GetBestMatches_V4 Developer Guide/Documentation](https://www.serviceobjects.com/docs/dots-fasttax/ft-operations/ft-getbestmatch-recommended-operation/)

## Library Usage

```
// 1. Build the input
//
//  Required fields:
//               address
//               address2
//               state
//               city
//               zip
//               tax_type
//               license_key
//               is_live
// 
// Optional:
//        timeout_seconds

from get_best_match_soap import GetBestMatchSoap

address = "27 E Cota St"
address2 = ""
city = "Santa Barbara"
state = "CA"
zip = "93101"
tax_type = "sales"
timeout_seconds = 15;
is_live = False
license_key = "YOUR LICENSE KEY"


// 2. Call the method.
service = GetBestMatchSoap(license_key, is_live, timeout_seconds * 1000)
response = service.get_best_match(address, address2, city, state, zip, tax_type)

// 3. Inspect results.
if not hasattr(response, 'Error') or not response.Error:
    print("\r\n* Tax Info *\r\n")
    print(f"Match Level    : {response.MatchLevel}")
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
    print(f"Error Desc  : {response.Error.Desc}")
    print(f"Error Number: {response.Error.Number}")
    print(f"Error Location: {response.Error.Location}")
```

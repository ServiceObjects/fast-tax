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
//               license_key
//               is_live
// 
// Optional:

//        tax_type	

from get_best_match_rest import get_best_match

address = "27 E Cota St"
address2 = ""
city = "Santa Barbara"
state = "CA"
zip = "93101"
tax_type = "sales"
is_live = False
license_key = "YOUR LICENSE KEY"

// 2. Call the method.
response = get_best_match(address, address2, city, state, zip, tax_type, license_key, is_live)

// 3. Inspect results.
console.log("\n* Tax Info *\n");
print("\r\n* Tax Info *\r\n")
if response and not response.Error:
    print(f"Match Level    : {response.MatchLevel}")
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
    print(f"Error Desc  : {response.Error.Desc}")
    print(f"Error Number: {response.Error.Number}")}
    print(f"Error Location: {response.Error.Location}")
```

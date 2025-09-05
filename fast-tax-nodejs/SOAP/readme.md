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
//               LicenseKey
//               IsLive
// 
// Optional:
//        Address
//        Address2
//        State
//        City
//        Zip
//        TaxType	
//        TimeoutSeconds (default: 15)

import { GetBestMatchSoap } from '../fast-tax-nodejs/SOAP/get_best_match_soap.js';

const address = "42083 County Road 161";
const address2 = "";
const city = "Agate";
const state = "CO";
const zip = "80101";
const taxType = "sales";
const timeoutSeconds = 15;

// 2. Call the sync invokeAsync() method.
const ft = new GetBestMatchSoap(address, address2, city, state, zip, taxType, licenseKey, isLive, timeoutSeconds);
const response = await ft.invokeAsync();

// 3. Inspect results.
console.log("\n* Tax Info *\n");
if (response) 
{
    console.log(`Match Level  : ${response.MatchLevel}`);
    if (response.TaxInfoItems && response.TaxInfoItems.BestMatchTaxInfo.length > 0) 
    {
            for (const  taxInfo of response.TaxInfoItems.BestMatchTaxInfo)
            {
            console.log(`Zip              : ${taxInfo.Zip}`);
            console.log(`City             : ${taxInfo.City}`);
            console.log(`County           : ${taxInfo.County}`);
            console.log(`State Abbrev     : ${taxInfo.StateAbbreviation}`);
            console.log(`State Name       : ${taxInfo.StateName}`);
            console.log(`Total Tax Rate   : ${taxInfo.TaxRate}`);
            console.log(`State Rate       : ${taxInfo.StateRate}`);
            console.log(`City Rate        : ${taxInfo.CityRate}`);
            console.log(`County Rate      : ${taxInfo.CountyRate}`);
            console.log(`County Dist Rate : ${taxInfo.CountyDistrictRate}`);
            console.log(`City Dist Rate   : ${taxInfo.CityDistrictRate}`);
            console.log(`Special Dist Rate: ${taxInfo.SpecialDistrictRate}`);
            console.log(`Total Tax Exempt : ${taxInfo.TotalTaxExempt}`);
            console.log(`Notes Codes      : ${taxInfo.NotesCodes}`);
            console.log(`Notes Desc       : ${taxInfo.NotesDesc}`);

            console.log("\n* Information Components *\n");
            if (taxInfo.InformationComponents && taxInfo.InformationComponents?.InformationComponent.length > 0)
            {
                taxInfo.InformationComponents?.InformationComponent.forEach((component, compIndex) => {
                    console.log(`${component.Name}: ${component.Value}`);
                });
            } 
            else 
            {
                console.log("No information components found.");
            }
        };
    } 
    else 
    {
        console.log("No tax info items found.");
    }
           
} 
else
{
    console.log("No tax info found.");
}

if (response.Error) {
    console.log("\n* Error *\n");
    console.log(`Error Desc  : ${response.Error.Desc}`);
    console.log(`Error Number: ${response.Error.Number}`);
}
```

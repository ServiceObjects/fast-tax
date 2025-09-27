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
//               Address
//               Address2
//               State
//               City
//               Zip
//               TaxType	
//               LicenseKey
//               IsLive
// 
// Optional:
//        TimeoutSeconds

using fast_tax_dot_net.REST;

GetBestMatchClient.GetBestMatchInput getBestMatchInput = new(
    Address: "27 E Cota St",
    Address2: "",
    City: "Santa Barbara",
    State: "CA",
    Zip: "93101",
    TaxType: "sales",
    LicenseKey: licenseKey,
    IsLive: true,
    TimeoutSeconds: 15
);

// 2. Call the sync Invoke() method.
GetBestMatchResponse response = GetBestMatchClient.Invoke(getBestMatchInput);

// 3. Inspect results.
if (response.Error is null)
{
    Console.WriteLine("\r\n* Tax Info *\r\n");
    Console.WriteLine($"Match Level  : {response.MatchLevel}");
    if (response.TaxInfoItems?.Length > 0)
    {
        foreach (var taxInfo in response.TaxInfoItems)
        {
            Console.WriteLine($"Zip              : {taxInfo.Zip}");
            Console.WriteLine($"City             : {taxInfo.City}");
            Console.WriteLine($"County           : {taxInfo.County}");
            Console.WriteLine($"State Abbrev     : {taxInfo.StateAbbreviation}");
            Console.WriteLine($"State Name       : {taxInfo.StateName}");
            Console.WriteLine($"Total Tax Rate   : {taxInfo.TaxRate}");
            Console.WriteLine($"State Rate       : {taxInfo.StateRate}");
            Console.WriteLine($"City Rate        : {taxInfo.CityRate}");
            Console.WriteLine($"County Rate      : {taxInfo.CountyRate}");
            Console.WriteLine($"County Dist Rate : {taxInfo.CountyDistrictRate}");
            Console.WriteLine($"City Dist Rate   : {taxInfo.CityDistrictRate}");
            Console.WriteLine($"Special Dist Rate: {taxInfo.SpecialDistrictRate}");
            Console.WriteLine($"Total Tax Exempt : {taxInfo.TotalTaxExempt}");
            Console.WriteLine($"Notes Codes      : {taxInfo.NotesCodes}");
            Console.WriteLine($"Notes Desc       : {taxInfo.NotesDesc}");

            Console.WriteLine("\r\n* Information Components *\r\n");
            if (taxInfo.InformationComponents?.Length > 0)
            {
                foreach (var component in taxInfo.InformationComponents)
                {
                    Console.WriteLine($"{component.Name}: {component.Value}");
                }
            }
            else
            {
                Console.WriteLine("No information components found.");
            }
        }
    }
    else
    {
        Console.WriteLine("No tax info items found.");
    }
}
else
{
    Console.WriteLine("\r\n* Error *\r\n");
    Console.WriteLine($"Error Number    : {response.Error.Number}");
    Console.WriteLine($"Error Desc      : {response.Error.Desc}");
    Console.WriteLine($"Error Location  : {response.Error.Location}");
}
```

import { GetBestMatchClient } from '../fast-tax-nodejs/REST/get_best_match_rest.js';

async function GetBestMatchRestGo(licenseKey, isLive) {
    console.log("\n---------------------------------");
    console.log("FastTax - GetBestMatch - REST SDK");
    console.log("---------------------------------");

    const address = "27 E Cota St";
    const address2 = "";
    const city = "Santa Barbara";
    const state = "CA";
    const zip = "93101";
    const taxType = "sales";
    const timeoutSeconds = 15;

    console.log("\n* Input *\n");
    console.log(`Address        : ${address}`);
    console.log(`Address2       : ${address2}`);
    console.log(`City           : ${city}`);
    console.log(`State          : ${state}`);
    console.log(`Zip            : ${zip}`);
    console.log(`Tax Type       : ${taxType}`);
    console.log(`License Key    : ${licenseKey}`);
    console.log(`Is Live        : ${isLive}`);
    console.log(`Timeout Seconds: ${timeoutSeconds}`);

    try {
        const response = await GetBestMatchClient.invoke(
            address,
            address2,
            city,
            state,
            zip,
            taxType,
            licenseKey,
            isLive,
            timeoutSeconds
        );

        console.log("\n* Tax Info *\n");
        if (response) {
            console.log(`Match Level  : ${response.MatchLevel}`);
            if (response.TaxInfoItems && response.TaxInfoItems.length > 0) {
                for (const taxInfo of response.TaxInfoItems) {
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
                    if (taxInfo.InformationComponents && taxInfo.InformationComponents.length > 0) {
                        taxInfo.InformationComponents.forEach((component) => {
                            console.log(`${component.Name}: ${component.Value}`);
                        });
                    } else {
                        console.log("No information components found.");
                    }
                }
            } else {
                console.log("No tax info items found.");
            }
        } else {
            console.log("No tax info found.");
        }

        if (response.Error) {
            console.log("\n* Error *\n");
            console.log(`Error Desc    : ${response.Error.Desc}`);
            console.log(`Error Number  : ${response.Error.Number}`);
            console.log(`Error Location: ${response.Error.Location}`);
            return;
        }
    } catch (e) {
        console.log("\n* Error *\n");
        console.log(`Error Message: ${e.message}`);
    }
}

export { GetBestMatchRestGo };

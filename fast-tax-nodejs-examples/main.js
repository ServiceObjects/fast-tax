
import { GetBestMatchRestGo } from './get_best_match_rest_sdk_example.js'
import { GetBestMatchSoapGo } from './get_best_match_soap_sdk_example.js'

export async function main()
{
    //Your license key from Service Objects.
    //Trial license keys will only work on the
    //trail environments and production license
    //keys will only work on production environments.
    const licenseKey = "LICENSE KEY";
    const isLive = true;

    // FastTax – GetBestMatch - REST SDK
    await GetBestMatchRestGo(licenseKey, isLive);

    // FastTax – GetBestMatch - SOAP SDK
    await GetBestMatchSoapGo(licenseKey, isLive);

}
main().catch((error) => {
  console.error("An error occurred:", error);
  process.exit(1);
});
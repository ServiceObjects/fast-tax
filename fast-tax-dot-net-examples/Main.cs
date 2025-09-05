using fast_tax_dot_net_examples;

//Your license key from Service Objects.
//Trial license keys will only work on the
//trail environments and production license
//keys will only work on production environments.
string LicenseKey = "LICENSE KEY";

bool IsProductionKey = false;

// FastTax – GetBestMatch - REST SDK
GetBestMatchRestSdkExample.Go(LicenseKey, IsProductionKey);

// FastTax - GetBestMatch - SOAP SDK
GetBestMatchSoapSdkExample.Go(LicenseKey, IsProductionKey);
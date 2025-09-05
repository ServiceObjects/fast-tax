using FTReference;
using fast_tax_dot_net.SOAP;

namespace fast_tax_dot_net_examples
{
    public static class GetBestMatchSoapSdkExample
    {
        public static void Go(string licenseKey, bool isLive)
        {
            Console.WriteLine("\r\n---------------------------------");
            Console.WriteLine("FastTax - GetBestMatch - SOAP SDK");
            Console.WriteLine("---------------------------------");

            string Address = "27 E Cota St";
            string Address2 = "";
            string City = "Santa Barbara";
            string State = "CA";
            string Zip = "93101";
            string TaxType = "sales";

            Console.WriteLine("\r\n* Input *\r\n");
            Console.WriteLine($"Address    : {Address}");
            Console.WriteLine($"Address2   : {Address2}");
            Console.WriteLine($"City       : {City}");
            Console.WriteLine($"State      : {State}");
            Console.WriteLine($"Zip        : {Zip}");
            Console.WriteLine($"Tax Type   : {TaxType}");
            Console.WriteLine($"License Key: {licenseKey}");
            Console.WriteLine($"Is Live    : {isLive}");

            GetBestMatchValidation getBestMatchValidation = new(isLive);
            BestMatchResponse response = getBestMatchValidation.GetBestMatch(Address, Address2, City, State, Zip, TaxType, licenseKey).Result;

            if (response.Error is null)
            {
                Console.WriteLine("\r\n* Tax Info *\r\n");
                Console.WriteLine($"Match Level      : {response.MatchLevel}");
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
        }
    }
}
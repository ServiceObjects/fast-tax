using System.Web;

namespace fast_tax_dot_net.REST
{
    /// <summary>
    /// Provides functionality to call the ServiceObjects FastTax (FT) REST API's GetBestMatch endpoint,
    /// retrieving tax rate information (e.g., total tax rate, city, county, state rates) for a given US address
    /// with fallback to a backup endpoint for reliability in live mode.
    /// </summary>
    public static class GetBestMatchClient
    {
        // Base URL constants: production, backup, and trial
        private const string LiveBaseUrl = "https://sws.serviceobjects.com/ft/web.svc/json/";
        private const string BackupBaseUrl = "https://swsbackup.serviceobjects.com/ft/web.svc/json/";
        private const string TrialBaseUrl = "https://trial.serviceobjects.com/ft/web.svc/json/";

        /// <summary>
        /// Synchronously calls the GetBestMatch REST endpoint to retrieve tax rate information,
        /// attempting the primary endpoint first and falling back to the backup if the response is invalid
        /// (Error.Number == "4") in live mode.
        /// </summary>
        /// <param name="input">The input parameters including address, city, state, zip, tax type, and license key.</param>
        /// <returns>Deserialized <see cref="GetBestMatchResponse"/> containing tax rate data or an error.</returns>
        public static GetBestMatchResponse Invoke(GetBestMatchInput input)
        {
            // Use query string parameters so missing/optional fields don't break the URL
            string url = BuildUrl(input, input.IsLive ? LiveBaseUrl : TrialBaseUrl);
            GetBestMatchResponse response = Helper.HttpGet<GetBestMatchResponse>(url, input.TimeoutSeconds);

            // Fallback on error in live mode
            if (input.IsLive && !IsValid(response))
            {
                string fallbackUrl = BuildUrl(input, BackupBaseUrl);
                GetBestMatchResponse fallbackResponse = Helper.HttpGet<GetBestMatchResponse>(fallbackUrl, input.TimeoutSeconds);
                return fallbackResponse;
            }

            return response;
        }

        /// <summary>
        /// Asynchronously calls the GetBestMatch REST endpoint to retrieve tax rate information,
        /// attempting the primary endpoint first and falling back to the backup if the response is invalid
        /// (Error.Number == "4") in live mode.
        /// </summary>
        /// <param name="input">The input parameters including address, city, state, zip, tax type, and license key.</param>
        /// <returns>Deserialized <see cref="GetBestMatchResponse"/> containing tax rate data or an error.</returns>
        public static async Task<GetBestMatchResponse> InvokeAsync(GetBestMatchInput input)
        {
            // Use query string parameters so missing/optional fields don't break the URL
            string url = BuildUrl(input, input.IsLive ? LiveBaseUrl : TrialBaseUrl);
            GetBestMatchResponse response = await Helper.HttpGetAsync<GetBestMatchResponse>(url, input.TimeoutSeconds).ConfigureAwait(false);

            // Fallback on error in live mode
            if (input.IsLive && !IsValid(response))
            {
                string fallbackUrl = BuildUrl(input, BackupBaseUrl);
                GetBestMatchResponse fallbackResponse = await Helper.HttpGetAsync<GetBestMatchResponse>(fallbackUrl, input.TimeoutSeconds).ConfigureAwait(false);
                return fallbackResponse;
            }

            return response;
        }

        // Build the full request URL, including URL-encoded query string
        public static string BuildUrl(GetBestMatchInput input, string baseUrl)
        {
            // Construct query string with URL-encoded parameters
            string qs = $"GetBestMatch?" +
                        $"Address={HttpUtility.UrlEncode(input.Address)}" +
                        $"&Address2={HttpUtility.UrlEncode(input.Address2)}" +
                        $"&City={HttpUtility.UrlEncode(input.City)}" +
                        $"&State={HttpUtility.UrlEncode(input.State)}" +
                        $"&Zip={HttpUtility.UrlEncode(input.Zip)}" +
                        $"&TaxType={HttpUtility.UrlEncode(input.TaxType)}" +
                        $"&LicenseKey={HttpUtility.UrlEncode(input.LicenseKey)}";
            return baseUrl + qs;
        }

        private static bool IsValid(GetBestMatchResponse response) => response?.Error == null || response.Error.Number != "4";

        /// <summary>
        /// Input parameters for the GetBestMatch API call. Represents a US address to retrieve tax rates
        /// with cascading logic for partial matches.
        /// </summary>
        /// <param name="Address">Address line of the address to get tax rates for (e.g., "123 Main Street").</param>
        /// <param name="Address2">Secondary address line (e.g., "Apt 4B"). Optional.</param>
        /// <param name="City">The city of the address (e.g., "New York"). Optional if zip is provided.</param>
        /// <param name="State">The state of the address (e.g., "NY"). Optional if zip is provided.</param>
        /// <param name="Zip">The ZIP code of the address. Optional if city and state are provided.</param>
        /// <param name="TaxType">The type of tax to look for ("sales" or "use").</param>
        /// <param name="LicenseKey">The license key to authenticate the API request.</param>
        /// <param name="IsLive">Indicates whether to use the live service (true) or trial service (false).</param>
        /// <param name="TimeoutSeconds">Timeout duration for the API call, in seconds.</param>
        public record GetBestMatchInput(
            string Address = "",
            string Address2 = "",
            string City = "",
            string State = "",
            string Zip = "",
            string TaxType = "",
            string LicenseKey = "",
            bool IsLive = true,
            int TimeoutSeconds = 15
        );
    }
}
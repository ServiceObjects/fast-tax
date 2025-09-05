using System;
using System.Threading.Tasks;
using FTReference;

namespace fast_tax_dot_net.SOAP
{
    /// <summary>
    /// Provides functionality to call the ServiceObjects FastTax (FT) SOAP service's GetBestMatch operation,
    /// retrieving tax rate information (e.g., total tax rate, city, county, state rates) for a given US address
    /// with fallback to a backup endpoint for reliability in live mode.
    /// </summary>
    public class GetBestMatchValidation
    {
        private const string LiveBaseUrl = "https://sws.serviceobjects.com/ft/soap.svc/SOAP";
        private const string BackupBaseUrl = "https://swsbackup.serviceobjects.com/ft/soap.svc/SOAP";
        private const string TrialBaseUrl = "https://trial.serviceobjects.com/ft/soap.svc/SOAP";

        private readonly string _primaryUrl;
        private readonly string _backupUrl;
        private readonly int _timeoutMs;
        private readonly bool _isLive;

        /// <summary>
        /// Initializes URLs/timeout/IsLive.
        /// </summary>
        public GetBestMatchValidation(bool isLive)
        {
            _timeoutMs = 10000;
            _isLive = isLive;

            _primaryUrl = isLive ? LiveBaseUrl : TrialBaseUrl;
            _backupUrl = isLive ? BackupBaseUrl : TrialBaseUrl;

            if (string.IsNullOrWhiteSpace(_primaryUrl))
                throw new InvalidOperationException("Primary URL not set.");
            if (string.IsNullOrWhiteSpace(_backupUrl))
                throw new InvalidOperationException("Backup URL not set.");
        }

        /// <summary>
        /// This operation returns the best available tax rate match for a given US address, including total tax rate,
        /// state, county, city, and district rates, along with additional information like IsUnincorporated status.
        /// </summary>
        /// <param name="Address">Address line of the address to get tax rates for (e.g., "123 Main Street").</param>
        /// <param name="Address2">Secondary address line (e.g., "Apt 4B"). Optional.</param>
        /// <param name="City">The city of the address (e.g., "New York"). Optional if zip is provided.</param>
        /// <param name="State">The state of the address (e.g., "NY"). Optional if zip is provided.</param>
        /// <param name="Zip">The ZIP code of the address. Optional if city and state are provided.</param>
        /// <param name="TaxType">The type of tax to look for ("sales" or "use").</param>
        /// <param name="LicenseKey">The license key to authenticate the API request.</param>
        public async Task<BestMatchResponse> GetBestMatch(string Address, string Address2, string City, string State, string Zip, string TaxType, string LicenseKey)
        {
            SOAPClient clientPrimary = null;
            SOAPClient clientBackup = null;

            try
            {
                // Attempt Primary
                clientPrimary = new SOAPClient();
                clientPrimary.Endpoint.Address = new System.ServiceModel.EndpointAddress(_primaryUrl);
                clientPrimary.InnerChannel.OperationTimeout = TimeSpan.FromMilliseconds(_timeoutMs);

                BestMatchResponse response = await clientPrimary.GetBestMatchAsync(
                    Address, Address2, City, State, Zip, TaxType, LicenseKey).ConfigureAwait(false);

                if (_isLive && !IsValid(response))
                {
                    throw new InvalidOperationException("Primary endpoint returned null or a fatal Number=4 error for GetBestMatch");
                }
                return response;
            }
            catch (Exception primaryEx)
            {

                try
                {
                    clientBackup = new SOAPClient();
                    clientBackup.Endpoint.Address = new System.ServiceModel.EndpointAddress(_backupUrl);
                    clientBackup.InnerChannel.OperationTimeout = TimeSpan.FromMilliseconds(_timeoutMs);

                    return await clientBackup.GetBestMatchAsync(
                        Address, Address2, City, State, Zip, TaxType, LicenseKey).ConfigureAwait(false);
                }
                catch (Exception backupEx)
                {
                    throw new InvalidOperationException(
                        $"Both primary and backup endpoints failed.\n" +
                        $"Primary error: {primaryEx.Message}\n" +
                        $"Backup error: {backupEx.Message}");
                }
                finally
                {
                    clientBackup?.Close();
                }
            }
            finally
            {
                clientPrimary?.Close();
            }
        }
        private static bool IsValid(BestMatchResponse response) => response?.Error == null || response.Error.Number != "4";
    }
}
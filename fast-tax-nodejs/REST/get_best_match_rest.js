import axios from 'axios';
import querystring from 'querystring';
import { GetBestMatchResponse } from './ft_response.js';

/**
 * @constant
 * @type {string}
 * @description The base URL for the live ServiceObjects FastTax (FT) API service.
 */
const LiveBaseUrl = 'https://sws.serviceobjects.com/ft/web.svc/json/';

/**
 * @constant
 * @type {string}
 * @description The base URL for the backup ServiceObjects FastTax (FT) API service.
 */
const BackupBaseUrl = 'https://swsbackup.serviceobjects.com/ft/web.svc/json/';

/**
 * @constant
 * @type {string}
 * @description The base URL for the trial ServiceObjects FastTax (FT) API service.
 */
const TrialBaseUrl = 'https://trial.serviceobjects.com/ft/web.svc/json/';

/**
 * <summary>
 * Checks if a response from the API is valid by verifying that it either has no Error object
 * or the Error.Number is not equal to '4'.
 * </summary>
 * <param name="response" type="Object">The API response object to validate.</param>
 * <returns type="boolean">True if the response is valid, false otherwise.</returns>
 */
const isValid = (response) => !response?.Error || response.Error.Number !== '4';

/**
 * <summary>
 * Constructs a full URL for the GetBestMatch API endpoint by combining the base URL
 * with query parameters derived from the input parameters.
 * </summary>
 * <param name="params" type="Object">An object containing all the input parameters.</param>
 * <param name="baseUrl" type="string">The base URL for the API service (live, backup, or trial).</param>
 * <returns type="string">The constructed URL with query parameters.</returns>
 */
const buildUrl = (params, baseUrl) =>
    `${baseUrl}GetBestMatch?${querystring.stringify(params)}`;

/**
 * <summary>
 * Performs an HTTP GET request to the specified URL with a given timeout.
 * </summary>
 * <param name="url" type="string">The URL to send the GET request to.</param>
 * <param name="timeoutSeconds" type="number">The timeout duration in seconds for the request.</param>
 * <returns type="Promise<GetBestMatchResponse>">A promise that resolves to a GetBestMatchResponse object containing the API response data.</returns>
 * <exception cref="Error">Thrown if the HTTP request fails, with a message detailing the error.</exception>
 */
const httpGet = async (url, timeoutSeconds) => {
    try {
        const response = await axios.get(url, { timeout: timeoutSeconds * 1000 });
        return new GetBestMatchResponse(response.data);
    } catch (error) {
        throw new Error(`HTTP request failed: ${error.message}`);
    }
};

/**
 * <summary>
 * Provides functionality to call the ServiceObjects FastTax (FT) API's GetBestMatch endpoint,
 * retrieving tax rate information (e.g., total tax rate, city, county, state rates) for a given US address
 * with fallback to a backup endpoint for reliability in live mode.
 * </summary>
 */
const GetBestMatchClient = {
    /**
     * <summary>
     * Asynchronously invokes the GetBestMatch API endpoint, attempting the primary endpoint
     * first and falling back to the backup if the response is invalid (Error.Number == '4') in live mode.
     * </summary>
     * @param {string} Address - Address line of the address to get tax rates for (e.g., "123 Main Street").
     * @param {string} Address2 - Secondary address line (e.g., "Apt 4B"). Optional.
     * @param {string} City - The city of the address (e.g., "New York"). Optional if zip is provided.
     * @param {string} State - The state of the address (e.g., "NY"). Optional if zip is provided.
     * @param {string} Zip - The ZIP code of the address. Optional if city and state are provided.
     * @param {string} TaxType - The type of tax to look for ("sales" or "use").
     * @param {string} LicenseKey - Your license key to use the service.
     * @param {boolean} isLive - Value to determine whether to use the live or trial servers.
     * @param {number} timeoutSeconds - Timeout, in seconds, for the call to the service.
     * @returns {Promise<GetBestMatchResponse>} - A promise that resolves to a GetBestMatchResponse object.
     */
    async invokeAsync(Address, Address2, City, State, Zip, TaxType, LicenseKey, isLive = true, timeoutSeconds = 15) {
        const params = {
            Address,
            Address2,
            City,
            State,
            Zip,
            TaxType,
            LicenseKey
        };

        const url = buildUrl(params, isLive ? LiveBaseUrl : TrialBaseUrl);
        let response = await httpGet(url, timeoutSeconds);

        if (isLive && !isValid(response)) {
            const fallbackUrl = buildUrl(params, BackupBaseUrl);
            const fallbackResponse = await httpGet(fallbackUrl, timeoutSeconds);
            return fallbackResponse;
        }
        return response;
    },

    /**
     * <summary>
     * Synchronously invokes the GetBestMatch API endpoint by wrapping the async call
     * and awaiting its result immediately.
     * </summary>
     * @param {string} Address - Address line of the address to get tax rates for (e.g., "123 Main Street").
     * @param {string} Address2 - Secondary address line (e.g., "Apt 4B"). Optional.
     * @param {string} City - The city of the address (e.g., "New York"). Optional if zip is provided.
     * @param {string} State - The state of the address (e.g., "NY"). Optional if zip is provided.
     * @param {string} Zip - The ZIP code of the address. Optional if city and state are provided.
     * @param {string} TaxType - The type of tax to look for ("sales" or "use").
     * @param {string} LicenseKey - Your license key to use the service.
     * @param {boolean} isLive - Value to determine whether to use the live or trial servers.
     * @param {number} timeoutSeconds - Timeout, in seconds, for the call to the service.
     * @returns {GetBestMatchResponse} - A GetBestMatchResponse object with tax rate details or an error.
     */
    invoke(Address, Address2, City, State, Zip, TaxType, LicenseKey, isLive = true, timeoutSeconds = 15) {
        return (async () => await this.invokeAsync(
            Address, Address2, City, State, Zip, TaxType, LicenseKey, isLive, timeoutSeconds
        ))();
    }
};

export { GetBestMatchClient, GetBestMatchResponse };
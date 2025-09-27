/**
 * Input parameters for the GetBestMatch API call.
 */
export class GetBestMatchInput {
    constructor(data = {}) {
        this.Address = data.Address;
        this.Address2 = data.Address2;
        this.City = data.City;
        this.State = data.State;
        this.Zip = data.Zip;
        this.TaxType = data.TaxType;
        this.LicenseKey = data.LicenseKey;
        this.IsLive = data.IsLive !== undefined ? data.IsLive : true;
        this.TimeoutSeconds = data.TimeoutSeconds !== undefined ? data.TimeoutSeconds : 15;
    }

    toString() {
        return `GetBestMatchInput: Address = ${this.Address}, Address2 = ${this.Address2}, City = ${this.City}, State = ${this.State}, Zip = ${this.Zip}, TaxType = ${this.TaxType}, LicenseKey = ${this.LicenseKey}, IsLive = ${this.IsLive}, TimeoutSeconds = ${this.TimeoutSeconds}`;
    }
}

/**
 * Information Component for API responses.
 */
export class InformationComponent {
    constructor(data = {}) {
        this.Name = data.Name;
        this.Value = data.Value;
    }

    toString() {
        return `Name = ${this.Name}, Value = ${this.Value}`;
    }
}

/**
 * Error object for API responses.
 */
export class Error {
    constructor(data = {}) {
        this.Desc = data.Desc;
        this.Number = data.Number;
        this.Location = data.Location;
    }

    toString() {
        return `Error: Desc = ${this.Desc}, Number = ${this.Number}, Location = ${this.Location}`;
    }
}

/**
 * Tax information for a matched address or ZIP code.
 */
export class BestMatchTaxInfo {
    constructor(data = {}) {
        this.Zip = data.Zip;
        this.City = data.City;
        this.County = data.County;
        this.StateAbbreviation = data.StateAbbreviation;
        this.StateName = data.StateName;
        this.TaxRate = data.TaxRate;
        this.StateRate = data.StateRate;
        this.CityRate = data.CityRate;
        this.CountyRate = data.CountyRate;
        this.CountyDistrictRate = data.CountyDistrictRate;
        this.CityDistrictRate = data.CityDistrictRate;
        this.SpecialDistrictRate = data.SpecialDistrictRate;
        this.InformationComponents = (data.InformationComponents || []).map(component => new InformationComponent(component));
        this.TotalTaxExempt = data.TotalTaxExempt;
        this.NotesCodes = data.NotesCodes;
        this.NotesDesc = data.NotesDesc;
    }

    toString() {
        const componentsString = this.InformationComponents.length
            ? this.InformationComponents.map(component => component.toString()).join(', ')
            : 'null';
        return `BestMatchTaxInfo: Zip = ${this.Zip}, City = ${this.City}, County = ${this.County}, StateAbbreviation = ${this.StateAbbreviation}, StateName = ${this.StateName}, TaxRate = ${this.TaxRate}, StateRate = ${this.StateRate}, CityRate = ${this.CityRate}, CountyRate = ${this.CountyRate}, CountyDistrictRate = ${this.CountyDistrictRate}, CityDistrictRate = ${this.CityDistrictRate}, SpecialDistrictRate = ${this.SpecialDistrictRate}, InformationComponents = [${componentsString}], TotalTaxExempt = ${this.TotalTaxExempt}, NotesCodes = ${this.NotesCodes}, NotesDesc = ${this.NotesDesc}`;
    }
}

/**
 * Response from GetBestMatch API, containing tax rate information for the best match.
 */
export class GetBestMatchResponse {
    constructor(data = {}) {
        this.TaxInfoItems = (data.TaxInfoItems || []).map(taxInfo => new BestMatchTaxInfo(taxInfo));
        this.MatchLevel = data.MatchLevel;
        this.Error = data.Error ? new Error(data.Error) : null;
        this.Debug = data.Debug || [];
    }

    toString() {
        const taxInfoItemsString = this.TaxInfoItems.length
            ? this.TaxInfoItems.map(taxInfo => taxInfo.toString()).join('; ')
            : 'null';
        const debugString = this.Debug.length
            ? this.Debug.join(', ')
            : 'null';
        return `GetBestMatchResponse: TaxInfoItems = [${taxInfoItemsString}], MatchLevel = ${this.MatchLevel}, Error = ${this.Error ? this.Error.toString() : 'null'}, Debug = [${debugString}]`;
    }
}

export default GetBestMatchResponse;
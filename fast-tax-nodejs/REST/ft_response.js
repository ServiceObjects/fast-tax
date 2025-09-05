/**
 * Input parameters for the GetBestMatch API call.
 */
export class GetBestMatchInput {
    constructor(data = {}) {
        this.Address = data.Address || null;
        this.Address2 = data.Address2 || null;
        this.City = data.City || null;
        this.State = data.State || null;
        this.Zip = data.Zip || null;
        this.TaxType = data.TaxType || null;
        this.LicenseKey = data.LicenseKey || null;
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
        this.Name = data.Name || null;
        this.Value = data.Value || null;
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
        this.Desc = data.Desc || null;
        this.Number = data.Number || null;
        this.Location = data.Location || null;
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
        this.Zip = data.Zip || null;
        this.City = data.City || null;
        this.County = data.County || null;
        this.StateAbbreviation = data.StateAbbreviation || null;
        this.StateName = data.StateName || null;
        this.TaxRate = data.TaxRate || null;
        this.StateRate = data.StateRate || null;
        this.CityRate = data.CityRate || null;
        this.CountyRate = data.CountyRate || null;
        this.CountyDistrictRate = data.CountyDistrictRate || null;
        this.CityDistrictRate = data.CityDistrictRate || null;
        this.SpecialDistrictRate = data.SpecialDistrictRate || null;
        this.InformationComponents = (data.InformationComponents || []).map(component => new InformationComponent(component));
        this.TotalTaxExempt = data.TotalTaxExempt || null;
        this.NotesCodes = data.NotesCodes || null;
        this.NotesDesc = data.NotesDesc || null;
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
        this.MatchLevel = data.MatchLevel || null;
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
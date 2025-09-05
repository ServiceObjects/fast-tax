from ft_response import GetBestMatchResponse, BestMatchTaxInfo, InformationComponent, Error
import requests

# Endpoint URLs for ServiceObjects FastTax (FT) API
primary_url = "https://sws.serviceobjects.com/ft/web.svc/json/GetBestMatch?"
backup_url = "https://swsbackup.serviceobjects.com/ft/web.svc/json/GetBestMatch?"
trial_url = "https://trial.serviceobjects.com/ft/web.svc/json/GetBestMatch?"

def get_best_match(
    address: str,
    address2: str,
    city: str,
    state: str,
    zip: str,
    tax_type: str,
    license_key: str,
    is_live: bool = True
) -> GetBestMatchResponse:
    """
    Call ServiceObjects FastTax (FT) API's GetBestMatch endpoint
    to retrieve tax rate information (e.g., total tax rate, city, county, state rates) for a given US address.

    Parameters:
        address: Address line of the address to get tax rates for (e.g., "123 Main Street").
        address2: Secondary address line (e.g., "Apt 4B"). Optional.
        city: The city of the address (e.g., "New York"). Optional if zip is provided.
        state: The state of the address (e.g., "NY"). Optional if zip is provided.
        zip: The ZIP code of the address. Optional if city and state are provided.
        tax_type: The type of tax to look for ("sales" or "use").
        license_key: Your ServiceObjects license key.
        is_live: Use live or trial servers.

    Returns:
        GetBestMatchResponse: Parsed JSON response with tax rate results or error details.

    Raises:
        RuntimeError: If the API returns an error payload.
        requests.RequestException: On network/HTTP failures (trial mode).
    """
    params = {
        "Address": address,
        "Address2": address2,
        "City": city,
        "State": state,
        "Zip": zip,
        "TaxType": tax_type,
        "LicenseKey": license_key,
    }
    # Select the base URL: production vs trial
    url = primary_url if is_live else trial_url

    try:
        # Attempt primary (or trial) endpoint
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        # If API returned an error in JSON payload, trigger fallback
        error = data.get('Error')
        if not (error is None or error.get('Number') != "4"):
            if is_live:
                # Try backup URL
                response = requests.get(backup_url, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()

                # If still error, propagate exception
                if 'Error' in data:
                    raise RuntimeError(f"FastTax service error: {data['Error']}")
            else:
                # Trial mode error is terminal
                raise RuntimeError(f"FastTax trial error: {data['Error']}")

        # Convert JSON response to GetBestMatchResponse for structured access
        error = Error(**data.get("Error", {})) if data.get("Error") else None

        return GetBestMatchResponse(
            TaxInfoItems=[
                BestMatchTaxInfo(
                    Zip=ti.get("Zip"),
                    City=ti.get("City"),
                    County=ti.get("County"),
                    StateAbbreviation=ti.get("StateAbbreviation"),
                    StateName=ti.get("StateName"),
                    TaxRate=ti.get("TaxRate"),
                    StateRate=ti.get("StateRate"),
                    CityRate=ti.get("CityRate"),
                    CountyRate=ti.get("CountyRate"),
                    CountyDistrictRate=ti.get("CountyDistrictRate"),
                    CityDistrictRate=ti.get("CityDistrictRate"),
                    SpecialDistrictRate=ti.get("SpecialDistrictRate"),
                    InformationComponents=[
                        InformationComponent(Name=comp.get("Name"), Value=comp.get("Value"))
                        for comp in ti.get("InformationComponents", [])
                    ] if "InformationComponents" in ti else [],
                    TotalTaxExempt=ti.get("TotalTaxExempt"),
                    NotesCodes=ti.get("NotesCodes"),
                    NotesDesc=ti.get("NotesDesc")
                )
                for ti in data.get("TaxInfoItems", [])
            ] if "TaxInfoItems" in data else [],
            MatchLevel=data.get("MatchLevel"),
            Error=error,
            Debug=data.get("Debug", [])
        )

    except requests.RequestException as req_exc:
        # Network or HTTP-level error occurred
        if is_live:
            try:
                # Fallback to backup URL
                response = requests.get(backup_url, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
                if "Error" in data:
                    raise RuntimeError(f"FastTax backup error: {data['Error']}") from req_exc

                error = Error(**data.get("Error", {})) if data.get("Error") else None

                return GetBestMatchResponse(
                    TaxInfoItems=[
                        BestMatchTaxInfo(
                            Zip=ti.get("Zip"),
                            City=ti.get("City"),
                            County=ti.get("County"),
                            StateAbbreviation=ti.get("StateAbbreviation"),
                            StateName=ti.get("StateName"),
                            TaxRate=ti.get("TaxRate"),
                            StateRate=ti.get("StateRate"),
                            CityRate=ti.get("CityRate"),
                            CountyRate=ti.get("CountyRate"),
                            CountyDistrictRate=ti.get("CountyDistrictRate"),
                            CityDistrictRate=ti.get("CityDistrictRate"),
                            SpecialDistrictRate=ti.get("SpecialDistrictRate"),
                            InformationComponents=[
                                InformationComponent(Name=comp.get("Name"), Value=comp.get("Value"))
                                for comp in ti.get("InformationComponents", [])
                            ] if "InformationComponents" in ti else [],
                            TotalTaxExempt=ti.get("TotalTaxExempt"),
                            NotesCodes=ti.get("NotesCodes"),
                            NotesDesc=ti.get("NotesDesc")
                        )
                        for ti in data.get("TaxInfoItems", [])
                    ] if "TaxInfoItems" in data else [],
                    MatchLevel=data.get("MatchLevel"),
                    Error=error,
                    Debug=data.get("Debug", [])
                )
            except Exception as backup_exc:
                raise RuntimeError("FastTax service unreachable on both endpoints") from backup_exc
        else:
            raise RuntimeError(f"FastTax trial error: {str(req_exc)}") from req_exc
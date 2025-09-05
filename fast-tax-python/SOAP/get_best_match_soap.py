from suds.client import Client
from suds import WebFault
from suds.sudsobject import Object


class GetBestMatchSoap:
    def __init__(self, license_key: str, is_live: bool = True, timeout_ms: int = 15000):
        """
        license_key: Service Objects FT license key.
        is_live: Whether to use live or trial endpoints
        timeout_ms: SOAP call timeout in milliseconds
        """
        self.is_live = is_live
        self.timeout = timeout_ms / 1000.0
        self.license_key = license_key
       

        # WSDL URLs
        self._primary_wsdl = (
            "https://sws.serviceobjects.com/ft/soap.svc?wsdl"
            if is_live
            else "https://trial.serviceobjects.com/ft/soap.svc?wsdl"
        )
        self._backup_wsdl = (
            "https://swsbackup.serviceobjects.com/ft/soap.svc?wsdl"
            if is_live
            else "https://trial.serviceobjects.com/ft/soap.svc?wsdl"
        )

    def get_best_match(
        self,
        address: str,
        address2: str,
        city: str,
        state: str,
        zip: str,
        tax_type: str,
    ) -> Object:
        """
        Calls the GetBestMatch SOAP  API to retrieve the information.

        Parameters:
            address: Address line of the address to get tax rates for (e.g., "123 Main Street").
            address2: Secondary address line (e.g., "Apt 4B"). Optional.
            city: The city of the address (e.g., "New York"). Optional if zip is provided.
            state: The state of the address (e.g., "NY"). Optional if zip is provided.
            zip: The ZIP code of the address. Optional if city and state are provided.
            tax_type: The type of tax to look for ("sales" or "use").
            license_key: Your ServiceObjects license key.
            is_live: Determines whether to use the live or trial servers.
            timeout_ms: Timeout, in milliseconds, for the call to the service.

        Returns:
            suds.sudsobject.Object: SOAP response containing tax rate details or error.
        """

        # Common kwargs for both calls
        call_kwargs = dict(
            Address=address,
            Address2=address2,
            City=city,
            State=state,
            Zip=zip,
            TaxType=tax_type,
            LicenseKey=self.license_key,
        )

        # Attempt primary
        try:
            client = Client(self._primary_wsdl)
            # Override endpoint URL if needed:
            # client.set_options(location=self._primary_wsdl.replace('?wsdl','/soap'))
            response = client.service.GetBestMatch(**call_kwargs)

            # If response invalid or Error.Number == "4", trigger fallback
            if response is None or (
                hasattr(response, "Error")
                and response.Error
                and response.Error.Number == "4"
            ):
                raise ValueError("Primary returned no result or Error.Number=4")

            return response

        except (WebFault, ValueError, Exception) as primary_ex:
            # Attempt backup
            try:
                client = Client(self._backup_wsdl)
                response = client.service.GetBestMatch(**call_kwargs)
                if response is None:
                    raise ValueError("Backup returned no result")
                return response
            except (WebFault, Exception) as backup_ex:
                msg = (
                    "Both primary and backup endpoints failed.\n"
                    f"Primary error: {str(primary_ex)}\n"
                    f"Backup error: {str(backup_ex)}"
                )
                raise RuntimeError(msg)
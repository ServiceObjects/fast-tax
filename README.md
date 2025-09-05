![Service Objects Logo](https://www.serviceobjects.com/wp-content/uploads/2021/05/SO-Logo-with-TM.gif "Service Objects Logo")

# FT - FastTax

DOTS FastTax (referred to as FastTax or FT) is a publicly available XML and JSON web service that provides sales tax rate information for all US areas based on several different inputs. The service provides zip, city, county, county fips codes, state, tax rates and exemptions. 

FastTax can provide instant sales tax rates for any address, zip code, city or county in the United States.

## [Service Objects Website](https://serviceobjects.com)
## [Developer Guide/Documentation](https://www.serviceobjects.com/docs/)

# FT - GetBestMatch

GetBestMatch: Returns sales or use tax rates based on address information. If the address information fails, it will provide a zip code level match. This operation can return multiple tax rates for zip Level matches.

## [GetBestMatch Developer Guide/Documentation](https://www.serviceobjects.com/docs/dots-fasttax/ft-operations/ft-getbestmatch-recommended-operation/)

## GetBestMatches Request URLs (Query String Parameters)

>[!CAUTION]
>### *Important - Use query string parameters for all inputs.  Do not use path parameters since it will lead to errors due to optional parameters and special character issues.*


### JSON
#### Trial

https://trial.serviceobjects.com/ft/web.svc/JSON/GetBestMatch?Address=27+E+Cota+St&Address2=&City=Santa+Barbara&State=CA&Zip=93101&TaxType=sales&LicenseKey=
{LicenseKey}

#### Production

https://sws.serviceobjects.com/ft/web.svc/JSON/GetBestMatch?Address=27+E+Cota+St&Address2=&City=Santa+Barbara&State=CA&Zip=93101&TaxType=sales&LicenseKey={LicenseKey}

#### Production Backup

https://swsbackup.serviceobjects.com/ft/web.svc/JSON/GetBestMatch?Address=27+E+Cota+St&Address2=&City=Santa+Barbara&State=CA&Zip=93101&TaxType=sales&LicenseKey={LicenseKey}

### XML
#### Trial

https://trial.serviceobjects.com/ft/web.svc/XML/GetBestMatch?Address=27+E+Cota+St&Address2=&City=Santa+Barbara&State=CA&Zip=93101&TaxType=sales&LicenseKey={LicenseKey}

#### Production

https://sws.serviceobjects.com/ft/web.svc/XML/GetBestMatch?Address=27+E+Cota+St&Address2=&City=Santa+Barbara&State=CA&Zip=93101&TaxType=sales&LicenseKey={LicenseKey}

#### Production Backup

https://swsbackup.serviceobjects.com/ft/web.svc/XML/GetBestMatch?Address=27+E+Cota+St&Address2=&City=Santa+Barbara&State=CA&Zip=93101&TaxType=sales&LicenseKey={LicenseKey}

https://swsbackup.serviceobjects.com/AV3/api.svc/GetSecondaryNumbers?Address=27+E+Cota+St&City=Santa+Barbara&State=CA&PostalCode=93101&LicenseKey={LicenseKey}


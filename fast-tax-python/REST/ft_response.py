from dataclasses import dataclass
from typing import Optional, List


@dataclass
class GetBestMatchInput:
    Address: Optional[str] = None
    Address2: Optional[str] = None
    City: Optional[str] = None
    State: Optional[str] = None
    Zip: Optional[str] = None
    TaxType: Optional[str] = None
    LicenseKey: Optional[str] = None
    IsLive: bool = True
    TimeoutSeconds: int = 15

    def __str__(self) -> str:
        return (f"GetBestMatchInput: Address={self.Address}, Address2={self.Address2}, City={self.City}, "
                f"State={self.State}, Zip={self.Zip}, TaxType={self.TaxType}, LicenseKey={self.LicenseKey}, "
                f"IsLive={self.IsLive}, TimeoutSeconds={self.TimeoutSeconds}")


@dataclass
class InformationComponent:
    Name: Optional[str] = None
    Value: Optional[str] = None

    def __str__(self) -> str:
        return f"InformationComponent: Name={self.Name}, Value={self.Value}"


@dataclass
class Error:
    Desc: Optional[str] = None
    Number: Optional[str] = None
    Location: Optional[str] = None

    def __str__(self) -> str:
        return f"Error: Desc={self.Desc}, Number={self.Number}, Location={self.Location}"


@dataclass
class BestMatchTaxInfo:
    Zip: Optional[str] = None
    City: Optional[str] = None
    County: Optional[str] = None
    StateAbbreviation: Optional[str] = None
    StateName: Optional[str] = None
    TaxRate: Optional[float] = None
    StateRate: Optional[float] = None
    CityRate: Optional[float] = None
    CountyRate: Optional[float] = None
    CountyDistrictRate: Optional[float] = None
    CityDistrictRate: Optional[float] = None
    SpecialDistrictRate: Optional[float] = None
    InformationComponents: Optional[List['InformationComponent']] = None
    TotalTaxExempt: Optional[str] = None
    NotesCodes: Optional[str] = None
    NotesDesc: Optional[str] = None

    def __post_init__(self):
        if self.InformationComponents is None:
            self.InformationComponents = []

    def __str__(self) -> str:
        components_string = ', '.join(str(component) for component in self.InformationComponents) if self.InformationComponents else 'None'
        return (f"BestMatchTaxInfo: Zip={self.Zip}, City={self.City}, County={self.County}, "
                f"StateAbbreviation={self.StateAbbreviation}, StateName={self.StateName}, "
                f"TaxRate={self.TaxRate}, StateRate={self.StateRate}, CityRate={self.CityRate}, "
                f"CountyRate={self.CountyRate}, CountyDistrictRate={self.CountyDistrictRate}, "
                f"CityDistrictRate={self.CityDistrictRate}, SpecialDistrictRate={self.SpecialDistrictRate}, "
                f"InformationComponents=[{components_string}], TotalTaxExempt={self.TotalTaxExempt}, "
                f"NotesCodes={self.NotesCodes}, NotesDesc={self.NotesDesc}")


@dataclass
class GetBestMatchResponse:
    TaxInfoItems: Optional[List['BestMatchTaxInfo']] = None
    MatchLevel: Optional[str] = None
    Error: Optional['Error'] = None
    Debug: Optional[List[str]] = None

    def __post_init__(self):
        if self.TaxInfoItems is None:
            self.TaxInfoItems = []
        if self.Debug is None:
            self.Debug = []

    def __str__(self) -> str:
        tax_info_string = '; '.join(str(tax_info) for tax_info in self.TaxInfoItems) if self.TaxInfoItems else 'None'
        debug_string = ', '.join(self.Debug) if self.Debug else 'None'
        error = str(self.Error) if self.Error else 'None'
        return (f"GetBestMatchResponse: TaxInfoItems=[{tax_info_string}], MatchLevel={self.MatchLevel}, "
                f"Error={error}, Debug=[{debug_string}]")

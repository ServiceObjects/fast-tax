using System.Runtime.Serialization;
using System.Linq;

namespace fast_tax_dot_net.REST
{
    /// <summary>
    /// Response from GetBestMatch API, containing tax rate information for the best match.
    /// </summary>
    [DataContract]
    public class GetBestMatchResponse
    {
        public BestMatchTaxInfo[] TaxInfoItems { get; set; }
        public string MatchLevel { get; set; }
        public Error Error { get; set; }
        public string[] Debug { get; set; }

        public override string ToString()
        {
            string taxInfoItemsStr = TaxInfoItems != null
                ? string.Join("\n", TaxInfoItems.Select(taxInfo => taxInfo.ToString()))
                : "null";
            string debugStr = Debug != null
                ? string.Join(", ", Debug)
                : "null";
            return $"GetBestMatchResponse:\n" +
                   $"TaxInfoItems:\n{taxInfoItemsStr}\n" +
                   $"MatchLevel: {MatchLevel}\n" +
                   $"Error: {(Error != null ? Error.ToString() : "null")}\n" +
                   $"Debug: [{debugStr}]";
        }
    }

    /// <summary>
    /// Tax information for a matched address or ZIP code.
    /// </summary>
    [DataContract]
    public class BestMatchTaxInfo
    {
        public string Zip { get; set; }
        public string City { get; set; }
        public string County { get; set; }
        public string StateAbbreviation { get; set; }
        public string StateName { get; set; }
        public string TaxRate { get; set; }
        public string StateRate { get; set; }
        public string CityRate { get; set; }
        public string CountyRate { get; set; }
        public string CountyDistrictRate { get; set; }
        public string CityDistrictRate { get; set; }
        public string SpecialDistrictRate { get; set; }
        public InformationComponent[] InformationComponents { get; set; }
        public string TotalTaxExempt { get; set; }
        public string NotesCodes { get; set; }
        public string NotesDesc { get; set; }
        public override string ToString()
        {
            string infoComponentsStr = InformationComponents != null
                ? string.Join(", ", InformationComponents.Select(ic => ic.ToString()))
                : "null";
            return $"BestMatchTaxInfo:\n" +
                   $"Zip: {Zip}\n" +
                   $"City: {City}\n" +
                   $"County: {County}\n" +
                   $"StateAbbreviation: {StateAbbreviation}\n" +
                   $"StateName: {StateName}\n" +
                   $"TaxRate: {TaxRate}\n" +
                   $"StateRate: {StateRate}\n" +
                   $"CityRate: {CityRate}\n" +
                   $"CountyRate: {CountyRate}\n" +
                   $"CountyDistrictRate: {CountyDistrictRate}\n" +
                   $"CityDistrictRate: {CityDistrictRate}\n" +
                   $"SpecialDistrictRate: {SpecialDistrictRate}\n" +
                   $"InformationComponents: [{infoComponentsStr}]\n" +
                   $"TotalTaxExempt: {TotalTaxExempt}\n" +
                   $"NotesCodes: {NotesCodes}\n" +
                   $"NotesDesc: {NotesDesc}";
        }
    }

    /// <summary>
    /// Information component containing name-value pairs for additional tax information.
    /// </summary>
    [DataContract]
    public class InformationComponent
    {
        public string Name { get; set; }
        public string Value { get; set; }
        public override string ToString()
        {
            return $"Name: {Name}, Value: {Value}";
        }
    }

    /// <summary>
    /// Error object for API responses.
    /// </summary>
    [DataContract]
    public class Error
    {
        public string Desc { get; set; }
        public string Number { get; set; }
        public string Location { get; set; }
        public override string ToString()
        {
            return $"Desc: {Desc}, Number: {Number}, Location: {Location}";
        }
    }
}
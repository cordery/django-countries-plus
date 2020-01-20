import pytest

from countries_plus.models import Country
from countries_plus.utils import parse_geonames_data, GeonamesParseError, update_geonames_data


@pytest.mark.django_db
class TestParseGeonamesData:

    @pytest.fixture
    def valid_data(self):
        return [
            u"#ISO	ISO3	ISO-Numeric	fips	Country	Capital	Area(in sq km)	Population	Continent	tld	CurrencyCode	CurrencyName	Phone	Postal Code Format	Postal Code Regex	Languages	geonameid	neighbours	EquivalentFipsCode".encode(),
            u"AD	AND	020	AN	Andorra	Andorra la Vella	468	84000	EU	.ad	EUR	Euro	376	AD###	^(?:AD)*(\d{3})$	ca	3041565	ES,FR	".encode()
        ]

    @pytest.fixture
    def invalid_data_no_header(self):
        return [
            u"AD	AND	020	AN	Andorra	Andorra la Vella	468	84000	EU	.ad	EUR	Euro	376	AD###	^(?:AD)*(\d{3})$	ca	3041565	ES,FR	".encode()
        ]

    @pytest.fixture
    def invalid_data_bad_header(self):
        return [
            u"#ISO  Country	Capital	Area(in sq km)	Population	Continent	tld	CurrencyCode	CurrencyName	Phone	Postal Code Format	Postal Code Regex	Languages	geonameid	neighbours	EquivalentFipsCode".encode(),
            u"AD	AND	020	AN	Andorra	Andorra la Vella	468	84000	EU	.ad	EUR	Euro	376	AD###	^(?:AD)*(\d{3})$	ca	3041565	ES,FR	".encode()
        ]

    @pytest.fixture
    def invalid_data_invalid_field_length(self):
        return [
            u"#ISO	ISO3	ISO-Numeric	fips	Country	Capital	Area(in sq km)	Population	Continent	tld	CurrencyCode	CurrencyName	Phone	Postal Code Format	Postal Code Regex	Languages	geonameid	neighbours	EquivalentFipsCode".encode(),
            u"AD	INVALID_ISO3	020	AN	Andorra	Andorra la Vella	468	84000	EU	.ad	EUR	Euro	376	AD###	^(?:AD)*(\d{3})$	ca	3041565	ES,FR	".encode()
        ]

    def test_valid_data(self, valid_data):
        parse_geonames_data(iter(valid_data))
        assert Country.objects.count() == 1

    def test_invalid_data_no_header(self, invalid_data_no_header):
        with pytest.raises(GeonamesParseError):
            parse_geonames_data(iter(invalid_data_no_header))

    def test_invalid_data_bad_header(self, invalid_data_bad_header):
        with pytest.raises(GeonamesParseError):
            parse_geonames_data(iter(invalid_data_bad_header))

    def test_invalid_data_field_length(self, invalid_data_invalid_field_length):
        with pytest.raises(GeonamesParseError):
            parse_geonames_data(iter(invalid_data_invalid_field_length))

    def test_invalid_data_field_length_update(self, valid_data, invalid_data_invalid_field_length):
        parse_geonames_data(iter(valid_data))
        with pytest.raises(GeonamesParseError):
            parse_geonames_data(iter(invalid_data_invalid_field_length))


@pytest.mark.django_db
class TestUpdateGeonamesData:

    def test_update_geonames_data(self):
        # If the geonames.org dataset adds/removes a country or changes its format
        # this test will fail, which is intended.
        num_updated, num_created = update_geonames_data()
        assert num_updated == 0
        assert num_created == 252

        num_updated, num_created = update_geonames_data()
        assert num_updated == 252
        assert num_created == 0

        assert Country.objects.count() == 252

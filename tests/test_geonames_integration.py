from django.test import TestCase

from countries_plus.models import Country
from countries_plus.utils import update_geonames_data, parse_geonames_data, GeonamesParseError


class TestUpdateGeonamesData(TestCase):
    def setUp(self):
        Country.objects.all().delete()

    def tearDown(self):
        Country.objects.all().delete()

    def test_update_geonames_data(self):
        # If the geonames.org dataset adds/removes a country or changes its format
        # this test will fail, which is intended.
        num_updated, num_created = update_geonames_data()
        self.assertEqual(num_updated, 0)
        self.assertEqual(num_created, 252)

        num_updated, num_created = update_geonames_data()
        self.assertEqual(num_updated, 252)
        self.assertEqual(num_created, 0)

        self.assertEqual(Country.objects.count(), 252)


class TestParseGeonamesData(TestCase):
    valid_data = [
        u"#ISO	ISO3	ISO-Numeric	fips	Country	Capital	Area(in sq km)	Population	"
        u"Continent	tld	CurrencyCode	CurrencyName	Phone	Postal Code Format	Postal Code "
        u"Regex	Languages	geonameid	neighbours	EquivalentFipsCode".encode(),
        u"AD	AND	020	AN	Andorra	Andorra la Vella	468	84000	EU	.ad	EUR	Euro	376	"
        u"AD###	^(?:AD)*(\d{3})$	ca	3041565	ES,FR	".encode()
    ]
    invalid_data_no_header = [
        u"AD	AND	020	AN	Andorra	Andorra la Vella	468	84000	EU	.ad	EUR	Euro	376	"
        u"AD###	^(?:AD)*(\d{3})$	ca	3041565	ES,FR	".encode()
    ]
    invalid_data_bad_header = [
        u"#ISO  Country	Capital	Area(in sq km)	Population	Continent	tld	CurrencyCode	"
        u"CurrencyName	Phone	Postal Code Format	Postal Code Regex	Languages	geonameid	"
        u"neighbours	EquivalentFipsCode".encode(),
        u"AD	AND	020	AN	Andorra	Andorra la Vella	468	84000	EU	.ad	EUR	Euro	376	"
        u"AD###	^(?:AD)*(\d{3})$	ca	3041565	ES,FR	".encode()
    ]
    invalid_data_invalid_field_length = [
        u"#ISO	ISO3	ISO-Numeric	fips	Country	Capital	Area(in sq km)	Population	"
        u"Continent	tld	CurrencyCode	CurrencyName	Phone	Postal Code Format	Postal Code "
        u"Regex	Languages	geonameid	neighbours	EquivalentFipsCode".encode(),
        u"AD	INVALID_ISO3	020	AN	Andorra	Andorra la Vella	468	84000	EU	.ad	EUR	"
        u"Euro	376	AD###	^(?:AD)*(\d{3})$	ca	3041565	ES,FR	".encode()
    ]

    def setUp(self):
        Country.objects.all().delete()

    def tearDown(self):
        Country.objects.all().delete()

    def test_valid_data(self):
        parse_geonames_data(iter(self.valid_data))
        self.assertEqual(Country.objects.count(), 1)

    def test_invalid_data_no_header(self):
        with self.assertRaises(GeonamesParseError):
            parse_geonames_data(iter(self.invalid_data_no_header))

    def test_invalid_data_bad_header(self):
        with self.assertRaises(GeonamesParseError):
            parse_geonames_data(iter(self.invalid_data_bad_header))

    def test_invalid_data_field_length(self):
        with self.assertRaises(GeonamesParseError):
            parse_geonames_data(iter(self.invalid_data_invalid_field_length))

    def test_invalid_data_field_length_update(self):
        parse_geonames_data(iter(self.valid_data))
        with self.assertRaises(GeonamesParseError):
            parse_geonames_data(iter(self.invalid_data_invalid_field_length))

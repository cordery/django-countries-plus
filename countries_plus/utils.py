# coding=utf-8
import re
from typing import Iterable, Tuple

import requests
from django.core.exceptions import ValidationError

from .models import Country

DATA_HEADERS_ORDERED = [
    'ISO',
    'ISO3',
    'ISO-Numeric',
    'fips',
    'Country',
    'Capital',
    'Area(in sq km)',
    'Population',
    'Continent',
    'tld',
    'CurrencyCode',
    'CurrencyName',
    'Phone',
    'Postal Code Format',
    'Postal Code Regex',
    'Languages',
    'geonameid',
    'neighbours',
    'EquivalentFipsCode',
]

DATA_HEADERS_MAP = {
    'ISO': 'iso',
    'ISO3': 'iso3',
    'ISO-Numeric': 'iso_numeric',
    'fips': 'fips',
    'Country': 'name',
    'Capital': 'capital',
    'Area(in sq km)': 'area',
    'Population': 'population',
    'Continent': 'continent',
    'tld': 'tld',
    'CurrencyCode': 'currency_code',
    'CurrencyName': 'currency_name',
    'Phone': 'phone',
    'Postal Code Format': 'postal_code_format',
    'Postal Code Regex': 'postal_code_regex',
    'Languages': 'languages',
    'geonameid': 'geonameid',
    'neighbours': 'neighbours',
    'EquivalentFipsCode': 'equivalent_fips_code',
}

CURRENCY_SYMBOLS = {
    "AED": "د.إ",
    "AFN": "؋",
    "ALL": "L",
    "AMD": "դր.",
    "ANG": "ƒ",
    "AOA": "Kz",
    "ARS": "$",
    "AUD": "$",
    "AWG": "ƒ",
    "AZN": "m",
    "BAM": "KM",
    "BBD": "$",
    "BDT": "৳",
    "BGN": "лв",
    "BHD": "ب.د",
    "BIF": "Fr",
    "BMD": "$",
    "BND": "$",
    "BOB": "Bs.",
    "BRL": "R$",
    "BSD": "$",
    "BTN": "Nu",
    "BWP": "P",
    "BYR": "Br",
    "BZD": "$",
    "CAD": "$",
    "CDF": "Fr",
    "CHF": "Fr",
    "CLP": "$",
    "CNY": "¥",
    "COP": "$",
    "CRC": "₡",
    "CUP": "$",
    "CVE": "$, Esc",
    "CZK": "Kč",
    "DJF": "Fr",
    "DKK": "kr",
    "DOP": "$",
    "DZD": "د.ج",
    "EEK": "KR",
    "EGP": "£,ج.م",
    "ERN": "Nfk",
    "ETB": "Br",
    "EUR": "€",
    "FJD": "$",
    "FKP": "£",
    "GBP": "£",
    "GEL": "ლ",
    "GHS": "₵",
    "GIP": "£",
    "GMD": "D",
    "GNF": "Fr",
    "GTQ": "Q",
    "GYD": "$",
    "HKD": "$",
    "HNL": "L",
    "HRK": "kn",
    "HTG": "G",
    "HUF": "Ft",
    "IDR": "Rp",
    "ILS": "₪",
    "INR": "₨",
    "IQD": "ع.د",
    "IRR": "﷼",
    "ISK": "kr",
    "JMD": "$",
    "JOD": "د.ا",
    "JPY": "¥",
    "KES": "Sh",
    "KGS": "лв",
    "KHR": "៛",
    "KMF": "Fr",
    "KPW": "₩",
    "KRW": "₩",
    "KWD": "د.ك",
    "KYD": "$",
    "KZT": "Т",
    "LAK": "₭",
    "LBP": "ل.ل",
    "LKR": "ரூ",
    "LRD": "$",
    "LSL": "L",
    "LTL": "Lt",
    "LVL": "Ls",
    "LYD": "ل.د",
    "MAD": "د.م.",
    "MDL": "L",
    "MGA": "Ar",
    "MKD": "ден",
    "MMK": "K",
    "MNT": "₮",
    "MOP": "P",
    "MRO": "UM",
    "MUR": "₨",
    "MVR": "ރ.",
    "MWK": "MK",
    "MXN": "$",
    "MYR": "RM",
    "MZN": "MT",
    "NAD": "$",
    "NGN": "₦",
    "NIO": "C$",
    "NOK": "kr",
    "NPR": "₨",
    "NZD": "$",
    "OMR": "ر.ع.",
    "PAB": "B/.",
    "PEN": "S/.",
    "PGK": "K",
    "PHP": "₱",
    "PKR": "₨",
    "PLN": "zł",
    "PYG": "₲",
    "QAR": "ر.ق",
    "RON": "RON",
    "RSD": "RSD",
    "RUB": "р.",
    "RWF": "Fr",
    "SAR": "ر.س",
    "SBD": "$",
    "SCR": "₨",
    "SDG": "S$",
    "SEK": "kr",
    "SGD": "$",
    "SHP": "£",
    "SLL": "Le",
    "SOS": "Sh",
    "SRD": "$",
    "STD": "Db",
    "SYP": "£, ل.س",
    "SZL": "L",
    "THB": "฿",
    "TJS": "ЅМ",
    "TMT": "m",
    "TND": "د.ت",
    "TOP": "T$",
    "TRY": "₤",
    "TTD": "$",
    "TWD": "$",
    "TZS": "Sh",
    "UAH": "₴",
    "UGX": "Sh",
    "USD": "$",
    "UYU": "$",
    "UZS": "лв",
    "VEF": "Bs",
    "VND": "₫",
    "VUV": "Vt",
    "WST": "T",
    "XAF": "Fr",
    "XCD": "$",
    "XOF": "Fr",
    "XPF": "Fr",
    "YER": "﷼",
    "ZAR": "R",
    "ZMK": "ZK",
    "ZWL": "$",
}


class GeonamesParseError(Exception):
    def __init__(self, message=None):
        super().__init__(
            (
                "I couldn't parse the Geonames file (http://download.geonames.org/export/dump/countryInfo.txt).  "
                "The format may have changed. An updated version of this software may be required, please check for "
                f"updates and/or raise an issue on github.  Specific error: {message}"
            )
        )


def update_geonames_data():
    """
    Requests the countries table from geonames.org, and then calls parse_geonames_data to parse it.
    :return: num_updated, num_created
    :raise GeonamesParseError:
    """
    r = requests.get(
        'http://download.geonames.org/export/dump/countryInfo.txt', stream=True
    )
    return parse_geonames_data(r.iter_lines())


def parse_geonames_data(lines_iterator: Iterable) -> Tuple[int, int]:
    """Parse countries table data from geonames.org, updating or adding records as needed.

    'currency_symbol' is not part of the countries table itself and is supplemented using the data
    obtained from the link provided in the countries table.

    :param lines_iterator: the lines to parse.
    :return: num_updated: int, num_created: int
    :raise GeonamesParseError:
    """
    data_headers = []
    num_created = 0
    num_updated = 0
    for line in lines_iterator:
        line = line.decode()
        if len(line) == 0:
            continue
        if line[0] == "#":
            if line[0:4] == "#ISO":
                data_headers = line.strip('# ').split('\t')
                if data_headers != DATA_HEADERS_ORDERED:
                    raise GeonamesParseError(
                        "The table headers do not match the expected headers."
                    )
            continue
        if not data_headers:
            raise GeonamesParseError("No table headers found.")
        bits = line.split('\t')

        data = {
            DATA_HEADERS_MAP[DATA_HEADERS_ORDERED[x]]: bits[x]
            for x in range(0, len(bits))
        }
        if 'currency_code' in data and data['currency_code']:
            data['currency_symbol'] = CURRENCY_SYMBOLS.get(data['currency_code'])

        # Remove empty items
        clean_data = {x: y for x, y in data.items() if y}

        # Puerto Rico and the Dominican Republic have two phone prefixes in the format "123 and
        # 456"
        if 'phone' in clean_data:
            if 'and' in clean_data['phone']:
                clean_data['phone'] = ",".join(
                    re.split(r'\s*and\s*', clean_data['phone'])
                )

        # Avoiding update_or_create to maintain compatibility with Django 1.5
        try:
            country = Country.objects.get(iso=clean_data['iso'])
            created = False
        except Country.DoesNotExist:
            try:
                country = Country.objects.create(**clean_data)
            except ValidationError as e:
                raise GeonamesParseError("Unexpected field length: %s" % e.message_dict)
            created = True

        for k, v in clean_data.items():
            setattr(country, k, v)

        try:
            country.save()
        except ValidationError as e:
            raise GeonamesParseError("Unexpected field length: %s" % e.message_dict)

        if created:
            num_created += 1
        else:
            num_updated += 1
    return num_updated, num_created

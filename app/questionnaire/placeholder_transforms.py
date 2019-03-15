from datetime import datetime
from dateutil.relativedelta import relativedelta

from babel.numbers import format_currency
from babel.dates import format_datetime
from babel import numbers
from app.settings import DEFAULT_LOCALE


class PlaceholderTransforms:
    """
    A class to group the transforms that can be used within placeholders
    """
    locale = DEFAULT_LOCALE
    input_date_format = '%Y-%m-%d'

    def format_currency(self, number=None, currency='GBP'):
        return format_currency(number, currency, locale=self.locale)

    def format_date(self, date_to_format, date_format):
        date_to_format = datetime.strptime(date_to_format, self.input_date_format)
        return format_datetime(date_to_format, date_format, locale=self.locale)

    @staticmethod
    def format_list(list_to_format):
        formatted_list = '<ul>'
        for item in list_to_format:
            formatted_list += '<li>{}</li>'.format(item)
        formatted_list += '</ul>'

        return formatted_list

    @staticmethod
    def remove_empty(list_to_filter):
        return [item for item in list_to_filter if item]

    @staticmethod
    def concatenate_list(list_to_concatenate, delimiter):
        return delimiter.join(list_to_concatenate)

    @staticmethod
    def format_possessive(string_to_format):
        if string_to_format:
            lowered_string = string_to_format.lower()

            if lowered_string.endswith("'s") or lowered_string.endswith('’s'):
                return string_to_format[:-2] + '’s'

            if lowered_string[-1:] == 's':
                return string_to_format + '’'

            return string_to_format + '’s'

    @staticmethod
    def format_number(number):
        if number or number == 0:
            return numbers.format_decimal(number, locale=PlaceholderTransforms.locale)

        return ''

    def calculate_years_difference(self, first_date, second_date):
        first_date = datetime.now() if first_date == 'now' else datetime.strptime(first_date, self.input_date_format)
        second_date = datetime.now() if second_date == 'now' else datetime.strptime(second_date, self.input_date_format)

        return str(relativedelta(second_date, first_date).years)

    @staticmethod
    def first_non_empty_item(items):
        """
        :param items: anything that is iterable
        :return: first non empty value

        In this filter the following values are considered non empty:
        - None
        - any empty sequence, for example, '', (), [].
        - any empty mapping, for example, {}.

         Note: to guarantee the returned element is actually the first non empty element in the iterable,
        'items' must be a data structure that preserves order, ie tuple, list etc.
        If order is not important, this can be reused to return `one of` the elements which is non empty.

        This filter will treat zero of any numeric type for example, 0, 0.0, 0j and boolean 'False'
        as a valid item since they are naturally 'falsy' in Python but not empty.

        Note: Booleans are a subtype of integers. Zero of any numeric type 'is not False' but 'equals False'.
        Reference: https://docs.python.org/release/3.4.2/library/stdtypes.html?highlight=boolean#boolean-values
        """
        for item in items:
            if item or item is False or item == 0:
                return item

        return ''


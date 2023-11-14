## unit tests for RESTClientObject

from pyfx.dispatch.oanda.test import ComponentTest
from pyfx.dispatch.oanda.rest import RESTClientObject, UTF8_RE_MATCH, CHARSET_RE_GROUP

import unittest
from assertpy import assert_that

CONTENT_REST: str = "application/json; charset=UTF-8"
CONTENT_STREAM: str = "application/octet-stream"
CONTENT_HTML: str = "text/html; charset=ISO-88859-8-I"


class TestRESTClientObject(ComponentTest):
    """Unit tests for RESTClientObject"""

    def test_charset_re(self):
        '''test regular expression patterns for RESTCLientObject'''
        rest_tail = CONTENT_REST.split(";", maxsplit=1)[1]
        stream_tail = ""
        html_tail = CONTENT_HTML.split(";", maxsplit=1)[1]
        assert_that(UTF8_RE_MATCH.match(rest_tail)).is_not_none()
        assert_that(UTF8_RE_MATCH.match(stream_tail)).is_none()
        assert_that(UTF8_RE_MATCH.match(html_tail)).is_none()

        html_charset_match = CHARSET_RE_GROUP.match(html_tail)
        assert_that(html_charset_match).is_not_none()
        assert_that(html_charset_match.group(1)).is_equal_to("ISO-88859-8-I")


if __name__ == '__main__':
    unittest.main()

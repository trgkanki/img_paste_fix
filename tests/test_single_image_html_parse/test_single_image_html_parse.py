import sys
import os

sys.path.insert(
    1, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src/html_parser"))
)


from single_image_html_parse import single_image_html_parse


def test_dict_setitem():
    assert single_image_html_parse("<img src='aa.png'>")["src"] == "aa.png"
    assert single_image_html_parse("<img src='aa.png' alt='aas'>")["alt"] == "aas"
    assert single_image_html_parse("<img src='aa.png' />")["src"] == "aa.png"
    assert single_image_html_parse("<img src='aa.png'>a") is None
    assert single_image_html_parse("<div><img src='aa.png'></div>") is None
    assert single_image_html_parse("<div></div><img src='aa.png'>") is None
    assert single_image_html_parse("a") is None

from drizm_commons.testing import self_to_id


def test__self_to_id():
    """
    GIVEN I have a JSONified body
        AND that body matches the Drizm HATEOAS format
    WHEN I extract the identifier from a valid URI
    THEN I should be get back a valid identifier
    """
    test_key = 1
    test_body = {
        "self": {
            "href": f"http://example.net/resources/{test_key}/"
        }
    }
    found_key = self_to_id(test_body)
    assert found_key == test_key
    assert type(found_key) == int

    test_key = "rgftbiuftbiubtiu"
    test_body = lambda k: {
        "self": {
            "href": f"https://www.bsdomain.com/resources/okay/{k}"
                    "?state=1&mode=test"
        }
    }

    found_key = self_to_id(test_body(test_key))
    assert found_key == test_key
    assert type(found_key) == str

    test_key = 30
    found_key = self_to_id(test_body(test_key))
    assert found_key == test_key
    assert type(found_key) == int

    found_key = self_to_id(test_body(test_key), force_str=True)
    assert found_key == str(test_key)
    assert type(found_key) == str

from typing import Dict, Union


def self_to_id(body: Dict[str, Union[str, dict]]) -> Union[str, int]:
    """
    Looks for the self attribute of a response (like so):
    {
        "self": {"href": "http://example.net/resources/1/"}
        ...
    }
    and then extracts the id out of the provided hyperlink.

    :param body: The full JSON response-body, must be compliant
    with the expected Drizm response-schema
    """
    identifier = [
        i for i in body["self"].get("href").split("/") if i
    ][-1]

    try:
        # Try and convert this into a numeric id
        identifier = int(identifier)

    except TypeError or ValueError:
        # if that fails, we know it must be something like a UUID
        pass

    finally:
        return identifier


__all__ = ["self_to_id"]

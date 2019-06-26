import unittest
from bs4 import BeautifulSoup


def test_laundry(payload):
    name = BeautifulSoup(str(payload.pop(0)), "html.parser").find("a").text.lower().replace(" ", "-")

    # split the number available and number in use
    washer = BeautifulSoup(str(payload.pop(1)), "html.parser").text.split("/")
    drier = BeautifulSoup(str(payload.pop(2)), "html.parser").text.split("/")

    # format into dictionary
    return({
        "dorm": name,
        "washer": {
            "available": int(washer[0][:-1]),
            "total": int(washer[1][1:]),
        },
        "drier": {
            "available": int(drier[0][:-1]),
            "total": int(drier[1][1:]),
        }
    })


class Test(unittest.TestCase):
    def test(self):
        payload = [
            "[<td align=\"left\"><a href=\"javascript:void(0)\" onclick=\"loaddetail(13);\">Easton Hall</a></td>",
            "<td><input checked=\"true\" onclick=\"updateFavorites(13, this);\" type=\"checkbox\"/></td>",
            "<td><big>6</big> / 8</td>",
            "<td><small>0</small></td>",
            "<td><big>0</big> / 8</td>",
            "<td><small>0</small></td>]"
        ]

        result = {
            "dorm": "easton-hall",
            "washer": {
                "available": 6,
                "total": 8,
            },
            "drier": {
                "available": 0,
                "total": 8,
            }
        }

        self.assertEqual(test_laundry(payload), result)


if __name__ == '__main__':
    unittest.main()

import unittest
import sys
from unittest import mock
from pathlib import Path

test_dir = Path(__file__).absolute().parent
main_dir = test_dir.parent
sys.path.append(str(main_dir))

from yt_dlp_helper import YtDlpHelper

test_url = "https://www.youtube.com/watch?v=BaW_jenozKc"


class TestURL(unittest.TestCase):
    def test_url(self):
        test_helper = YtDlpHelper()
        with mock.patch("builtins.input", return_value=test_url):
            self.assertEqual(test_helper.get_url(), test_url)


if __name__ == "__main__":
    unittest.main()

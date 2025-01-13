import unittest
import toml
from get_moji_collection import get_word_list_of_moji_collection


class TestFunc1(unittest.TestCase):
    def test_get_word_list_of_moji_collection(self):
        res = get_word_list_of_moji_collection(col_id='buUXwKnDFz')
        print(res)

    def test_get_config(self):
        config = toml.load("./.env.toml")
        collect_map = config["moji"]["collection_dict"]
        print(collect_map)
        pass


if __name__ == '__main__':
    unittest.main()
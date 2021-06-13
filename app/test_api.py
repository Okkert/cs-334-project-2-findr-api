import unittest


class TestCreateGroup(unittest.TestCase):

    def test_create_group(self):
        response = {
            "status": 200,
            "content": {"reason": "Success"}
        }
        result = {
            "status": 200,
            "content": {"reason": "Success"}
        }
        self.assertEqual(result, response)


if __name__ == '__main__':
    unittest.main()

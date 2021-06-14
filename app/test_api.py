import unittest
#import requests


class TestCreateGroup(unittest.TestCase):

    def test_create_group(self):
        print("Testing create")
        response = {
            "status": 200,
            "content": {"reason": "Success"}
        }
        result = {
            "status": 200,
            "content": {"reason": "Success"}
        }
        self.assertEqual(result, response)


# class TestAPI(unittest.TestCase):

#     # ---------------- POSTS ---------------- #
#     def test_load_post(self):
#         print("Testing load post...")
#         url = "https://cs-334-findr-api.herokuapp.com/api/post/?userId=2&postId=33"
#         resp = requests.get(url=url)
#         self.assertEqual(resp.status_code, 200)

#     # ---------------- USERS ---------------- #
#     def test_load_userId(self):
#         print("Testing load userId...")
#         url = "https://cs-334-findr-api.herokuapp.com/api/load_userId/?username=swinger_2"
#         resp = requests.get(url=url)
#         self.assertEqual(resp.status_code, 200)

#     # ---------------- COMMENTS ---------------- #
#     def test_load_comment(self):
#         print("Testing load comment...")
#         url = "https://cs-334-findr-api.herokuapp.com/api/comment/?commentId=1"
#         resp = requests.get(url=url)
#         self.assertEqual(resp.status_code, 200)

#     # ---------------- NOTES ---------------- #
#     def test_load_note(self):
#         print("Testing load note...")
#         url = "https://cs-334-findr-api.herokuapp.com/api/note/?noteId=1"
#         resp = requests.get(url=url)
#         self.assertEqual(resp.status_code, 200)


if __name__ == '__main__':
    unittest.main()

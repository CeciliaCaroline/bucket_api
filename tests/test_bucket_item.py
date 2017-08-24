from tests.base import BaseTestCase
import unittest
import json


class TestBucketItem(BaseTestCase):
    def test_item_post_request_content_type(self):
        """
        Test that the correct response is returned if the request payload content type is not application/json
        :return:
        """
        with self.client:
            response = self.client.post(
                '/bucketlists/1/items',
                data=json.dumps(dict(name='food')),
                content_type='application/javascript',
                headers=dict(Authorization='Bearer ' + self.get_user_token())
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Content-type must be application/json')
            self.assertEqual(response.status_code, 401)

    def test_bucket_id_is_invalid_in_request(self):
        """
        Test that the bucket Id is invalid
        :return:
        """
        with self.client:
            response = self.client.post(
                '/bucketlists/id/items',
                data=json.dumps(dict(name='Food')),
                content_type='application/json',
                headers=dict(Authorization='Bearer ' + self.get_user_token())
            )
            print(response.data)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Provide a valid Bucket Id')
            self.assertEqual(response.status_code, 401)

    def test_name_attribute_is_missing_in_request(self):
        with self.client:
            response = self.client.post(
                '/bucketlists/1/items',
                data=json.dumps(dict(description='')),
                content_type='application/json',
                headers=dict(Authorization='Bearer ' + self.get_user_token())
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'No name or value attribute found')
            self.assertEqual(response.status_code, 401)

    def test_name_attribute_has_no_value_in_request(self):
        with self.client:
            response = self.client.post(
                '/bucketlists/1/items',
                data=json.dumps(dict(name='')),
                content_type='application/json',
                headers=dict(Authorization='Bearer ' + self.get_user_token())
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'No name or value attribute found')
            self.assertEqual(response.status_code, 401)

    def test_correct_response_when_user_has_no_bucket_with_specified_id(self):
        """
        Test that a user does not have a Bucket specified by that Id
        :return:
        """
        with self.client:
            response = self.client.post(
                '/bucketlists/1/items',
                data=json.dumps(dict(name='food')),
                content_type='application/json',
                headers=dict(Authorization='Bearer ' + self.get_user_token())
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'User has no Bucket with Id 1')
            self.assertEqual(response.status_code, 202)

    def test_an_item_has_been_successfully_saved(self):
        """
        Test a Bucket Item has been successfully stored.
        :return:
        """
        with self.client:
            token = self.get_user_token()
            self.create_bucket(token)
            response = self.client.post(
                '/bucketlists/1/items',
                data=json.dumps(dict(name='food', description='Enjoying the good life')),
                content_type='application/json',
                headers=dict(Authorization='Bearer ' + token)
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertEqual(data['item']['id'], 1)
            self.assertTrue(data['item']['name'] == 'food')
            self.assertTrue(data['item']['description'] == 'Enjoying the good life')
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()

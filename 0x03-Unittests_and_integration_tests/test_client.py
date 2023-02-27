#!/usr/bin/env python3
"""
Testing client.py
"""
import unittest
from unittest.mock import patch, MagicMock, PropertyMock
from parameterized import parameterized, parameterized_class
requests = __import__("utils").requests
GithubOrgClient = __import__("client").GithubOrgClient
# get_json = __import__("utils").get_json
utils = __import__("utils")
TEST_PAYLOAD = __import__("fixtures").TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """
    Testing GithubOrgClient
    """

    @parameterized.expand([
        ('google'),
        ('abc')
    ])
    @patch('requests.get')
    def test_org(self, org_name, mock_get_json):
        """
        Testing GithubOrgClient
        """
        instance = GithubOrgClient(org_name)
        # Mocking the response object
        mock_response = MagicMock()
        mock_response.json.return_value = {"payload": True}

        # Assigning the mocked response object to the mocked
        # request.get object
        mock_get_json.return_value = mock_response

        doc = instance.org
        doc = instance.org

        # Since the org method is decorated by @memoize
        # the get_json function should only be executed once,
        # hence the mocked get function is executed only once
        mock_get_json.assert_called_once()
        self.assertEqual(doc, {"payload": True})

    def test_public_repos_url(self):
        """
        Test GithubOrgClient._public_repos_url
        """
        instance = GithubOrgClient('google')
        # Mocking the org method of GithubOrgClient, it is
        # considered a propoerty because the @memoize decorator
        # turns it into a property
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as org_mock:
            org_mock.return_value = {"repos_url": True}

            # The _public_repos_url method returns the value
            # associated with the key "repos_url"
            value = instance._public_repos_url
            self.assertEqual(value, True)

    # @patch('utils.get_json')
    # def test_public_repos(self, get_json_mock):
    #     """
    #     Test GithubOrgClient.public_repos
    #     """
    #     instance = GithubOrgClient('google')
    #     with patch('client.GithubOrgClient._public_repos_url',
    #                 new_callable=PropertyMock) as _public_repos_url_mock:
    #         _public_repos_url_mock.return_value = "http://hi"
    #         mock_response = MagicMock()
    #         mock_response.json.return_value = {"name": "apps"}
    #         get_json_mock.return_value = mock_response
    #         result = instance.public_repos()
    #         self.assertEqual(result, ["apps"])
    #         _public_repos_url_mock.assert_called_once()
    #         get_json_mock.assert_called_once()

    # @patch('utils.get_json')
    # def test_public_repos(self, get_json_mock):
    #     """
    #     Test GithubOrgClient.public_repos
    #     """
    #     # instance = GithubOrgClient('google')
    #     # mock_response = MagicMock()
    #     # mock_response.return_value = 1
    #     get_json_mock.return_value = 1
    #     self.assertEqual(utils.get_json('http://google.com'), 1)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        Testing GithubOrgClient.has_license
        """
        instance = GithubOrgClient('google')
        license_exists = instance.has_license(repo, license_key)
        self.assertEqual(license_exists, expected)

# ---------------------------------------------------------------
# Integration Testing (Task 8)


@parameterized_class(('org_payload', 'repos_payload',
                      'expected_repos', 'apache2_repos'), [
    (TEST_PAYLOAD[0][0], TEST_PAYLOAD[0][1],
     TEST_PAYLOAD[0][2], TEST_PAYLOAD[0][3]),
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.get_patcher = patch('requests.get')
        mock_get = cls.get_patcher.start()
        mock_get.side_effect = [cls.org_payload, cls.repos_payload,
                                cls.expected_repos, cls.apache2_repos]

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()

    # def test_get(self):
    #     self.assertEqual(requests.get("hello"),
    #     {'repos_url': 'https://api.github.com/orgs/google/repos'})

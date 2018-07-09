# coding: utf-8

"""
    

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import os
import sys
import unittest

import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from deploy_sdk_client.apis.solution_catalog_api import SolutionCatalogApi


class TestSolutionCatalogApi(unittest.TestCase):
    """ SolutionCatalogApi unit test stubs """

    def setUp(self):
        self.api = deploy_sdk_client.apis.solution_catalog_api.SolutionCatalogApi()

    def tearDown(self):
        pass

    def test_get_all_resources(self):
        """
        Test case for get_all_resources

        Get all available catalogs
        """
        pass

    def test_get_all_solution_catalogs(self):
        """
        Test case for get_all_solution_catalogs

        Gets Solution Catalog details for given UserId ID
        """
        pass

    def test_get_solution_catalog_by_id(self):
        """
        Test case for get_solution_catalog_by_id

        Gets Solution Catalog details for given UserId ID
        """
        pass

    def test_get_solution_catalog_by_name(self):
        """
        Test case for get_solution_catalog_by_name

        Gets Solution Catalog details for given UserId ID
        """
        pass

    def test_prepare_import_blueprint(self):
        """
        Test case for prepare_import_blueprint

        Delpoy the blueprint which is specied in ID.
        """
        pass

    def test_prepare_import_blueprint_0(self):
        """
        Test case for prepare_import_blueprint_0

        Used before Solution import.
        """
        pass


if __name__ == '__main__':
    unittest.main()

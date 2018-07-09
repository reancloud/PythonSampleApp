# deploy_sdk_client.SolutionCatalogApi

All URIs are relative to *https://localhost/api/reandeploy/DeployNow/rest*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_all_resources**](SolutionCatalogApi.md#get_all_resources) | **GET** /solutioncatalog/json | Get all available catalogs
[**get_all_solution_catalogs**](SolutionCatalogApi.md#get_all_solution_catalogs) | **GET** /solutioncatalog | Gets Solution Catalog details for given UserId ID
[**get_solution_catalog_by_id**](SolutionCatalogApi.md#get_solution_catalog_by_id) | **GET** /solutioncatalog/id/{catalogId} | Gets Solution Catalog details for given UserId ID
[**get_solution_catalog_by_name**](SolutionCatalogApi.md#get_solution_catalog_by_name) | **GET** /solutioncatalog/name/{catalogName} | Gets Solution Catalog details for given UserId ID
[**prepare_import_blueprint**](SolutionCatalogApi.md#prepare_import_blueprint) | **POST** /solutioncatalog/deploy/{blueprintId} | Delpoy the blueprint which is specied in ID.
[**prepare_import_blueprint_0**](SolutionCatalogApi.md#prepare_import_blueprint_0) | **POST** /solutioncatalog/import | Used before Solution import.


# **get_all_resources**
> get_all_resources()

Get all available catalogs



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.SolutionCatalogApi()

try: 
    # Get all available catalogs
    api_instance.get_all_resources()
except ApiException as e:
    print("Exception when calling SolutionCatalogApi->get_all_resources: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_solution_catalogs**
> get_all_solution_catalogs(user_id)

Gets Solution Catalog details for given UserId ID

Response will be same as Solution

### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.SolutionCatalogApi()
user_id = 789 # int | 

try: 
    # Gets Solution Catalog details for given UserId ID
    api_instance.get_all_solution_catalogs(user_id)
except ApiException as e:
    print("Exception when calling SolutionCatalogApi->get_all_solution_catalogs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **int**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_solution_catalog_by_id**
> get_solution_catalog_by_id(catalog_id)

Gets Solution Catalog details for given UserId ID

Response will be same as Solution

### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.SolutionCatalogApi()
catalog_id = 789 # int | 

try: 
    # Gets Solution Catalog details for given UserId ID
    api_instance.get_solution_catalog_by_id(catalog_id)
except ApiException as e:
    print("Exception when calling SolutionCatalogApi->get_solution_catalog_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **catalog_id** | **int**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_solution_catalog_by_name**
> get_solution_catalog_by_name(catalog_name)

Gets Solution Catalog details for given UserId ID

Response will be same as Solution

### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.SolutionCatalogApi()
catalog_name = 'catalog_name_example' # str | 

try: 
    # Gets Solution Catalog details for given UserId ID
    api_instance.get_solution_catalog_by_name(catalog_name)
except ApiException as e:
    print("Exception when calling SolutionCatalogApi->get_solution_catalog_by_name: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **catalog_name** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **prepare_import_blueprint**
> prepare_import_blueprint(blueprint_id)

Delpoy the blueprint which is specied in ID.

The blueprint ID is sent which is need to be deployed along with all its environment

### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.SolutionCatalogApi()
blueprint_id = 789 # int | 

try: 
    # Delpoy the blueprint which is specied in ID.
    api_instance.prepare_import_blueprint(blueprint_id)
except ApiException as e:
    print("Exception when calling SolutionCatalogApi->prepare_import_blueprint: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **blueprint_id** | **int**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **prepare_import_blueprint_0**
> prepare_import_blueprint_0(body=body)

Used before Solution import.

Given a blueprint file, it returns response to set typical environment create params to send it to blueprint import API

### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.SolutionCatalogApi()
body = deploy_sdk_client.MultipleBlueprintImport() # MultipleBlueprintImport |  (optional)

try: 
    # Used before Solution import.
    api_instance.prepare_import_blueprint_0(body=body)
except ApiException as e:
    print("Exception when calling SolutionCatalogApi->prepare_import_blueprint_0: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**MultipleBlueprintImport**](MultipleBlueprintImport.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


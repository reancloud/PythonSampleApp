# deploy_sdk_client.ResourceApi

All URIs are relative to *https://localhost/api/reandeploy/DeployNow/rest*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_all_data_resources**](ResourceApi.md#get_all_data_resources) | **GET** /resource/datasources | Get all available resources
[**get_all_resources**](ResourceApi.md#get_all_resources) | **GET** /resource | Get all available resources


# **get_all_data_resources**
> get_all_data_resources()

Get all available resources



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.ResourceApi()

try: 
    # Get all available resources
    api_instance.get_all_data_resources()
except ApiException as e:
    print("Exception when calling ResourceApi->get_all_data_resources: %s\n" % e)
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

# **get_all_resources**
> get_all_resources()

Get all available resources



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.ResourceApi()

try: 
    # Get all available resources
    api_instance.get_all_resources()
except ApiException as e:
    print("Exception when calling ResourceApi->get_all_resources: %s\n" % e)
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


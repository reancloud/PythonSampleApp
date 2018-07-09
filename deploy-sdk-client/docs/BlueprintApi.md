# deploy_sdk_client.BlueprintApi

All URIs are relative to *https://localhost/api/reandeploy/DeployNow/rest*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_all_resources**](BlueprintApi.md#get_all_resources) | **GET** /blueprint | Returns the list of all the available blueprints
[**get_read_me_file**](BlueprintApi.md#get_read_me_file) | **GET** /blueprint/readme/{readMe} | Get the readme file content of blueprint
[**import_blueprint**](BlueprintApi.md#import_blueprint) | **POST** /blueprint/import | Import blurprint in REAN Deploy
[**import_blueprint_file**](BlueprintApi.md#import_blueprint_file) | **GET** /blueprint/{file} | Returns blueprint file.
[**prepare_import_blueprint**](BlueprintApi.md#prepare_import_blueprint) | **POST** /blueprint/import/prepare | Prepare blueprint before importing it


# **get_all_resources**
> get_all_resources()

Returns the list of all the available blueprints



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.BlueprintApi()

try: 
    # Returns the list of all the available blueprints
    api_instance.get_all_resources()
except ApiException as e:
    print("Exception when calling BlueprintApi->get_all_resources: %s\n" % e)
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

# **get_read_me_file**
> str get_read_me_file(read_me)

Get the readme file content of blueprint



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.BlueprintApi()
read_me = 'read_me_example' # str | Name of Blueprint's README file

try: 
    # Get the readme file content of blueprint
    api_response = api_instance.get_read_me_file(read_me)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BlueprintApi->get_read_me_file: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **read_me** | **str**| Name of Blueprint&#39;s README file | 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: text/plain

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **import_blueprint**
> import_blueprint(body=body)

Import blurprint in REAN Deploy

This API is only been used after prepareImportBlueprint API. Set required params from prepare and use import/blueprint.Response will be map of keys [id and environments], in which id refers to last environment in chain.

### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.BlueprintApi()
body = deploy_sdk_client.BlueprintImport() # BlueprintImport |  (optional)

try: 
    # Import blurprint in REAN Deploy
    api_instance.import_blueprint(body=body)
except ApiException as e:
    print("Exception when calling BlueprintApi->import_blueprint: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**BlueprintImport**](BlueprintImport.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **import_blueprint_file**
> str import_blueprint_file(file)

Returns blueprint file.



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.BlueprintApi()
file = 'file_example' # str | Name of the Blueprint

try: 
    # Returns blueprint file.
    api_response = api_instance.import_blueprint_file(file)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BlueprintApi->import_blueprint_file: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file** | **str**| Name of the Blueprint | 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **prepare_import_blueprint**
> BlueprintImport prepare_import_blueprint(body=body)

Prepare blueprint before importing it



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.BlueprintApi()
body = deploy_sdk_client.JsonNode() # JsonNode |  (optional)

try: 
    # Prepare blueprint before importing it
    api_response = api_instance.prepare_import_blueprint(body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BlueprintApi->prepare_import_blueprint: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**JsonNode**](JsonNode.md)|  | [optional] 

### Return type

[**BlueprintImport**](BlueprintImport.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


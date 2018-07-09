# deploy_sdk_client.ChefServerApi

All URIs are relative to *https://localhost/api/reandeploy/DeployNow/rest*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete**](ChefServerApi.md#delete) | **DELETE** /chefserver/{id} | 
[**exists**](ChefServerApi.md#exists) | **GET** /chefserver/{name}/exists | 
[**get**](ChefServerApi.md#get) | **GET** /chefserver/{id} | 
[**get_all**](ChefServerApi.md#get_all) | **GET** /chefserver | 
[**list_environments**](ChefServerApi.md#list_environments) | **GET** /chefserver/{id}/environment | 
[**list_packages**](ChefServerApi.md#list_packages) | **GET** /chefserver/{id}/package | 
[**save**](ChefServerApi.md#save) | **POST** /chefserver | 
[**update**](ChefServerApi.md#update) | **PUT** /chefserver/{id} | 


# **delete**
> ChefServer delete(id)



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.ChefServerApi()
id = 789 # int | 

try: 
    api_response = api_instance.delete(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ChefServerApi->delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 

### Return type

[**ChefServer**](ChefServer.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **exists**
> bool exists(name)



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.ChefServerApi()
name = 'name_example' # str | 

try: 
    api_response = api_instance.exists(name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ChefServerApi->exists: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**|  | 

### Return type

**bool**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get**
> ChefServer get(id)



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.ChefServerApi()
id = 789 # int | 

try: 
    api_response = api_instance.get(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ChefServerApi->get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 

### Return type

[**ChefServer**](ChefServer.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all**
> list[ChefServer] get_all()



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.ChefServerApi()

try: 
    api_response = api_instance.get_all()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ChefServerApi->get_all: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[ChefServer]**](ChefServer.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_environments**
> list[str] list_environments(id)



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.ChefServerApi()
id = 789 # int | 

try: 
    api_response = api_instance.list_environments(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ChefServerApi->list_environments: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 

### Return type

**list[str]**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_packages**
> list[Package] list_packages(id)



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.ChefServerApi()
id = 789 # int | 

try: 
    api_response = api_instance.list_packages(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ChefServerApi->list_packages: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 

### Return type

[**list[Package]**](Package.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **save**
> ChefServer save(body=body)



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.ChefServerApi()
body = deploy_sdk_client.ChefServer() # ChefServer |  (optional)

try: 
    api_response = api_instance.save(body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ChefServerApi->save: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ChefServer**](ChefServer.md)|  | [optional] 

### Return type

[**ChefServer**](ChefServer.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update**
> ChefServer update(id, body=body)



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.ChefServerApi()
id = 789 # int | 
body = deploy_sdk_client.ChefServer() # ChefServer |  (optional)

try: 
    api_response = api_instance.update(id, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ChefServerApi->update: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 
 **body** | [**ChefServer**](ChefServer.md)|  | [optional] 

### Return type

[**ChefServer**](ChefServer.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


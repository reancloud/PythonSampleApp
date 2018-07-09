# deploy_sdk_client.CustomTagApi

All URIs are relative to *https://localhost/api/reandeploy/DeployNow/rest*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_custom_tag**](CustomTagApi.md#delete_custom_tag) | **DELETE** /customTag/{customTagId} | Delete a customTag by id
[**get_all_custom_tags**](CustomTagApi.md#get_all_custom_tags) | **GET** /customTag | Get all available Custom Tags
[**get_custom_tag**](CustomTagApi.md#get_custom_tag) | **GET** /customTag/{customTagId} | Get a Custom Tag by Id
[**get_custom_tag_by_name**](CustomTagApi.md#get_custom_tag_by_name) | **GET** /customTag/name/{customTagName} | Get a Custom Tag by name
[**get_custom_tags_by_user**](CustomTagApi.md#get_custom_tags_by_user) | **GET** /customTag/user | Get all Custom Tags by User
[**save_custom_tag**](CustomTagApi.md#save_custom_tag) | **POST** /customTag | Create a CustomTag
[**update_custom_tag**](CustomTagApi.md#update_custom_tag) | **PUT** /customTag | update a CustomTag


# **delete_custom_tag**
> delete_custom_tag(custom_tag_id)

Delete a customTag by id



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.CustomTagApi()
custom_tag_id = 789 # int | 

try: 
    # Delete a customTag by id
    api_instance.delete_custom_tag(custom_tag_id)
except ApiException as e:
    print("Exception when calling CustomTagApi->delete_custom_tag: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **custom_tag_id** | **int**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_custom_tags**
> list[CustomTag] get_all_custom_tags()

Get all available Custom Tags



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.CustomTagApi()

try: 
    # Get all available Custom Tags
    api_response = api_instance.get_all_custom_tags()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CustomTagApi->get_all_custom_tags: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[CustomTag]**](CustomTag.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_custom_tag**
> CustomTag get_custom_tag(custom_tag_id)

Get a Custom Tag by Id



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.CustomTagApi()
custom_tag_id = 789 # int | 

try: 
    # Get a Custom Tag by Id
    api_response = api_instance.get_custom_tag(custom_tag_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CustomTagApi->get_custom_tag: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **custom_tag_id** | **int**|  | 

### Return type

[**CustomTag**](CustomTag.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_custom_tag_by_name**
> CustomTag get_custom_tag_by_name(custom_tag_name)

Get a Custom Tag by name



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.CustomTagApi()
custom_tag_name = 'custom_tag_name_example' # str | 

try: 
    # Get a Custom Tag by name
    api_response = api_instance.get_custom_tag_by_name(custom_tag_name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CustomTagApi->get_custom_tag_by_name: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **custom_tag_name** | **str**|  | 

### Return type

[**CustomTag**](CustomTag.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_custom_tags_by_user**
> list[CustomTag] get_custom_tags_by_user()

Get all Custom Tags by User



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.CustomTagApi()

try: 
    # Get all Custom Tags by User
    api_response = api_instance.get_custom_tags_by_user()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CustomTagApi->get_custom_tags_by_user: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[CustomTag]**](CustomTag.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **save_custom_tag**
> CustomTag save_custom_tag(body=body)

Create a CustomTag



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.CustomTagApi()
body = deploy_sdk_client.CustomTag() # CustomTag |  (optional)

try: 
    # Create a CustomTag
    api_response = api_instance.save_custom_tag(body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CustomTagApi->save_custom_tag: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CustomTag**](CustomTag.md)|  | [optional] 

### Return type

[**CustomTag**](CustomTag.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_custom_tag**
> CustomTag update_custom_tag(body=body)

update a CustomTag



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.CustomTagApi()
body = deploy_sdk_client.CustomTag() # CustomTag |  (optional)

try: 
    # update a CustomTag
    api_response = api_instance.update_custom_tag(body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CustomTagApi->update_custom_tag: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CustomTag**](CustomTag.md)|  | [optional] 

### Return type

[**CustomTag**](CustomTag.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


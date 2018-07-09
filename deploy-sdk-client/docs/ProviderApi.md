# deploy_sdk_client.ProviderApi

All URIs are relative to *https://localhost/api/reandeploy/DeployNow/rest*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_provider**](ProviderApi.md#delete_provider) | **DELETE** /provider/{provId} | Delete Provider by id
[**get_all_providers**](ProviderApi.md#get_all_providers) | **GET** /provider | Get allProviders for user
[**get_aws_regions**](ProviderApi.md#get_aws_regions) | **GET** /provider/awsRegions | Get all available AWS regions
[**get_provider**](ProviderApi.md#get_provider) | **GET** /provider/{provId} | Get provider by Provider id
[**get_provider_by_name**](ProviderApi.md#get_provider_by_name) | **GET** /provider/name/{provName} | Get Provider by provider name
[**save_provider**](ProviderApi.md#save_provider) | **POST** /provider | Create Provider for User
[**save_provider_with_permissions**](ProviderApi.md#save_provider_with_permissions) | **POST** /provider/validateandsave | Validate and Save AWS Provider
[**update_provider**](ProviderApi.md#update_provider) | **PUT** /provider | Update existing Provider


# **delete_provider**
> delete_provider(prov_id)

Delete Provider by id



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.ProviderApi()
prov_id = 789 # int | 

try: 
    # Delete Provider by id
    api_instance.delete_provider(prov_id)
except ApiException as e:
    print("Exception when calling ProviderApi->delete_provider: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **prov_id** | **int**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_providers**
> list[Provider] get_all_providers()

Get allProviders for user



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.ProviderApi()

try: 
    # Get allProviders for user
    api_response = api_instance.get_all_providers()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProviderApi->get_all_providers: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[Provider]**](Provider.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_aws_regions**
> list[str] get_aws_regions()

Get all available AWS regions



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.ProviderApi()

try: 
    # Get all available AWS regions
    api_response = api_instance.get_aws_regions()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProviderApi->get_aws_regions: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**list[str]**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_provider**
> get_provider(prov_id)

Get provider by Provider id



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.ProviderApi()
prov_id = 789 # int | 

try: 
    # Get provider by Provider id
    api_instance.get_provider(prov_id)
except ApiException as e:
    print("Exception when calling ProviderApi->get_provider: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **prov_id** | **int**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_provider_by_name**
> get_provider_by_name(prov_name)

Get Provider by provider name



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.ProviderApi()
prov_name = 'prov_name_example' # str | 

try: 
    # Get Provider by provider name
    api_instance.get_provider_by_name(prov_name)
except ApiException as e:
    print("Exception when calling ProviderApi->get_provider_by_name: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **prov_name** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **save_provider**
> save_provider(provider)

Create Provider for User



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.ProviderApi()
provider = deploy_sdk_client.SaveProvider() # SaveProvider | 

try: 
    # Create Provider for User
    api_instance.save_provider(provider)
except ApiException as e:
    print("Exception when calling ProviderApi->save_provider: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **provider** | [**SaveProvider**](SaveProvider.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **save_provider_with_permissions**
> save_provider_with_permissions(provider)

Validate and Save AWS Provider

API verifies the aws provider credentials before saving it

### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.ProviderApi()
provider = deploy_sdk_client.SaveProvider() # SaveProvider | 

try: 
    # Validate and Save AWS Provider
    api_instance.save_provider_with_permissions(provider)
except ApiException as e:
    print("Exception when calling ProviderApi->save_provider_with_permissions: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **provider** | [**SaveProvider**](SaveProvider.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_provider**
> update_provider(provider)

Update existing Provider



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.ProviderApi()
provider = deploy_sdk_client.SaveProvider() # SaveProvider | 

try: 
    # Update existing Provider
    api_instance.update_provider(provider)
except ApiException as e:
    print("Exception when calling ProviderApi->update_provider: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **provider** | [**SaveProvider**](SaveProvider.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


# deploy_sdk_client.ConnectionApi

All URIs are relative to *https://localhost/api/reandeploy/DeployNow/rest*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_vm_connection**](ConnectionApi.md#delete_vm_connection) | **DELETE** /conn/{conId} | Delete Connection using connection Id
[**get_all_vm_connections**](ConnectionApi.md#get_all_vm_connections) | **GET** /conn | Get all Connections of an User
[**get_vm_connection**](ConnectionApi.md#get_vm_connection) | **GET** /conn/{conId} | Get Connection of current loggedIn user by connection id
[**is_connection_exists**](ConnectionApi.md#is_connection_exists) | **GET** /conn/connection/{name}/exists | Verify if Connection with name exists
[**save_vm_connection**](ConnectionApi.md#save_vm_connection) | **POST** /conn | Create Connection
[**update_vm_connection**](ConnectionApi.md#update_vm_connection) | **PUT** /conn | Update existing Connection


# **delete_vm_connection**
> VmConnection delete_vm_connection(con_id)

Delete Connection using connection Id



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.ConnectionApi()
con_id = 789 # int | connection Id

try: 
    # Delete Connection using connection Id
    api_response = api_instance.delete_vm_connection(con_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConnectionApi->delete_vm_connection: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **con_id** | **int**| connection Id | 

### Return type

[**VmConnection**](VmConnection.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_vm_connections**
> VmConnection get_all_vm_connections()

Get all Connections of an User



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.ConnectionApi()

try: 
    # Get all Connections of an User
    api_response = api_instance.get_all_vm_connections()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConnectionApi->get_all_vm_connections: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**VmConnection**](VmConnection.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_vm_connection**
> VmConnection get_vm_connection(con_id)

Get Connection of current loggedIn user by connection id



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.ConnectionApi()
con_id = 789 # int | connection ID

try: 
    # Get Connection of current loggedIn user by connection id
    api_response = api_instance.get_vm_connection(con_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConnectionApi->get_vm_connection: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **con_id** | **int**| connection ID | 

### Return type

[**VmConnection**](VmConnection.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **is_connection_exists**
> str is_connection_exists(name)

Verify if Connection with name exists



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.ConnectionApi()
name = 'name_example' # str | connection name to check

try: 
    # Verify if Connection with name exists
    api_response = api_instance.is_connection_exists(name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConnectionApi->is_connection_exists: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| connection name to check | 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **save_vm_connection**
> VmConnection save_vm_connection(connection)

Create Connection



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.ConnectionApi()
connection = deploy_sdk_client.VmConnection() # VmConnection | 

try: 
    # Create Connection
    api_response = api_instance.save_vm_connection(connection)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConnectionApi->save_vm_connection: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connection** | [**VmConnection**](VmConnection.md)|  | 

### Return type

[**VmConnection**](VmConnection.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_vm_connection**
> VmConnection update_vm_connection(connection)

Update existing Connection



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.ConnectionApi()
connection = deploy_sdk_client.VmConnection() # VmConnection | 

try: 
    # Update existing Connection
    api_response = api_instance.update_vm_connection(connection)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConnectionApi->update_vm_connection: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connection** | [**VmConnection**](VmConnection.md)|  | 

### Return type

[**VmConnection**](VmConnection.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


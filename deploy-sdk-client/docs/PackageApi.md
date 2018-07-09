# deploy_sdk_client.PackageApi

All URIs are relative to *https://localhost/api/reandeploy/DeployNow/rest*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_ansible_package**](PackageApi.md#add_ansible_package) | **POST** /package/upload | Create an ansible package by uploading zip folder
[**add_package**](PackageApi.md#add_package) | **POST** /package | Create a package
[**create_new_version**](PackageApi.md#create_new_version) | **POST** /package/newVersion | Create a new Version
[**delete_package**](PackageApi.md#delete_package) | **DELETE** /package/{packageId} | Delete a package by id
[**get_all_packages**](PackageApi.md#get_all_packages) | **GET** /package | Get all available packages
[**get_all_unique_package**](PackageApi.md#get_all_unique_package) | **GET** /package/unique | Get all packages with unique names
[**get_default_package_type**](PackageApi.md#get_default_package_type) | **GET** /package/defaultPackageType | Returns the only package type can be used on particular server.
[**get_package**](PackageApi.md#get_package) | **GET** /package/{packageId} | Get a package by id
[**get_package_templates**](PackageApi.md#get_package_templates) | **GET** /package/templates | Package JSON Template with sample values which can be used to create/modify packages
[**get_packages**](PackageApi.md#get_packages) | **GET** /package/{packageName}/{packageType} | Get all packages by name and type
[**get_shared_package_policy**](PackageApi.md#get_shared_package_policy) | **GET** /package/{packageId}/share | Get shared package policy
[**share_package**](PackageApi.md#share_package) | **POST** /package/share | Change Package sharing policy
[**update_packages**](PackageApi.md#update_packages) | **POST** /package/update | Updates all packages form central packages repository
[**update_packages_0**](PackageApi.md#update_packages_0) | **PUT** /package | Updates a package


# **add_ansible_package**
> add_ansible_package(file=file)

Create an ansible package by uploading zip folder



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.PackageApi()
file = '/path/to/file.txt' # file |  (optional)

try: 
    # Create an ansible package by uploading zip folder
    api_instance.add_ansible_package(file=file)
except ApiException as e:
    print("Exception when calling PackageApi->add_ansible_package: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file** | **file**|  | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **add_package**
> add_package(body=body)

Create a package



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.PackageApi()
body = deploy_sdk_client.Package() # Package |  (optional)

try: 
    # Create a package
    api_instance.add_package(body=body)
except ApiException as e:
    print("Exception when calling PackageApi->add_package: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Package**](Package.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_new_version**
> create_new_version(body=body)

Create a new Version



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.PackageApi()
body = deploy_sdk_client.NewPackageVersionDto() # NewPackageVersionDto |  (optional)

try: 
    # Create a new Version
    api_instance.create_new_version(body=body)
except ApiException as e:
    print("Exception when calling PackageApi->create_new_version: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**NewPackageVersionDto**](NewPackageVersionDto.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_package**
> delete_package(package_id)

Delete a package by id



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.PackageApi()
package_id = 789 # int | 

try: 
    # Delete a package by id
    api_instance.delete_package(package_id)
except ApiException as e:
    print("Exception when calling PackageApi->delete_package: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **package_id** | **int**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_packages**
> get_all_packages()

Get all available packages



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.PackageApi()

try: 
    # Get all available packages
    api_instance.get_all_packages()
except ApiException as e:
    print("Exception when calling PackageApi->get_all_packages: %s\n" % e)
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

# **get_all_unique_package**
> get_all_unique_package()

Get all packages with unique names



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.PackageApi()

try: 
    # Get all packages with unique names
    api_instance.get_all_unique_package()
except ApiException as e:
    print("Exception when calling PackageApi->get_all_unique_package: %s\n" % e)
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

# **get_default_package_type**
> str get_default_package_type()

Returns the only package type can be used on particular server.



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.PackageApi()

try: 
    # Returns the only package type can be used on particular server.
    api_response = api_instance.get_default_package_type()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PackageApi->get_default_package_type: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_package**
> Package get_package(package_id)

Get a package by id



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.PackageApi()
package_id = 789 # int | 

try: 
    # Get a package by id
    api_response = api_instance.get_package(package_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PackageApi->get_package: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **package_id** | **int**|  | 

### Return type

[**Package**](Package.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_package_templates**
> get_package_templates()

Package JSON Template with sample values which can be used to create/modify packages



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.PackageApi()

try: 
    # Package JSON Template with sample values which can be used to create/modify packages
    api_instance.get_package_templates()
except ApiException as e:
    print("Exception when calling PackageApi->get_package_templates: %s\n" % e)
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

# **get_packages**
> list[Package] get_packages(package_name, package_type)

Get all packages by name and type



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.PackageApi()
package_name = 'package_name_example' # str | 
package_type = 'package_type_example' # str | 

try: 
    # Get all packages by name and type
    api_response = api_instance.get_packages(package_name, package_type)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PackageApi->get_packages: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **package_name** | **str**|  | 
 **package_type** | **str**|  | 

### Return type

[**list[Package]**](Package.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_shared_package_policy**
> SharePolicy get_shared_package_policy(package_id)

Get shared package policy



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.PackageApi()
package_id = 789 # int | 

try: 
    # Get shared package policy
    api_response = api_instance.get_shared_package_policy(package_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PackageApi->get_shared_package_policy: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **package_id** | **int**|  | 

### Return type

[**SharePolicy**](SharePolicy.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **share_package**
> share_package(body=body)

Change Package sharing policy



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.PackageApi()
body = deploy_sdk_client.MultiSharePolicy() # MultiSharePolicy |  (optional)

try: 
    # Change Package sharing policy
    api_instance.share_package(body=body)
except ApiException as e:
    print("Exception when calling PackageApi->share_package: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**MultiSharePolicy**](MultiSharePolicy.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_packages**
> update_packages()

Updates all packages form central packages repository



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.PackageApi()

try: 
    # Updates all packages form central packages repository
    api_instance.update_packages()
except ApiException as e:
    print("Exception when calling PackageApi->update_packages: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_packages_0**
> update_packages_0(body=body)

Updates a package



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.PackageApi()
body = deploy_sdk_client.Package() # Package |  (optional)

try: 
    # Updates a package
    api_instance.update_packages_0(body=body)
except ApiException as e:
    print("Exception when calling PackageApi->update_packages_0: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Package**](Package.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


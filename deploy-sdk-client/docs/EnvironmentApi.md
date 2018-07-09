# deploy_sdk_client.EnvironmentApi

All URIs are relative to *https://localhost/api/reandeploy/DeployNow/rest*

Method | HTTP request | Description
------------- | ------------- | -------------
[**check_environment_import_for_name_and_version**](EnvironmentApi.md#check_environment_import_for_name_and_version) | **POST** /env/checkIfEnvironmentNamesAndVersionExists | Check if Environment Names And Version is already Exists
[**check_if_environment_exists**](EnvironmentApi.md#check_if_environment_exists) | **GET** /env/exists/{envName} | Check if environment with specified name is already created by the user
[**confirm_destroy_env_by_token**](EnvironmentApi.md#confirm_destroy_env_by_token) | **GET** /env/destroy/once/{token} | Destroy deployment using destroy token
[**copy_and_deploy**](EnvironmentApi.md#copy_and_deploy) | **POST** /env/copyanddeploy | Create a copy of an environment and deploy
[**copy_environment**](EnvironmentApi.md#copy_environment) | **POST** /env/copy | Copy an environment using configuration like tags and input variables
[**create_empty_env_resource**](EnvironmentApi.md#create_empty_env_resource) | **POST** /env/resource/{envId}/{name}/{resourceName} | Creates a new resource with given name and resourceName and gives resource template to set applicable attribute values
[**create_new_env_package**](EnvironmentApi.md#create_new_env_package) | **POST** /env/resource/package/{resourceId}/{packageName} | Create package on the resource and gives package template to set values for required attributes
[**create_new_env_resource**](EnvironmentApi.md#create_new_env_resource) | **POST** /env/{envId}/resource | Creates a new resource with given name and resourceName and positionX and positionY and gives resource template to set applicable attribute values
[**create_new_env_resource_using_import**](EnvironmentApi.md#create_new_env_resource_using_import) | **POST** /env/{envId}/resource/import | Creates a new resource with given name, resourceName, positonX, positionY, and existingId and gives resource template to set applicable attribute values
[**delete_environment**](EnvironmentApi.md#delete_environment) | **DELETE** /env/{envId} | Deletes environment by id
[**delete_package**](EnvironmentApi.md#delete_package) | **DELETE** /env/resource/package/{packageId} | delete package by id
[**delete_resource**](EnvironmentApi.md#delete_resource) | **DELETE** /env/resource/{resourceId} | Delete resource by id
[**deploy_as_blueprint**](EnvironmentApi.md#deploy_as_blueprint) | **POST** /env/deploy/blueprint/{envId} | Deploy an environment by id
[**deploy_by_config**](EnvironmentApi.md#deploy_by_config) | **POST** /env/deploy_by_env_id_and_dep_name | Deploy/Redeploys an environment by environment id with deployment name and other deployment configurations
[**deploy_by_env_id**](EnvironmentApi.md#deploy_by_env_id) | **POST** /env/deploy/deployment/{envId} | Deploy an environment by environment id with deploy configuration
[**deploy_by_env_id_and_config**](EnvironmentApi.md#deploy_by_env_id_and_config) | **POST** /env/deploy/{envId} | Deploy an environment by environment id
[**deploy_by_env_name_version_and_config**](EnvironmentApi.md#deploy_by_env_name_version_and_config) | **POST** /env/deploy/deployment/{envName}/{envVersion} | Deploy an environment by name and version
[**destroy**](EnvironmentApi.md#destroy) | **DELETE** /env/deploy/{envId} | Destroys environment deployment from REAN Deploy and Actually erases your infracture on provider
[**destroy_deployment_by_env_name_and_deployment_name**](EnvironmentApi.md#destroy_deployment_by_env_name_and_deployment_name) | **DELETE** /env/deploy/deployment/{envName}/{deploymentName} | Destroys environment deployment. Actually erases your infracture on provider
[**destroy_deployment_by_id**](EnvironmentApi.md#destroy_deployment_by_id) | **DELETE** /env/deploy/deployment/{deploymentId} | Destroys environment deployment. Actually erases your infracture on provider
[**destroy_deployment_by_id_and_deployment_name**](EnvironmentApi.md#destroy_deployment_by_id_and_deployment_name) | **DELETE** /env/deploy/deployment/{envId}/{deploymentName} | Destroys environment deployment. Actually erases your infracture on provider
[**destroy_env_by_token**](EnvironmentApi.md#destroy_env_by_token) | **DELETE** /env/destroy/once/{token} | One-time destroy of an an environment by a non-user using token
[**download_terraform_files**](EnvironmentApi.md#download_terraform_files) | **GET** /env/download/terraform/{envId} | Gives zip stream of all terraform files for an environment
[**export_blueprint_environment**](EnvironmentApi.md#export_blueprint_environment) | **GET** /env/export/blueprint/{envId} | Export Environment with all Parent environment which can be imported into another REAN Deploy Server
[**export_environment**](EnvironmentApi.md#export_environment) | **GET** /env/export/{envId} | Export Environment into JSON format
[**get_actions**](EnvironmentApi.md#get_actions) | **GET** /env/actions/{resourceType} | Get all supported Resource type
[**get_all_deployments_for_environment**](EnvironmentApi.md#get_all_deployments_for_environment) | **GET** /env/get-deployment/{envName} | Get all the deplyments of enviroment which are owned by loggedIn User
[**get_all_deployments_for_environment_across_versions**](EnvironmentApi.md#get_all_deployments_for_environment_across_versions) | **GET** /env/get-deployments-across-versions/{envId} | Get all the deplyments of enviroment across all versions
[**get_all_deployments_for_environment_by_id**](EnvironmentApi.md#get_all_deployments_for_environment_by_id) | **GET** /env/get-deployment-by-id/{envId} | Get all the deployments of Environment by environment id
[**get_all_deployments_for_environment_by_id_and_deployment_name**](EnvironmentApi.md#get_all_deployments_for_environment_by_id_and_deployment_name) | **GET** /env/get-deployment-by-name/{envId}/{deploymentName} | Get deployment of Environment by environment id and deployment name
[**get_all_environments**](EnvironmentApi.md#get_all_environments) | **GET** /env | Get all User environments
[**get_all_resources**](EnvironmentApi.md#get_all_resources) | **GET** /env/resources/{envId} | Gets all resources of an environment by environment id
[**get_cost_of_environment**](EnvironmentApi.md#get_cost_of_environment) | **GET** /env/{envId}/price | Estimated Cost of the environment before deploying Environment
[**get_deploy_resource_list**](EnvironmentApi.md#get_deploy_resource_list) | **GET** /env/deploy/{envId} | Gets all resources by deployment
[**get_deploy_resource_log**](EnvironmentApi.md#get_deploy_resource_log) | **GET** /env/deploy/resource/{envId}/{resourceId} | Gets terraform deploy logs for a resource.
[**get_deploy_status_by_env_id**](EnvironmentApi.md#get_deploy_status_by_env_id) | **GET** /env/deploy/status/{envId} | Gets default deployment status for an environment
[**get_deploy_status_by_env_id_and_deployment_name**](EnvironmentApi.md#get_deploy_status_by_env_id_and_deployment_name) | **GET** /env/deploy/status/{envId}/{deploymentName} | Gets deploy status for an environment by environment id and deployment name
[**get_deployed_resource_ids**](EnvironmentApi.md#get_deployed_resource_ids) | **GET** /env/resource/ids/{envId} | Gets all deployed resources information for an environment
[**get_deployment_details**](EnvironmentApi.md#get_deployment_details) | **GET** /env/deployment-details/{envId}/{deploymentName} | Get deployment of Environment by environment id and deployment name
[**get_deployment_input_json**](EnvironmentApi.md#get_deployment_input_json) | **GET** /env/get-input-json/{envId}/{deploymentName} | Get deployment&#39;s input json by environment id and deployment Name
[**get_deployment_status**](EnvironmentApi.md#get_deployment_status) | **GET** /env/deploy/deployment/{runId} | Gets deployment information related to runId of an environment
[**get_environment**](EnvironmentApi.md#get_environment) | **GET** /env/{envId} | Get Environment by Id
[**get_environment_by_version_and_name**](EnvironmentApi.md#get_environment_by_version_and_name) | **GET** /env/{envName}/{envVersion} | Get Environment by name and version
[**get_environment_difference**](EnvironmentApi.md#get_environment_difference) | **GET** /env/diff/{base_env_id}/{target_env_id} | Get environment difference of two enviroments
[**get_environment_hierarchy**](EnvironmentApi.md#get_environment_hierarchy) | **GET** /env/{envId}/hierarchy | Get hierarchical information about parents of specified specified environment
[**get_groups**](EnvironmentApi.md#get_groups) | **GET** /env/groups | Get all the platform groups
[**get_input_json**](EnvironmentApi.md#get_input_json) | **GET** /env/input/{envId} | Gets all environments resources json with attributes names/values
[**get_layout_resources**](EnvironmentApi.md#get_layout_resources) | **GET** /env/{envId}/layoutResources | Gets all resources of environment without their attributes/packages
[**get_links_between_resources**](EnvironmentApi.md#get_links_between_resources) | **GET** /env/resource/links/{envId} | Get dependency links between an environment resources
[**get_parent_deployment_mapping_data**](EnvironmentApi.md#get_parent_deployment_mapping_data) | **GET** /env/parentDeploymentMappingData/{envId}/{deploymentId} | Get Parent Deployment Map For Env For Deployment
[**get_private_key_for_resource**](EnvironmentApi.md#get_private_key_for_resource) | **GET** /env/privatekey/{envId}/{deploymentId}/{resourceId} | Gets private key for SSH keygen resource
[**get_resource_with_id**](EnvironmentApi.md#get_resource_with_id) | **GET** /env/resource/{resourceId} | Get resource with id
[**get_shared_environment**](EnvironmentApi.md#get_shared_environment) | **GET** /env/{envId}/share | Get environment sharing policy of environment by environment Id
[**get_tf_state**](EnvironmentApi.md#get_tf_state) | **GET** /env/tfstate/{envId} | Gets terraform state of the environment
[**get_validation_param**](EnvironmentApi.md#get_validation_param) | **GET** /env/validation/param/{envId} | 
[**import_blueprint**](EnvironmentApi.md#import_blueprint) | **POST** /env/import/blueprint | Import blurprint in REAN Deploy
[**import_environment**](EnvironmentApi.md#import_environment) | **POST** /env/import | Import environment into REAN Deploy.
[**is_multiple_resources**](EnvironmentApi.md#is_multiple_resources) | **GET** /env/resource/{resourceId}/multiple | True if resource has multiple resources
[**plan**](EnvironmentApi.md#plan) | **POST** /env/plan/{envId} | Plan for an environment using Environment id and Deploy configuration
[**plan_deployment**](EnvironmentApi.md#plan_deployment) | **POST** /env/plan/{envId}/{deploymentName} | Plan for an environment using Environment id, Deployment Name and Deploy configuration
[**prepare_import_blueprint**](EnvironmentApi.md#prepare_import_blueprint) | **POST** /env/import/blueprint/prepare | Prepare blueprint before importing it
[**prepare_import_environment**](EnvironmentApi.md#prepare_import_environment) | **POST** /env/import/prepare | Prepare environment imports before actually importing it
[**re_deploy_by_deployment_id_and_config**](EnvironmentApi.md#re_deploy_by_deployment_id_and_config) | **POST** /env/redeploy/deployment/{deploymentId} | Redeploy deployment using deployment id and Deploy configuration
[**re_deploy_by_env_name_version_and_config**](EnvironmentApi.md#re_deploy_by_env_name_version_and_config) | **POST** /env/redeploy/deployment/{envName}/{envVersion} | Redeploy an environment by name and version
[**refresh**](EnvironmentApi.md#refresh) | **POST** /env/refresh/{envId} | Executes refresh for an environment and gives changes, should be followed by updateState if change seems fine
[**save_all**](EnvironmentApi.md#save_all) | **POST** /env/saveAll | Save Environment with resources and their attributes and packages
[**save_as**](EnvironmentApi.md#save_as) | **POST** /env/saveAs | Copy Existing env with different name.
[**save_environment**](EnvironmentApi.md#save_environment) | **POST** /env | Save Environment
[**save_new_version**](EnvironmentApi.md#save_new_version) | **POST** /env/new-version | Create new Version
[**share_all_version_environment**](EnvironmentApi.md#share_all_version_environment) | **POST** /env/{envId}/share-all | Share all the versions of environment using specified policy
[**share_environment**](EnvironmentApi.md#share_environment) | **POST** /env/{envId}/share | Save of update environment sharing policies
[**stop_deployment**](EnvironmentApi.md#stop_deployment) | **POST** /env/deploy/stop/{deploymentId} | Stop ongoing deployment by deployment id
[**update_environment**](EnvironmentApi.md#update_environment) | **PUT** /env | Update Environment
[**update_package_version**](EnvironmentApi.md#update_package_version) | **POST** /env/resource/package/{resourceId}/{packageName}/{packageVersion} | Updated package version for package on environment resource
[**update_resource**](EnvironmentApi.md#update_resource) | **PUT** /env/resource | Update resource using payload
[**update_tf_state**](EnvironmentApi.md#update_tf_state) | **POST** /env/updateState/{envId} | Updates terraform state from refresh action on environment.
[**validate_resource_name_change**](EnvironmentApi.md#validate_resource_name_change) | **GET** /env/validate/{envId}/{resourceId}/{newName} | Check if new resource Name is valid, returns true if valid


# **check_environment_import_for_name_and_version**
> dict(str, str) check_environment_import_for_name_and_version(body=body)

Check if Environment Names And Version is already Exists

Example  - {\"name\" = \"version\"}

### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
body = NULL # object |  (optional)

try: 
    # Check if Environment Names And Version is already Exists
    api_response = api_instance.check_environment_import_for_name_and_version(body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->check_environment_import_for_name_and_version: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | **object**|  | [optional] 

### Return type

[**dict(str, str)**](dict.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **check_if_environment_exists**
> bool check_if_environment_exists(env_name)

Check if environment with specified name is already created by the user



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
env_name = 'env_name_example' # str | 

try: 
    # Check if environment with specified name is already created by the user
    api_response = api_instance.check_if_environment_exists(env_name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->check_if_environment_exists: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **env_name** | **str**|  | 

### Return type

**bool**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **confirm_destroy_env_by_token**
> EnvironmentDestroy confirm_destroy_env_by_token(token, all=all)

Destroy deployment using destroy token

Give true for param all if dependent environnments are also to be destroyed

### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
token = 'token_example' # str | 
all = false # bool |  (optional) (default to false)

try: 
    # Destroy deployment using destroy token
    api_response = api_instance.confirm_destroy_env_by_token(token, all=all)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->confirm_destroy_env_by_token: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **token** | **str**|  | 
 **all** | **bool**|  | [optional] [default to false]

### Return type

[**EnvironmentDestroy**](EnvironmentDestroy.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **copy_and_deploy**
> Environment copy_and_deploy(body=body)

Create a copy of an environment and deploy



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
body = deploy_sdk_client.CopyDeployConfig() # CopyDeployConfig |  (optional)

try: 
    # Create a copy of an environment and deploy
    api_response = api_instance.copy_and_deploy(body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->copy_and_deploy: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CopyDeployConfig**](CopyDeployConfig.md)|  | [optional] 

### Return type

[**Environment**](Environment.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **copy_environment**
> Environment copy_environment(body=body)

Copy an environment using configuration like tags and input variables



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
body = deploy_sdk_client.ConfigurationUsedForCopydeployAPI() # ConfigurationUsedForCopydeployAPI |  (optional)

try: 
    # Copy an environment using configuration like tags and input variables
    api_response = api_instance.copy_environment(body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->copy_environment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConfigurationUsedForCopydeployAPI**](ConfigurationUsedForCopydeployAPI.md)|  | [optional] 

### Return type

[**Environment**](Environment.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_empty_env_resource**
> EnvResource create_empty_env_resource(env_id, name, resource_name)

Creates a new resource with given name and resourceName and gives resource template to set applicable attribute values



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
env_id = 789 # int | 
name = 'name_example' # str | 
resource_name = 'resource_name_example' # str | 

try: 
    # Creates a new resource with given name and resourceName and gives resource template to set applicable attribute values
    api_response = api_instance.create_empty_env_resource(env_id, name, resource_name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->create_empty_env_resource: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **env_id** | **int**|  | 
 **name** | **str**|  | 
 **resource_name** | **str**|  | 

### Return type

[**EnvResource**](EnvResource.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_new_env_package**
> list[EnvPackage] create_new_env_package(resource_id, package_name, header_env_id, modified_on)

Create package on the resource and gives package template to set values for required attributes



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
resource_id = 789 # int | 
package_name = 'package_name_example' # str | 
header_env_id = 56 # int | 
modified_on = 56 # int | 

try: 
    # Create package on the resource and gives package template to set values for required attributes
    api_response = api_instance.create_new_env_package(resource_id, package_name, header_env_id, modified_on)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->create_new_env_package: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **resource_id** | **int**|  | 
 **package_name** | **str**|  | 
 **header_env_id** | **int**|  | 
 **modified_on** | **int**|  | 

### Return type

[**list[EnvPackage]**](EnvPackage.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_new_env_resource**
> EnvResource create_new_env_resource(env_id, header_env_id, modified_on, body=body)

Creates a new resource with given name and resourceName and positionX and positionY and gives resource template to set applicable attribute values



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
env_id = 789 # int | 
header_env_id = 56 # int | 
modified_on = 56 # int | 
body = deploy_sdk_client.EnvResource() # EnvResource |  (optional)

try: 
    # Creates a new resource with given name and resourceName and positionX and positionY and gives resource template to set applicable attribute values
    api_response = api_instance.create_new_env_resource(env_id, header_env_id, modified_on, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->create_new_env_resource: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **env_id** | **int**|  | 
 **header_env_id** | **int**|  | 
 **modified_on** | **int**|  | 
 **body** | [**EnvResource**](EnvResource.md)|  | [optional] 

### Return type

[**EnvResource**](EnvResource.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_new_env_resource_using_import**
> list[EnvResource] create_new_env_resource_using_import(env_id, header_env_id, modified_on, body=body)

Creates a new resource with given name, resourceName, positonX, positionY, and existingId and gives resource template to set applicable attribute values



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
env_id = 789 # int | 
header_env_id = 56 # int | 
modified_on = 56 # int | 
body = deploy_sdk_client.EnvResource() # EnvResource |  (optional)

try: 
    # Creates a new resource with given name, resourceName, positonX, positionY, and existingId and gives resource template to set applicable attribute values
    api_response = api_instance.create_new_env_resource_using_import(env_id, header_env_id, modified_on, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->create_new_env_resource_using_import: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **env_id** | **int**|  | 
 **header_env_id** | **int**|  | 
 **modified_on** | **int**|  | 
 **body** | [**EnvResource**](EnvResource.md)|  | [optional] 

### Return type

[**list[EnvResource]**](EnvResource.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_environment**
> Environment delete_environment(env_id)

Deletes environment by id



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
env_id = 789 # int | 

try: 
    # Deletes environment by id
    api_response = api_instance.delete_environment(env_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->delete_environment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **env_id** | **int**|  | 

### Return type

[**Environment**](Environment.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_package**
> str delete_package(package_id)

delete package by id



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
package_id = 789 # int | 

try: 
    # delete package by id
    api_response = api_instance.delete_package(package_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->delete_package: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **package_id** | **int**|  | 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_resource**
> EnvResource delete_resource(resource_id)

Delete resource by id



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
resource_id = 789 # int | 

try: 
    # Delete resource by id
    api_response = api_instance.delete_resource(resource_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->delete_resource: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **resource_id** | **int**|  | 

### Return type

[**EnvResource**](EnvResource.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **deploy_as_blueprint**
> Environment deploy_as_blueprint(env_id)

Deploy an environment by id



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
env_id = 789 # int | 

try: 
    # Deploy an environment by id
    api_response = api_instance.deploy_as_blueprint(env_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->deploy_as_blueprint: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **env_id** | **int**|  | 

### Return type

[**Environment**](Environment.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **deploy_by_config**
> Deployment deploy_by_config(body=body)

Deploy/Redeploys an environment by environment id with deployment name and other deployment configurations



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
body = deploy_sdk_client.DeploymentConfigurationDto() # DeploymentConfigurationDto |  (optional)

try: 
    # Deploy/Redeploys an environment by environment id with deployment name and other deployment configurations
    api_response = api_instance.deploy_by_config(body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->deploy_by_config: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**DeploymentConfigurationDto**](DeploymentConfigurationDto.md)|  | [optional] 

### Return type

[**Deployment**](Deployment.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **deploy_by_env_id**
> Deployment deploy_by_env_id(env_id, body=body)

Deploy an environment by environment id with deploy configuration



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
env_id = 789 # int | 
body = deploy_sdk_client.DeploymentConfiguration() # DeploymentConfiguration |  (optional)

try: 
    # Deploy an environment by environment id with deploy configuration
    api_response = api_instance.deploy_by_env_id(env_id, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->deploy_by_env_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **env_id** | **int**|  | 
 **body** | [**DeploymentConfiguration**](DeploymentConfiguration.md)|  | [optional] 

### Return type

[**Deployment**](Deployment.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **deploy_by_env_id_and_config**
> Deployment deploy_by_env_id_and_config(env_id, body=body)

Deploy an environment by environment id



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
env_id = 789 # int | 
body = deploy_sdk_client.DeploymentConfiguration() # DeploymentConfiguration |  (optional)

try: 
    # Deploy an environment by environment id
    api_response = api_instance.deploy_by_env_id_and_config(env_id, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->deploy_by_env_id_and_config: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **env_id** | **int**|  | 
 **body** | [**DeploymentConfiguration**](DeploymentConfiguration.md)|  | [optional] 

### Return type

[**Deployment**](Deployment.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **deploy_by_env_name_version_and_config**
> Deployment deploy_by_env_name_version_and_config(env_name, env_version, body=body)

Deploy an environment by name and version



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
env_name = 'env_name_example' # str | 
env_version = 'env_version_example' # str | 
body = deploy_sdk_client.DeploymentConfiguration() # DeploymentConfiguration |  (optional)

try: 
    # Deploy an environment by name and version
    api_response = api_instance.deploy_by_env_name_version_and_config(env_name, env_version, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->deploy_by_env_name_version_and_config: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **env_name** | **str**|  | 
 **env_version** | **str**|  | 
 **body** | [**DeploymentConfiguration**](DeploymentConfiguration.md)|  | [optional] 

### Return type

[**Deployment**](Deployment.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **destroy**
> Deployment destroy(env_id)

Destroys environment deployment from REAN Deploy and Actually erases your infracture on provider



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
env_id = 789 # int | 

try: 
    # Destroys environment deployment from REAN Deploy and Actually erases your infracture on provider
    api_response = api_instance.destroy(env_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->destroy: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **env_id** | **int**|  | 

### Return type

[**Deployment**](Deployment.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **destroy_deployment_by_env_name_and_deployment_name**
> Deployment destroy_deployment_by_env_name_and_deployment_name(env_name, deployment_name)

Destroys environment deployment. Actually erases your infracture on provider



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
env_name = 'env_name_example' # str | 
deployment_name = 'deployment_name_example' # str | 

try: 
    # Destroys environment deployment. Actually erases your infracture on provider
    api_response = api_instance.destroy_deployment_by_env_name_and_deployment_name(env_name, deployment_name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->destroy_deployment_by_env_name_and_deployment_name: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **env_name** | **str**|  | 
 **deployment_name** | **str**|  | 

### Return type

[**Deployment**](Deployment.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **destroy_deployment_by_id**
> Deployment destroy_deployment_by_id(deployment_id)

Destroys environment deployment. Actually erases your infracture on provider



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
deployment_id = 789 # int | 

try: 
    # Destroys environment deployment. Actually erases your infracture on provider
    api_response = api_instance.destroy_deployment_by_id(deployment_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->destroy_deployment_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **deployment_id** | **int**|  | 

### Return type

[**Deployment**](Deployment.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **destroy_deployment_by_id_and_deployment_name**
> Deployment destroy_deployment_by_id_and_deployment_name(env_id, deployment_name)

Destroys environment deployment. Actually erases your infracture on provider



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
env_id = 789 # int | 
deployment_name = 'deployment_name_example' # str | 

try: 
    # Destroys environment deployment. Actually erases your infracture on provider
    api_response = api_instance.destroy_deployment_by_id_and_deployment_name(env_id, deployment_name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->destroy_deployment_by_id_and_deployment_name: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **env_id** | **int**|  | 
 **deployment_name** | **str**|  | 

### Return type

[**Deployment**](Deployment.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **destroy_env_by_token**
> EnvironmentDestroy destroy_env_by_token(token, all=all)

One-time destroy of an an environment by a non-user using token



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
token = 'token_example' # str | 
all = false # bool |  (optional) (default to false)

try: 
    # One-time destroy of an an environment by a non-user using token
    api_response = api_instance.destroy_env_by_token(token, all=all)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->destroy_env_by_token: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **token** | **str**|  | 
 **all** | **bool**|  | [optional] [default to false]

### Return type

[**EnvironmentDestroy**](EnvironmentDestroy.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **download_terraform_files**
> download_terraform_files(env_id)

Gives zip stream of all terraform files for an environment



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
env_id = 789 # int | 

try: 
    # Gives zip stream of all terraform files for an environment
    api_instance.download_terraform_files(env_id)
except ApiException as e:
    print("Exception when calling EnvironmentApi->download_terraform_files: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **env_id** | **int**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/gzip

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **export_blueprint_environment**
> BlueprintEnvImport export_blueprint_environment(env_id)

Export Environment with all Parent environment which can be imported into another REAN Deploy Server



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
env_id = 789 # int | 

try: 
    # Export Environment with all Parent environment which can be imported into another REAN Deploy Server
    api_response = api_instance.export_blueprint_environment(env_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->export_blueprint_environment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **env_id** | **int**|  | 

### Return type

[**BlueprintEnvImport**](BlueprintEnvImport.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **export_environment**
> ExportedEnvironment export_environment(env_id)

Export Environment into JSON format

Gets Json of an environment with applicable values to be imported into another REAN Deploy server

### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
env_id = 789 # int | 

try: 
    # Export Environment into JSON format
    api_response = api_instance.export_environment(env_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->export_environment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **env_id** | **int**|  | 

### Return type

[**ExportedEnvironment**](ExportedEnvironment.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_actions**
> list[str] get_actions(resource_type)

Get all supported Resource type



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
resource_type = 'resource_type_example' # str | 

try: 
    # Get all supported Resource type
    api_response = api_instance.get_actions(resource_type)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->get_actions: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **resource_type** | **str**|  | 

### Return type

**list[str]**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_deployments_for_environment**
> list[Deployment] get_all_deployments_for_environment(env_name)

Get all the deplyments of enviroment which are owned by loggedIn User



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
env_name = 'env_name_example' # str | 

try: 
    # Get all the deplyments of enviroment which are owned by loggedIn User
    api_response = api_instance.get_all_deployments_for_environment(env_name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->get_all_deployments_for_environment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **env_name** | **str**|  | 

### Return type

[**list[Deployment]**](Deployment.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_deployments_for_environment_across_versions**
> list[Deployment] get_all_deployments_for_environment_across_versions(env_id)

Get all the deplyments of enviroment across all versions



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
env_id = 789 # int | 

try: 
    # Get all the deplyments of enviroment across all versions
    api_response = api_instance.get_all_deployments_for_environment_across_versions(env_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->get_all_deployments_for_environment_across_versions: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **env_id** | **int**|  | 

### Return type

[**list[Deployment]**](Deployment.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_deployments_for_environment_by_id**
> list[Deployment] get_all_deployments_for_environment_by_id(env_id)

Get all the deployments of Environment by environment id



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
env_id = 789 # int | 

try: 
    # Get all the deployments of Environment by environment id
    api_response = api_instance.get_all_deployments_for_environment_by_id(env_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->get_all_deployments_for_environment_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **env_id** | **int**|  | 

### Return type

[**list[Deployment]**](Deployment.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_deployments_for_environment_by_id_and_deployment_name**
> Deployment get_all_deployments_for_environment_by_id_and_deployment_name(env_id, deployment_name)

Get deployment of Environment by environment id and deployment name



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
env_id = 789 # int | 
deployment_name = 'deployment_name_example' # str | 

try: 
    # Get deployment of Environment by environment id and deployment name
    api_response = api_instance.get_all_deployments_for_environment_by_id_and_deployment_name(env_id, deployment_name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->get_all_deployments_for_environment_by_id_and_deployment_name: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **env_id** | **int**|  | 
 **deployment_name** | **str**|  | 

### Return type

[**Deployment**](Deployment.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_environments**
> Environment get_all_environments()

Get all User environments



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()

try: 
    # Get all User environments
    api_response = api_instance.get_all_environments()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->get_all_environments: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**Environment**](Environment.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_resources**
> list[EnvResource] get_all_resources(env_id)

Gets all resources of an environment by environment id



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
env_id = 789 # int | 

try: 
    # Gets all resources of an environment by environment id
    api_response = api_instance.get_all_resources(env_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->get_all_resources: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **env_id** | **int**|  | 

### Return type

[**list[EnvResource]**](EnvResource.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_cost_of_environment**
> dict(str, list[AWSPriceMap]) get_cost_of_environment(env_id)

Estimated Cost of the environment before deploying Environment



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
env_id = 789 # int | environment ID

try: 
    # Estimated Cost of the environment before deploying Environment
    api_response = api_instance.get_cost_of_environment(env_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->get_cost_of_environment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **env_id** | **int**| environment ID | 

### Return type

[**dict(str, list[AWSPriceMap])**](dict.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_deploy_resource_list**
> dict(str, list[TFResource]) get_deploy_resource_list(env_id)

Gets all resources by deployment



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
env_id = 789 # int | 

try: 
    # Gets all resources by deployment
    api_response = api_instance.get_deploy_resource_list(env_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->get_deploy_resource_list: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **env_id** | **int**|  | 

### Return type

[**dict(str, list[TFResource])**](dict.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_deploy_resource_log**
> str get_deploy_resource_log(env_id, resource_id)

Gets terraform deploy logs for a resource.

To get entire log for an environment send resourceId as -1

### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
env_id = 789 # int | 
resource_id = 789 # int | 

try: 
    # Gets terraform deploy logs for a resource.
    api_response = api_instance.get_deploy_resource_log(env_id, resource_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->get_deploy_resource_log: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **env_id** | **int**|  | 
 **resource_id** | **int**|  | 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_deploy_status_by_env_id**
> TFExecutionStatus get_deploy_status_by_env_id(env_id)

Gets default deployment status for an environment



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
env_id = 789 # int | 

try: 
    # Gets default deployment status for an environment
    api_response = api_instance.get_deploy_status_by_env_id(env_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->get_deploy_status_by_env_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **env_id** | **int**|  | 

### Return type

[**TFExecutionStatus**](TFExecutionStatus.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_deploy_status_by_env_id_and_deployment_name**
> TFExecutionStatus get_deploy_status_by_env_id_and_deployment_name(env_id, deployment_name)

Gets deploy status for an environment by environment id and deployment name



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
env_id = 789 # int | 
deployment_name = 'deployment_name_example' # str | 

try: 
    # Gets deploy status for an environment by environment id and deployment name
    api_response = api_instance.get_deploy_status_by_env_id_and_deployment_name(env_id, deployment_name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->get_deploy_status_by_env_id_and_deployment_name: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **env_id** | **int**|  | 
 **deployment_name** | **str**|  | 

### Return type

[**TFExecutionStatus**](TFExecutionStatus.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_deployed_resource_ids**
> get_deployed_resource_ids(env_id)

Gets all deployed resources information for an environment

Gives map of resource name and ids

### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
env_id = 789 # int | 

try: 
    # Gets all deployed resources information for an environment
    api_instance.get_deployed_resource_ids(env_id)
except ApiException as e:
    print("Exception when calling EnvironmentApi->get_deployed_resource_ids: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **env_id** | **int**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_deployment_details**
> Deployment get_deployment_details(env_id, deployment_name)

Get deployment of Environment by environment id and deployment name



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
env_id = 789 # int | 
deployment_name = 'deployment_name_example' # str | 

try: 
    # Get deployment of Environment by environment id and deployment name
    api_response = api_instance.get_deployment_details(env_id, deployment_name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->get_deployment_details: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **env_id** | **int**|  | 
 **deployment_name** | **str**|  | 

### Return type

[**Deployment**](Deployment.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_deployment_input_json**
> str get_deployment_input_json(env_id, deployment_name)

Get deployment's input json by environment id and deployment Name



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
env_id = 789 # int | 
deployment_name = 'deployment_name_example' # str | 

try: 
    # Get deployment's input json by environment id and deployment Name
    api_response = api_instance.get_deployment_input_json(env_id, deployment_name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->get_deployment_input_json: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **env_id** | **int**|  | 
 **deployment_name** | **str**|  | 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_deployment_status**
> Deployment get_deployment_status(run_id)

Gets deployment information related to runId of an environment



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
run_id = 'run_id_example' # str | 

try: 
    # Gets deployment information related to runId of an environment
    api_response = api_instance.get_deployment_status(run_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->get_deployment_status: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **run_id** | **str**|  | 

### Return type

[**Deployment**](Deployment.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_environment**
> Environment get_environment(env_id)

Get Environment by Id



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
env_id = 789 # int | Environment ID

try: 
    # Get Environment by Id
    api_response = api_instance.get_environment(env_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->get_environment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **env_id** | **int**| Environment ID | 

### Return type

[**Environment**](Environment.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_environment_by_version_and_name**
> Environment get_environment_by_version_and_name(env_name, env_version)

Get Environment by name and version



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
env_name = 'env_name_example' # str | Environment ID
env_version = 'env_version_example' # str | Environment Version

try: 
    # Get Environment by name and version
    api_response = api_instance.get_environment_by_version_and_name(env_name, env_version)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->get_environment_by_version_and_name: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **env_name** | **str**| Environment ID | 
 **env_version** | **str**| Environment Version | 

### Return type

[**Environment**](Environment.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_environment_difference**
> EnvironmentDiffDto get_environment_difference(base_env_id, target_env_id)

Get environment difference of two enviroments



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
base_env_id = 789 # int | 
target_env_id = 789 # int | 

try: 
    # Get environment difference of two enviroments
    api_response = api_instance.get_environment_difference(base_env_id, target_env_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->get_environment_difference: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **base_env_id** | **int**|  | 
 **target_env_id** | **int**|  | 

### Return type

[**EnvironmentDiffDto**](EnvironmentDiffDto.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_environment_hierarchy**
> EnvironmentParentHierarchy get_environment_hierarchy(env_id)

Get hierarchical information about parents of specified specified environment



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
env_id = 789 # int | environment ID

try: 
    # Get hierarchical information about parents of specified specified environment
    api_response = api_instance.get_environment_hierarchy(env_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->get_environment_hierarchy: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **env_id** | **int**| environment ID | 

### Return type

[**EnvironmentParentHierarchy**](EnvironmentParentHierarchy.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_groups**
> list[GroupDto] get_groups()

Get all the platform groups



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()

try: 
    # Get all the platform groups
    api_response = api_instance.get_groups()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->get_groups: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[GroupDto]**](GroupDto.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_input_json**
> str get_input_json(env_id)

Gets all environments resources json with attributes names/values



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
env_id = 789 # int | 

try: 
    # Gets all environments resources json with attributes names/values
    api_response = api_instance.get_input_json(env_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->get_input_json: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **env_id** | **int**|  | 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_layout_resources**
> list[EnvResource] get_layout_resources(env_id)

Gets all resources of environment without their attributes/packages



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
env_id = 789 # int | 

try: 
    # Gets all resources of environment without their attributes/packages
    api_response = api_instance.get_layout_resources(env_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->get_layout_resources: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **env_id** | **int**|  | 

### Return type

[**list[EnvResource]**](EnvResource.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_links_between_resources**
> list[ResourceLink] get_links_between_resources(env_id)

Get dependency links between an environment resources



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
env_id = 789 # int | 

try: 
    # Get dependency links between an environment resources
    api_response = api_instance.get_links_between_resources(env_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->get_links_between_resources: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **env_id** | **int**|  | 

### Return type

[**list[ResourceLink]**](ResourceLink.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_parent_deployment_mapping_data**
> list[ParentDeploymentMapping] get_parent_deployment_mapping_data(env_id, deployment_id)

Get Parent Deployment Map For Env For Deployment



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
env_id = 789 # int | 
deployment_id = 789 # int | 

try: 
    # Get Parent Deployment Map For Env For Deployment
    api_response = api_instance.get_parent_deployment_mapping_data(env_id, deployment_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->get_parent_deployment_mapping_data: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **env_id** | **int**|  | 
 **deployment_id** | **int**|  | 

### Return type

[**list[ParentDeploymentMapping]**](ParentDeploymentMapping.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_private_key_for_resource**
> str get_private_key_for_resource(env_id, deployment_id, resource_id)

Gets private key for SSH keygen resource



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
env_id = 789 # int | 
deployment_id = 789 # int | 
resource_id = 789 # int | 

try: 
    # Gets private key for SSH keygen resource
    api_response = api_instance.get_private_key_for_resource(env_id, deployment_id, resource_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->get_private_key_for_resource: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **env_id** | **int**|  | 
 **deployment_id** | **int**|  | 
 **resource_id** | **int**|  | 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_resource_with_id**
> EnvResource get_resource_with_id(resource_id)

Get resource with id



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
resource_id = 789 # int | 

try: 
    # Get resource with id
    api_response = api_instance.get_resource_with_id(resource_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->get_resource_with_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **resource_id** | **int**|  | 

### Return type

[**EnvResource**](EnvResource.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_shared_environment**
> EnvironmentPolicy get_shared_environment(env_id)

Get environment sharing policy of environment by environment Id



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
env_id = 789 # int | 

try: 
    # Get environment sharing policy of environment by environment Id
    api_response = api_instance.get_shared_environment(env_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->get_shared_environment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **env_id** | **int**|  | 

### Return type

[**EnvironmentPolicy**](EnvironmentPolicy.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_tf_state**
> get_tf_state(env_id)

Gets terraform state of the environment

Response will be same as tfstate file

### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
env_id = 789 # int | 

try: 
    # Gets terraform state of the environment
    api_instance.get_tf_state(env_id)
except ApiException as e:
    print("Exception when calling EnvironmentApi->get_tf_state: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **env_id** | **int**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_validation_param**
> get_validation_param(env_id)



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
env_id = 789 # int | 

try: 
    api_instance.get_validation_param(env_id)
except ApiException as e:
    print("Exception when calling EnvironmentApi->get_validation_param: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **env_id** | **int**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

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
api_instance = deploy_sdk_client.EnvironmentApi()
body = deploy_sdk_client.BlueprintImport() # BlueprintImport |  (optional)

try: 
    # Import blurprint in REAN Deploy
    api_instance.import_blueprint(body=body)
except ApiException as e:
    print("Exception when calling EnvironmentApi->import_blueprint: %s\n" % e)
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

# **import_environment**
> Environment import_environment(body=body)

Import environment into REAN Deploy.

Use this API after prepareImport API. Set required params from prepare and use import

### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
body = deploy_sdk_client.EnvironmentImport() # EnvironmentImport |  (optional)

try: 
    # Import environment into REAN Deploy.
    api_response = api_instance.import_environment(body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->import_environment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**EnvironmentImport**](EnvironmentImport.md)|  | [optional] 

### Return type

[**Environment**](Environment.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **is_multiple_resources**
> bool is_multiple_resources(resource_id)

True if resource has multiple resources



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
resource_id = 789 # int | 

try: 
    # True if resource has multiple resources
    api_response = api_instance.is_multiple_resources(resource_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->is_multiple_resources: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **resource_id** | **int**|  | 

### Return type

**bool**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **plan**
> TFPlanOutput plan(env_id, body=body)

Plan for an environment using Environment id and Deploy configuration



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
env_id = 789 # int | 
body = deploy_sdk_client.DeploymentConfiguration() # DeploymentConfiguration |  (optional)

try: 
    # Plan for an environment using Environment id and Deploy configuration
    api_response = api_instance.plan(env_id, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->plan: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **env_id** | **int**|  | 
 **body** | [**DeploymentConfiguration**](DeploymentConfiguration.md)|  | [optional] 

### Return type

[**TFPlanOutput**](TFPlanOutput.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **plan_deployment**
> TFPlanOutput plan_deployment(env_id, deployment_name, body=body)

Plan for an environment using Environment id, Deployment Name and Deploy configuration



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
env_id = 789 # int | 
deployment_name = 'deployment_name_example' # str | 
body = deploy_sdk_client.DeploymentConfiguration() # DeploymentConfiguration |  (optional)

try: 
    # Plan for an environment using Environment id, Deployment Name and Deploy configuration
    api_response = api_instance.plan_deployment(env_id, deployment_name, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->plan_deployment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **env_id** | **int**|  | 
 **deployment_name** | **str**|  | 
 **body** | [**DeploymentConfiguration**](DeploymentConfiguration.md)|  | [optional] 

### Return type

[**TFPlanOutput**](TFPlanOutput.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **prepare_import_blueprint**
> BlueprintImport prepare_import_blueprint(file=file)

Prepare blueprint before importing it

Given a blueprint file, it returns response to set typical environment create params to send it to blueprint import API

### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
file = '/path/to/file.txt' # file |  (optional)

try: 
    # Prepare blueprint before importing it
    api_response = api_instance.prepare_import_blueprint(file=file)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->prepare_import_blueprint: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file** | **file**|  | [optional] 

### Return type

[**BlueprintImport**](BlueprintImport.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **prepare_import_environment**
> EnvironmentImport prepare_import_environment(file=file)

Prepare environment imports before actually importing it

Given an import files, it returns response to set typical environment create params to send it to import API

### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
file = '/path/to/file.txt' # file |  (optional)

try: 
    # Prepare environment imports before actually importing it
    api_response = api_instance.prepare_import_environment(file=file)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->prepare_import_environment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file** | **file**|  | [optional] 

### Return type

[**EnvironmentImport**](EnvironmentImport.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **re_deploy_by_deployment_id_and_config**
> Deployment re_deploy_by_deployment_id_and_config(deployment_id, body=body)

Redeploy deployment using deployment id and Deploy configuration



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
deployment_id = 789 # int | 
body = deploy_sdk_client.DeploymentConfiguration() # DeploymentConfiguration |  (optional)

try: 
    # Redeploy deployment using deployment id and Deploy configuration
    api_response = api_instance.re_deploy_by_deployment_id_and_config(deployment_id, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->re_deploy_by_deployment_id_and_config: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **deployment_id** | **int**|  | 
 **body** | [**DeploymentConfiguration**](DeploymentConfiguration.md)|  | [optional] 

### Return type

[**Deployment**](Deployment.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **re_deploy_by_env_name_version_and_config**
> Deployment re_deploy_by_env_name_version_and_config(env_name, env_version, body=body)

Redeploy an environment by name and version



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
env_name = 'env_name_example' # str | 
env_version = 'env_version_example' # str | 
body = deploy_sdk_client.DeploymentConfiguration() # DeploymentConfiguration |  (optional)

try: 
    # Redeploy an environment by name and version
    api_response = api_instance.re_deploy_by_env_name_version_and_config(env_name, env_version, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->re_deploy_by_env_name_version_and_config: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **env_name** | **str**|  | 
 **env_version** | **str**|  | 
 **body** | [**DeploymentConfiguration**](DeploymentConfiguration.md)|  | [optional] 

### Return type

[**Deployment**](Deployment.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **refresh**
> list[TFResourceChangeLog] refresh(env_id)

Executes refresh for an environment and gives changes, should be followed by updateState if change seems fine



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
env_id = 789 # int | 

try: 
    # Executes refresh for an environment and gives changes, should be followed by updateState if change seems fine
    api_response = api_instance.refresh(env_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->refresh: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **env_id** | **int**|  | 

### Return type

[**list[TFResourceChangeLog]**](TFResourceChangeLog.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **save_all**
> EnvironmentSaveAll save_all(body=body)

Save Environment with resources and their attributes and packages



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
body = deploy_sdk_client.EnvironmentSaveAll() # EnvironmentSaveAll |  (optional)

try: 
    # Save Environment with resources and their attributes and packages
    api_response = api_instance.save_all(body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->save_all: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**EnvironmentSaveAll**](EnvironmentSaveAll.md)|  | [optional] 

### Return type

[**EnvironmentSaveAll**](EnvironmentSaveAll.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **save_as**
> Environment save_as(body=body)

Copy Existing env with different name.

Payload should contain the id of the environment you are copying and name of the environment you want to create as new and other applicable env creation params

### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
body = deploy_sdk_client.Environment() # Environment |  (optional)

try: 
    # Copy Existing env with different name.
    api_response = api_instance.save_as(body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->save_as: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Environment**](Environment.md)|  | [optional] 

### Return type

[**Environment**](Environment.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **save_environment**
> Environment save_environment(body=body)

Save Environment



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
body = deploy_sdk_client.Environment() # Environment |  (optional)

try: 
    # Save Environment
    api_response = api_instance.save_environment(body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->save_environment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Environment**](Environment.md)|  | [optional] 

### Return type

[**Environment**](Environment.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **save_new_version**
> Environment save_new_version(body=body)

Create new Version

Payload should contain the id and name of the environment for which new version is created. New Version should be greater than the version from which its being created

### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
body = deploy_sdk_client.Environment() # Environment |  (optional)

try: 
    # Create new Version
    api_response = api_instance.save_new_version(body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->save_new_version: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Environment**](Environment.md)|  | [optional] 

### Return type

[**Environment**](Environment.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **share_all_version_environment**
> share_all_version_environment(env_id, body=body)

Share all the versions of environment using specified policy



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
env_id = 789 # int | 
body = deploy_sdk_client.EnvironmentPolicy() # EnvironmentPolicy |  (optional)

try: 
    # Share all the versions of environment using specified policy
    api_instance.share_all_version_environment(env_id, body=body)
except ApiException as e:
    print("Exception when calling EnvironmentApi->share_all_version_environment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **env_id** | **int**|  | 
 **body** | [**EnvironmentPolicy**](EnvironmentPolicy.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **share_environment**
> share_environment(env_id, body=body)

Save of update environment sharing policies



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
env_id = 789 # int | 
body = deploy_sdk_client.EnvironmentPolicy() # EnvironmentPolicy |  (optional)

try: 
    # Save of update environment sharing policies
    api_instance.share_environment(env_id, body=body)
except ApiException as e:
    print("Exception when calling EnvironmentApi->share_environment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **env_id** | **int**|  | 
 **body** | [**EnvironmentPolicy**](EnvironmentPolicy.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **stop_deployment**
> StopRequestStatus stop_deployment(deployment_id)

Stop ongoing deployment by deployment id



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
deployment_id = 789 # int | 

try: 
    # Stop ongoing deployment by deployment id
    api_response = api_instance.stop_deployment(deployment_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->stop_deployment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **deployment_id** | **int**|  | 

### Return type

[**StopRequestStatus**](StopRequestStatus.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_environment**
> Environment update_environment(header_env_id, modified_on, body=body)

Update Environment



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
header_env_id = 56 # int | 
modified_on = 56 # int | 
body = deploy_sdk_client.Environment() # Environment |  (optional)

try: 
    # Update Environment
    api_response = api_instance.update_environment(header_env_id, modified_on, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->update_environment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **header_env_id** | **int**|  | 
 **modified_on** | **int**|  | 
 **body** | [**Environment**](Environment.md)|  | [optional] 

### Return type

[**Environment**](Environment.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_package_version**
> EnvPackage update_package_version(resource_id, package_name, package_version, header_env_id, modified_on)

Updated package version for package on environment resource



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
resource_id = 789 # int | 
package_name = 'package_name_example' # str | 
package_version = 'package_version_example' # str | 
header_env_id = 56 # int | 
modified_on = 56 # int | 

try: 
    # Updated package version for package on environment resource
    api_response = api_instance.update_package_version(resource_id, package_name, package_version, header_env_id, modified_on)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->update_package_version: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **resource_id** | **int**|  | 
 **package_name** | **str**|  | 
 **package_version** | **str**|  | 
 **header_env_id** | **int**|  | 
 **modified_on** | **int**|  | 

### Return type

[**EnvPackage**](EnvPackage.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_resource**
> EnvResource update_resource(header_env_id, modified_on, body=body)

Update resource using payload



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
header_env_id = 56 # int | 
modified_on = 56 # int | 
body = deploy_sdk_client.EnvResource() # EnvResource |  (optional)

try: 
    # Update resource using payload
    api_response = api_instance.update_resource(header_env_id, modified_on, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->update_resource: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **header_env_id** | **int**|  | 
 **modified_on** | **int**|  | 
 **body** | [**EnvResource**](EnvResource.md)|  | [optional] 

### Return type

[**EnvResource**](EnvResource.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_tf_state**
> Environment update_tf_state(env_id)

Updates terraform state from refresh action on environment.

Once updated, state file can not be reverted

### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
env_id = 789 # int | 

try: 
    # Updates terraform state from refresh action on environment.
    api_response = api_instance.update_tf_state(env_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->update_tf_state: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **env_id** | **int**|  | 

### Return type

[**Environment**](Environment.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **validate_resource_name_change**
> str validate_resource_name_change(resource_id, env_id, new_name, header_env_id, modified_on)

Check if new resource Name is valid, returns true if valid



### Example 
```python
from __future__ import print_function
import time
import deploy_sdk_client
from deploy_sdk_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = deploy_sdk_client.EnvironmentApi()
resource_id = 789 # int | 
env_id = 789 # int | 
new_name = 'new_name_example' # str | 
header_env_id = 56 # int | 
modified_on = 56 # int | 

try: 
    # Check if new resource Name is valid, returns true if valid
    api_response = api_instance.validate_resource_name_change(resource_id, env_id, new_name, header_env_id, modified_on)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnvironmentApi->validate_resource_name_change: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **resource_id** | **int**|  | 
 **env_id** | **int**|  | 
 **new_name** | **str**|  | 
 **header_env_id** | **int**|  | 
 **modified_on** | **int**|  | 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


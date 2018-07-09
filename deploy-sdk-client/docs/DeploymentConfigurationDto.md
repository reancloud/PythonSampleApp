# DeploymentConfigurationDto

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**deployment_name** | **str** | Name of Deployment. Unique for each environment | 
**environment_id** | **int** | Id of Environment which is getting deployed | [optional] 
**input_json** | **str** | Input variable JSON to override default values configured in \&quot;Input Variable\&quot; resource of the Environment. This input is used for parameterizing the environment deployments. | [optional] 
**parent_deployments** | **dict(str, object)** | Map of parent deployment where key is a name of \&quot;Depends On\&quot; resource and value is a name/id of the deployment for the parent environment. | [optional] 
**deployment_description** | **str** | Description of deployment | [optional] 
**provider_name** | **str** | Name of the Provider which should be used for Deployment | [optional] 
**custom_tag** | [**CustomTag**](CustomTag.md) | Custom tag for environment | [optional] 
**region** | **str** | Region into which environment resources should be launched. Defaults to set Provider region if any | [optional] 
**connections** | **dict(str, str)** | Map of connections where key is the name of resource and value is the name or id of connection | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



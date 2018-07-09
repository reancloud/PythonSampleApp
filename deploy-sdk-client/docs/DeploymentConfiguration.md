# DeploymentConfiguration

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**deployment_id** | **int** |  | [optional] 
**deployment_name** | **str** | Name of Deployment. Unique for each environment | 
**deployment_description** | **str** | Description of deployment | [optional] 
**provider_name** | **str** | Name of the Provider which should be used for Deployment | [optional] 
**region** | **str** | Region into which environment resources should be launched. Defaults to set Provider region if any | [optional] 
**connections** | **dict(str, str)** | Map of connections where key is the name of resource and value is the name or id of connection | [optional] 
**parent_deployments** | **dict(str, object)** | Map of parent deployment where key is a name of \&quot;Depends On\&quot; resource and value is a name/id of the deployment for the parent environment. | [optional] 
**input_json** | **str** | Input variable JSON to override default values configured in \&quot;Input Variable\&quot; resource of the Environment. This input is used for parameterizing the environment deployments. | [optional] 
**environment_id** | **int** | Id of Environment which is getting deployed | [optional] 
**destroy_after_min** | **int** | A value in minutes to Automatically destroy deployment after a specified time | [optional] 
**email_to_notify** | **str** | Email to receive notification about deployment status | [optional] 
**deploy_email_template_name** | **str** | Deploy mail template to receive notification about deployment status on specified mail | [optional] 
**destroy_email_template_name** | **str** | Destroy mail template to receive notification about deployment status on specified mail | [optional] 
**deploy_parent_environments** | **bool** | Flag to deploy parent environment before the current deployment | [optional] 
**max_retries** | **int** |  | [optional] 
**statuses_for_mail** | **list[str]** |  | [optional] 
**parent_deploy_config** | [**DeploymentConfiguration**](DeploymentConfiguration.md) |  | [optional] 
**custom_tag** | [**CustomTag**](CustomTag.md) | Custom tag for environment | [optional] 
**env_version_id** | **int** | The id of the environment in case the user wants to upgrade existing deployment with the newer version of an environment | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



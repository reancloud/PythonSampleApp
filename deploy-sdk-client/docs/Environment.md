# Environment

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**created_by** | **int** | Created By User(Id) | [optional] 
**modified_by** | **int** | Modified By User(Id) | [optional] 
**created_on** | **date** | Created at Date Time | [optional] 
**modified_on** | **date** | Modified at Date Time | [optional] 
**name** | **str** | Unique name of environment | 
**description** | **str** | Description of environment | 
**provider** | [**SaveProvider**](SaveProvider.md) | Default provider to deploy an environment | 
**connection_id** | **int** | Default connection to configure compute resources in an Environment | 
**chef_server_id** | **int** | Chef Server Id (Only when REAN Deploy is configured for Chefserver) | [optional] 
**chef_environment** | **str** | Chef Environment (Only when REAN Deploy is configured for Chefserver) | [optional] 
**region** | **str** | Region into which environment resources should be launched. Defaults to set Provider region if any | [optional] 
**env_version** | **str** | Version of the environment | 
**base_env_id** | **int** | Base version enviroment id | [optional] 
**released** | **bool** | Flag to Release environment | [optional] 
**blueprint_dep_status** | **str** | Blueprint Deployment status | [optional] 
**restart_blueprint** | **bool** | Restart Blueprint Deployment | [optional] 
**status** | **str** |  | [optional] 
**ref_env_id** | **str** | The environment id from which it is copied | [optional] 
**config** | [**EnvConfig**](EnvConfig.md) | Environment Configuration Object | [optional] 
**custom_tag** | [**CustomTag**](CustomTag.md) | Custom tag for environment | [optional] 
**terraform_version** | **str** | Terraform version with environment is created | [optional] 
**public** | **bool** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



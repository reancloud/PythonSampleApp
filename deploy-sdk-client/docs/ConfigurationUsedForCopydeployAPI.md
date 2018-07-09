# ConfigurationUsedForCopydeployAPI

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**original_environment** | **str** | The environment name from which copy should happen | [optional] 
**new_environment** | **str** | The environment name the copy opeartion should create | [optional] 
**new_env_description** | **str** | New environment description | [optional] 
**new_env_connection** | **str** | New environment connection name.Must match one of the names from GET Connection API | [optional] 
**new_env_provider** | **str** | New environment Provider name.Must match one of the names from GET Provider API | [optional] 
**tags** | **str** | Tags or other input variables name and value JSON | [optional] 
**copy_parent_environments** | **bool** | set true if it has to copy the parent environments of the original environment | [optional] 
**depends_on_enviroments** | **str** | key-value pairs of which environment name dependency should be changed to which name | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



# EnvResource

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**name** | **str** | Name of the resource in an environment | 
**resource_name** | **str** | Name of the resource defined by Terraform | 
**connection_id** | **int** | Connection ID | [optional] 
**attributes** | [**list[EnvResourceAttr]**](EnvResourceAttr.md) | Attributes for the resource. Possible attribute name and type for resource should be fetched by resource API | [optional] 
**packages** | [**list[EnvPackage]**](EnvPackage.md) | Packages for the environment resource. Possible package name and package attributes for resource should be fetched by package API | [optional] 
**environment** | [**Environment**](Environment.md) |  | [optional] 
**count** | **str** |  | [optional] 
**depends_on** | **str** | Name of the other resource in same environment which should get deployed before the current resource | [optional] 
**prevent_destroy** | **bool** | Flag for preventing the resource to be destroy | [optional] 
**resource_type** | **str** | Resource type | 
**ignore_changes** | **str** |  | [optional] 
**ref_env_resource_id** | **int** | The resource ID from which this environment resource is copied.It is set only when copy API is used to create current environment | [optional] 
**short_name** | **str** |  | [optional] 
**custom_connection** | **str** | Custom Connection to use for provisioning | [optional] 
**position_x** | **int** | Position X on the canvas to display in UI.Can be set to zero if you want to use only API | [optional] 
**position_y** | **int** | Position Y on the canvas to display in UI.Can be set to zero if you want to use only API | [optional] 
**accept_packages** | **bool** | Not all resources can accept packages. Only a few resources like AWS instance, Null resource can accept packages | [optional] 
**count_support** | **bool** |  | [optional] 
**lifecycle_support** | **bool** |  | [optional] 
**data_source** | **bool** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



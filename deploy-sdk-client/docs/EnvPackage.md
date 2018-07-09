# EnvPackage

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**name** | **str** | Name of the package.Must match the names from Package API/Model | [optional] 
**sequence** | **int** | Order of the package in which it should execute | [optional] 
**ref_package_id** | **int** | Id of Package from which it is copied. It is set only when using copy API | [optional] 
**attributes** | [**list[EnvPackageAttr]**](EnvPackageAttr.md) | Attributes and their values for package. Must match the attributes of package with the name from Package API/Model | [optional] 
**version** | **str** | Version of Package. Must match the version of package with the name from Package API/Model | [optional] 
**type** | **str** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



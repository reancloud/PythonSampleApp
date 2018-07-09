# Package

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**package_name** | **str** | Name of the package | [optional] 
**type** | **str** |  | [optional] 
**package_version** | **str** | Version of the package | [optional] 
**access_token** | **str** | Access token to download package from URL.Required for private repos | [optional] 
**attributes** | [**list[PackageAttribute]**](PackageAttribute.md) |  | [optional] 
**created_by** | **int** | Created By User(Id) | [optional] 
**created_on** | **date** | Created at Date Time | [optional] 
**decrypted_access_token** | **str** |  | [optional] 
**default_package** | **bool** | If package is managed By REAN Cloud | [optional] 
**deleted** | **bool** | Deleted Flag | [optional] 
**dependent_packages** | [**list[Package]**](Package.md) | Dependent Packages | [optional] 
**dependent_packages_set** | **list[str]** | List Dependent Packages names | [optional] 
**description** | **str** | Description of the package | [optional] 
**dn_version** | **str** | REAN Deploy version | [optional] 
**download_url** | **str** | The URL to download the package on provisioning VM | [optional] 
**group_name** | **str** |  | [optional] 
**id** | **int** |  | [optional] 
**modified_by** | **int** | Modified By User(Id) | [optional] 
**modified_on** | **date** | Modified at Date Time | [optional] 
**released** | **bool** | true if package is release | [optional] 
**repo_type** | **str** |  | [optional] 
**sub_type** | **str** | sub type of package | [optional] 
**unzipped_name** | **str** | The folder name in which the package contents are extracted on provisioning VM | [optional] 
**visible** | **bool** | List of Dependent Packages names | [optional] 
**zip_file_name** | **str** | The name with which the download package archive should be saved on provisioning VM | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



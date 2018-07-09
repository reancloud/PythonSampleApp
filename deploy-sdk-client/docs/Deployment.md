# Deployment

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**created_by** | **int** | Created By User(Id) | [optional] 
**modified_by** | **int** | Modified By User(Id) | [optional] 
**created_on** | **date** | Created at Date Time | [optional] 
**modified_on** | **date** | Modified at Date Time | [optional] 
**deployment_name** | **str** | Name of the deployment. Unique for each environment | 
**deployment_description** | **str** | Description of the deployment | [optional] 
**environment** | [**Environment**](Environment.md) |  | [optional] 
**input_json** | **str** | Input variables JSON | [optional] 
**tf_run_id** | **str** | Terraform execution id | [optional] 
**status** | **str** | Status of deployment | [optional] 
**destroy_after_minutes** | **int** | A value in minutes to Automatically destroy deployment after a specified time | [optional] 
**email_to_notify** | **str** | Email to receive notification of deployment status | [optional] 
**deploy_mail_template_name** | **str** | Name of Deploy mail template to receive notification about deployment status on specified mail | [optional] 
**destroy_mail_template_name** | **str** | Name of Destroy mail template to receive notification about deployment status on specified mail | [optional] 
**destroy_failed_mail_template_name** | **str** | Name of failed destroy mail template | [optional] 
**email_for_status** | **str** | Email to receive notification of deployment status | [optional] 
**destroy_token** | **str** |  | [optional] 
**deploy_parent_environments** | **bool** | Flag to deploy Parent environment before the current deployment | [optional] 
**retries_remaining** | **int** |  | [optional] 
**statuses_for_emails** | **str** |  | [optional] 
**connections_map** | **dict(str, str)** | Map of connections where key is the name of resource and value is the name or id of connection | [optional] 
**connections_deploy** | **str** |  | [optional] 
**parent_deployments_map** | **dict(str, str)** | Map of parent deployment where key is a name of \&quot;Depends On\&quot; resource and value is a name/id of the deployment for the parent environment | [optional] 
**parent_deployments** | **str** |  | [optional] 
**provider** | **str** | Provider for deployment | [optional] 
**region** | **str** | Region into which resources should be launched. Defaults to set Provider region if any. | [optional] 
**statuses_for_email_set** | **list[str]** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



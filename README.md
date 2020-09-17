# Deploy an Azure ML model in a local environment

In this example we will show how to use your local environment to deploy an Machine Learning model registered in an Azure ML Workspace as a *local web service*. This scenario is indicated for **limited testing** and **troubleshooting**. 

For more details please see this [link](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-deploy-and-where?tabs=python#choose-a-compute-target) about different deployment scenarios.

---

## Prerequisites

1. Have an Azure Subscription
2. Have a local Docker running
3. Create (or use an existing) Azure Machine Learning Workspace
4. Have a registered model in your Azure ML Workspace
5. Have a [service principal](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-setup-authentication) already configured
6. Have (or build) a `.yml file` with the dependencies (libs required, Python`s version, etc.) in your local environment
7. Have (or build) a `score.py` file to be used as *entry script*. An *Entry Script* is useful to coordinate how your API will load the model when the deployed service starts. This script is also responsible for receiving data, passing it to the model, and then returning a response (see more details in this [link](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-deploy-existing-model#define-inference-configuration))
8. Have Python installed with [`azureml-sdk`](https://pypi.org/project/azureml-sdk/) in your local environment
9. Set the configs from your Azure ML and local environment in the `config/setting.py` (just rename the file `settings.py.example` and change the configs to your own need)
10. Clone this repository in your local environment

### How to run

#### Change `config/setting.py`
After cloning the repo, change the variables in the `config/settings.py` using the following configuration:

`WORKSPACE_NAME`: Your Azure ML Workspace

`WORKSPACE_LOCATION`: The location of your Azure ML Workspace

`RESOURCE_GROUP`: Your Resource Group

`SUBSCRIPTION_ID`: Your Subscription_Id

`TENANT_ID`: Your Tenant Id

`SERVICE_PRINCIPAL_ID`: Your client-id

`SERVICE_PRINCIPAL_PASSWORD`: Your client-secret

`MODEL_NAME`: The model name registered in your Azure ML Workspace

`ENDPOINT_NAME`: The local endpoint name to be generated after the deployment

In this example we will use a `Service Principal` to be able to authenticate on Azure (to get the model). Please check this [link](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-setup-authentication#service-principal-authentication) to see more details about this process. You will set the variables `TENANT_ID`, `SERVICE_PRINCIPAL_ID` and `SERVICE_PRINCIPAL_PASSWORD` with values collected from your service principal.

#### Run `azure-local-deploy.py`

Now we can simply run the script `azure-local-deploy.py` and wait 😆😆😆.

This process will create a new image in a Container Registry (on Azure) and after will pull it to your local environment.

The **local endpoint** will be generated on *http://localhost/PORT* (using the port defined on your `settings.py`).

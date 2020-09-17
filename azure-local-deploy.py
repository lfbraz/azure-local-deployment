import azureml
from azureml.core import Workspace
from azureml.core.authentication import ServicePrincipalAuthentication
from azureml.core.model import Model, InferenceConfig
from azureml.core.environment import Environment, CondaDependencies
from azureml.core.webservice import LocalWebservice
import config.settings as conf

svc_pr = ServicePrincipalAuthentication(
    tenant_id = conf.TENANT_ID,
    service_principal_id = conf.SERVICE_PRINCIPAL_ID,
    service_principal_password = conf.SERVICE_PRINCIPAL_PASSWORD)

workspace = Workspace.create(name=conf.WORKSPACE_NAME,
                             location=conf.WORKSPACE_LOCATION,
                             resource_group=conf.RESOURCE_GROUP,
                             subscription_id=conf.SUBSCRIPTION_ID,
                             auth=svc_pr,
                             exist_ok=True)

# Get the model registered in your Azure ML Workspace
model = Model.list(workspace, conf.MODEL_NAME)[0]

# Create the environment to manage the dependencies
env = Environment(name="env-local-deploy")

# Here we will use a .yml file to control the dependencies
conda_dep = CondaDependencies(conda_dependencies_file_path='conda_env.yml')

# Adds dependencies to PythonSection of myenv
env.python.conda_dependencies=conda_dep

# Our inference config with the score.py file
inference_config = InferenceConfig(entry_script="score.py", environment=env)

# Create a local deployment, using port 8890 for the web service endpoint
deployment_config = LocalWebservice.deploy_configuration(port=conf.PORT)

# Deploy the service
service = Model.deploy(workspace, conf.ENDPOINT_NAME, [model], inference_config, deployment_config)

# Wait for the deployment to complete
service.wait_for_deployment(True)

# Display the port that the web service is available on
print(service.port)

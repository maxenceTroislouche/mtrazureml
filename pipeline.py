from azure.ai.ml import MLClient, load_component
from azure.ai.ml.dsl import pipeline
from azure.identity import DefaultAzureCredential
from azureml.core.environment import Environment

from azure_utils import get_or_create_resource_group, get_or_create_workspace, get_or_create_compute, \
    get_or_create_container_registry

# Configuration
subscription_id = "6c07bf15-eea9-4a31-9510-986d8a14c19c"
resource_group_name = "waldone_pipeline"
workspace_name = "waldone_pipeline"
registry_name = "waldonecontainerregistry"
location = "westeurope"
compute_name = "cpu-cluster"

# 1. Connexion à Azure
credential = DefaultAzureCredential()

# 2. Création du resource_group
resource_client = get_or_create_resource_group(credential, subscription_id, resource_group_name, location)

# 3. Création du client AzureML
ml_client = MLClient(credential, subscription_id, resource_group_name, workspace_name)

# 4. Vérifier ou créer le workspace
workspace = get_or_create_workspace(ml_client, workspace_name, location)

# 5. Vérifier ou créer le compute target
compute_target = get_or_create_compute(ml_client, compute_name)

# 5bis. Vérifier ou créer un container registry
registry = get_or_create_container_registry(credential, subscription_id, resource_group_name, registry_name, location)

# 6. Définir les environnements
env = Environment.from_conda_specification(name="yolo-env", file_path="components/train_yolo/conda_env.yml")

# 7. Charger les composants
train_yolo_component = load_component(source="components/train_yolo/component.yaml")

@pipeline(default_compute=compute_name)
def train_pipeline():
    train_yolo_component()

pipeline_job = train_pipeline()

submitted_job = ml_client.jobs.create_or_update(
    pipeline_job,
    experiment_name="yolo-training-pipeline",
)

from azure.ai.ml.entities import Workspace, AmlCompute
from azure.core.exceptions import ResourceNotFoundError
from azure.mgmt.containerregistry import ContainerRegistryManagementClient
from azure.mgmt.containerregistry.models import Registry, Sku
from azure.mgmt.resource import ResourceManagementClient


def get_or_create_resource_group(credential, subscription_id, resource_group, location):
    resource_client = ResourceManagementClient(credential, subscription_id)
    try:
        rg = resource_client.resource_groups.get(resource_group)
    except ResourceNotFoundError:
        rg = resource_client.resource_groups.create_or_update(
            resource_group,
            {"location": location}
        )

    return rg


def get_or_create_workspace(ml_client, workspace_name, location):
    try:
        workspace = ml_client.workspaces.get(workspace_name)
    except ResourceNotFoundError:
        workspace = Workspace(
            name=workspace_name,
            location=location,
            display_name=f"{workspace_name}-workspace",
            description=f"{workspace_name}"
        )
        workspace = ml_client.workspaces.begin_create(workspace).result()

    return workspace


def get_or_create_compute(ml_client, compute_name):
    try:
        compute_target = ml_client.compute.get(compute_name)
    except ResourceNotFoundError:
        compute_target = AmlCompute(
            name=compute_name,
            size="Standard_DS11_v2",
            min_instances=0,
            max_instances=2,
            idle_time_before_scale_down=120
        )
        compute_target = ml_client.compute.begin_create_or_update(compute_target).result()

    return compute_target


def get_or_create_container_registry(credential, subscription_id, resource_group_name, registry_name, location):
    acr_client = ContainerRegistryManagementClient(credential, subscription_id)

    try:
        return acr_client.registries.get(resource_group_name, registry_name)
    except ResourceNotFoundError:
        registry_params = Registry(
            location=location,
            sku=Sku(name="Basic"),
            admin_user_enabled=True
        )
        registry = acr_client.registries.begin_create(resource_group_name, registry_name, registry_params).result()
        return registry

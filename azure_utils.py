from azure.ai.ml.entities import Workspace, AmlCompute
from azure.core.exceptions import ResourceNotFoundError
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

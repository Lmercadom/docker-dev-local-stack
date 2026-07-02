from aws_cdk import (
    Stack,
    CfnOutput,
    aws_apprunner as apprunner,
    aws_ecr_assets as ecr_assets,
    aws_iam as iam,
)
from constructs import Construct


class AppRunnerStack(Stack):
    """
    Builds the Docker image from a local project folder, pushes it to ECR
    (both handled automatically by DockerImageAsset), then deploys it to
    App Runner as a public HTTPS service.
    """

    def __init__(self, scope: Construct, construct_id: str, project_path: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Builds the image from project_path's Dockerfile and pushes to a
        # CDK-managed ECR repo. Re-running `cdk deploy` after a code change
        # rebuilds and pushes automatically -- no manual docker/ECR commands.
        image_asset = ecr_assets.DockerImageAsset(
            self, "ServiceImage",
            directory=project_path,
        )

        # App Runner needs permission to pull the image from ECR.
        access_role = iam.Role(
            self, "AppRunnerECRAccessRole",
            assumed_by=iam.ServicePrincipal("build.apprunner.amazonaws.com"),
        )
        image_asset.repository.grant_pull(access_role)

        service = apprunner.CfnService(
            self, "Service",
            source_configuration=apprunner.CfnService.SourceConfigurationProperty(
                auto_deployments_enabled=False,
                authentication_configuration=apprunner.CfnService.AuthenticationConfigurationProperty(
                    access_role_arn=access_role.role_arn,
                ),
                image_repository=apprunner.CfnService.ImageRepositoryProperty(
                    image_identifier=image_asset.image_uri,
                    image_repository_type="ECR",
                    image_configuration=apprunner.CfnService.ImageConfigurationProperty(
                        port="8000",
                    ),
                ),
            ),
            instance_configuration=apprunner.CfnService.InstanceConfigurationProperty(
                # Smallest available size -- keeps cost down for a demo service.
                cpu="0.25 vCPU",
                memory="0.5 GB",
            ),
            health_check_configuration=apprunner.CfnService.HealthCheckConfigurationProperty(
                protocol="HTTP",
                path="/health",
                interval=10,
                timeout=5,
            ),
        )

        CfnOutput(
            self, "ServiceUrl",
            value=f"https://{service.attr_service_url}",
            description="Public URL of the deployed service",
        )
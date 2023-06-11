#!/usr/bin/env python3
import os

import aws_cdk as cdk
import aws_cdk.aws_rds as rds 
import aws_cdk.aws_ecs as ecs
from cdk_keycloak import KeyCloak, KeycloakVersion
from aws_cdk import CfnOutput

app = cdk.App()
env = cdk.Environment(region="us-east-1", account="314374386591")

stack = cdk.Stack(app, "keycloakauth", env=env)

mysso = KeyCloak(stack, "KeyCloak",
    certificate_arn="arn:aws:acm:us-east-1:314374386591:certificate/0b723b8c-7d16-40cf-9bcb-3e1e1cc17f49",
    keycloak_version=KeycloakVersion.V21_0_1,
    cluster_engine = rds.DatabaseClusterEngine.aurora_mysql(version=rds.AuroraMysqlEngineVersion.VER_2_11_2),
    hostname = "keycloak.mysmartpay.com.ng",
    env = { "KEYCLOAK_FRONTEND_URL" : "keycloak.mysmartpay.com.ng"},
    container_image = ecs.ContainerImage.from_registry("314374386591.dkr.ecr.us-east-1.amazonaws.com/keycloak:21.1.1-amd64"),
    database_removal_policy=cdk.RemovalPolicy.DESTROY
)

CfnOutput(
            stack,
            id="KeyCloakSecret",
            value=mysso.keycloak_secret.secret_full_arn,
            description="Keycloak admin username and password"
        )
app.synth()
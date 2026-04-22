from jarvis_v5.integration_plane.adapters.node_express import NodeExpressAdapter
from jarvis_v5.integration_plane.adapters.python_fastapi import PythonFastAPIAdapter
from jarvis_v5.integration_plane.adapters.cloudflare import CloudflareAdapter
from jarvis_v5.integration_plane.adapters.aws_eb import AwsElasticBeanstalkAdapter
from jarvis_v5.integration_plane.adapters.docker_runtime import DockerAdapter
from jarvis_v5.integration_plane.adapters.generic import GenericAdapter


class AdapterRouter:
    def for_project(self, project: dict):
        stack = project.get("stack", "")
        if stack == "node_express":
            return NodeExpressAdapter()
        if stack == "python_fastapi":
            return PythonFastAPIAdapter()
        if stack == "cloudflare_pages":
            return CloudflareAdapter()
        if stack == "aws_elastic_beanstalk":
            return AwsElasticBeanstalkAdapter()
        if stack == "docker_runtime":
            return DockerAdapter()
        return GenericAdapter()

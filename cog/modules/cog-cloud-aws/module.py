from cog.cog_module import CogModule
from cog.tools.base import Tool, ToolResult
from cog.verification.base import Verifier, VerificationResult, VerificationStatus


class AWSS3ListTool(Tool):
    name = "aws.s3.list"
    description = "List AWS S3 buckets or objects"
    required_permissions = ["shell.execute"]

    def execute(self, bucket: str = "", prefix: str = "", **kwargs) -> ToolResult:
        from cog.tools.shell import ShellTool

        shell = ShellTool()
        if bucket:
            command = f"aws s3 ls s3://{bucket}/{prefix} --recursive"
        else:
            command = "aws s3 ls"
        result = shell.execute(command=command, timeout=60)
        return result


class AWSS3UploadTool(Tool):
    name = "aws.s3.upload"
    description = "Upload file to AWS S3"
    required_permissions = ["shell.execute", "filesystem.read"]

    def execute(self, file_path: str, bucket: str, key: str = "", **kwargs) -> ToolResult:
        from cog.tools.shell import ShellTool

        shell = ShellTool()
        s3_path = f"s3://{bucket}/{key}" if key else f"s3://{bucket}/"
        command = f"aws s3 cp {file_path} {s3_path}"
        result = shell.execute(command=command, timeout=300)
        return result


class AWSS3DownloadTool(Tool):
    name = "aws.s3.download"
    description = "Download file from AWS S3"
    required_permissions = ["shell.execute", "filesystem.write"]

    def execute(self, bucket: str, key: str, file_path: str = "", **kwargs) -> ToolResult:
        from cog.tools.shell import ShellTool

        shell = ShellTool()
        s3_path = f"s3://{bucket}/{key}"
        local_path = file_path or key.split("/")[-1]
        command = f"aws s3 cp {s3_path} {local_path}"
        result = shell.execute(command=command, timeout=300)
        return result


class AWSEC2ListTool(Tool):
    name = "aws.ec2.list"
    description = "List AWS EC2 instances"
    required_permissions = ["shell.execute"]

    def execute(self, region: str = "us-east-1", **kwargs) -> ToolResult:
        from cog.tools.shell import ShellTool

        shell = ShellTool()
        command = f"aws ec2 describe-instances --region {region}"
        result = shell.execute(command=command, timeout=60)
        return result


class AWSEC2StartTool(Tool):
    name = "aws.ec2.start"
    description = "Start AWS EC2 instance"
    required_permissions = ["shell.execute"]

    def execute(self, instance_id: str, region: str = "us-east-1", **kwargs) -> ToolResult:
        from cog.tools.shell import ShellTool

        shell = ShellTool()
        command = f"aws ec2 start-instances --instance-ids {instance_id} --region {region}"
        result = shell.execute(command=command, timeout=60)
        return result


class AWSEC2StopTool(Tool):
    name = "aws.ec2.stop"
    description = "Stop AWS EC2 instance"
    required_permissions = ["shell.execute"]

    def execute(self, instance_id: str, region: str = "us-east-1", **kwargs) -> ToolResult:
        from cog.tools.shell import ShellTool

        shell = ShellTool()
        command = f"aws ec2 stop-instances --instance-ids {instance_id} --region {region}"
        result = shell.execute(command=command, timeout=60)
        return result


class AWSLambdaInvokeTool(Tool):
    name = "aws.lambda.invoke"
    description = "Invoke AWS Lambda function"
    required_permissions = ["shell.execute"]

    def execute(self, function_name: str, payload: str = "{}", region: str = "us-east-1", **kwargs) -> ToolResult:
        from cog.tools.shell import ShellTool

        shell = ShellTool()
        command = f'aws lambda invoke --function-name {function_name} --region {region} --payload "{payload}" response.json'
        result = shell.execute(command=command, timeout=60)
        return result


class AWSConnectivityVerifier(Verifier):
    name = "aws.connectivity"
    description = "Verify AWS CLI connectivity and credentials"

    def verify(self, target, **kwargs) -> VerificationResult:
        from cog.tools.shell import ShellTool

        shell = ShellTool()
        command = "aws sts get-caller-identity"

        result = shell.execute(command=command, timeout=10)
        if result.success:
            return VerificationResult(
                verifier=self.name,
                status=VerificationStatus.PASSED,
                message="AWS connectivity OK - credentials valid",
                details={"output": result.output},
            )
        return VerificationResult(
            verifier=self.name,
            status=VerificationStatus.FAILED,
            message="AWS connectivity failed - check credentials",
            details={"error": result.error},
        )


class CogCloudAws(CogModule):
    name = "cog-cloud-aws"
    version = "1.0.0"
    description = "Amazon Web Services operations module"

    def register_tools(self) -> list[Tool]:
        return [
            AWSS3ListTool(),
            AWSS3UploadTool(),
            AWSS3DownloadTool(),
            AWSEC2ListTool(),
            AWSEC2StartTool(),
            AWSEC2StopTool(),
            AWSLambdaInvokeTool(),
        ]

    def register_verifiers(self) -> list[Verifier]:
        return [AWSConnectivityVerifier()]

    def get_prompt_extensions(self) -> list[str]:
        return [
            "## AWS Cloud Expertise",
            "You understand Amazon Web Services including:",
            "- S3 storage and buckets",
            "- EC2 compute instances",
            "- Lambda serverless functions",
            "- IAM roles and permissions",
            "- CloudFormation templates",
            "- AWS CLI commands",
            "- Security best practices",
            "- Cost optimization",
            "",
            "When working with AWS:",
            "- Always check region settings",
            "- Use IAM roles instead of access keys when possible",
            "- Verify permissions before operations",
            "- Monitor costs and resource usage",
            "- Use tags for resource organization",
            "- Enable logging and monitoring",
        ]

    def get_capabilities(self) -> list[str]:
        return [
            "s3_operations",
            "ec2_management",
            "lambda_functions",
            "cloudformation",
            "iam_management",
            "aws_monitoring",
            "cost_optimization",
        ]


module = CogCloudAws()

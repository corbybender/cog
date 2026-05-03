from cog.cog_module import CogModule
from cog.tools.base import Tool, ToolResult
from cog.verification.base import Verifier, VerificationResult, VerificationStatus


class PostgresQueryTool(Tool):
    name = "postgres.query"
    description = "Execute PostgreSQL query"
    required_permissions = ["shell.execute"]

    def execute(
        self,
        database: str,
        query: str,
        host: str = "localhost",
        port: int = 5432,
        user: str = "postgres",
        **kwargs
    ) -> ToolResult:
        from cog.tools.shell import ShellTool

        shell = ShellTool()
        # Use psql to execute query
        command = f'PGPASSWORD={kwargs.get("password", "")} psql -h {host} -p {port} -U {user} -d {database} -c "{query}"'
        result = shell.execute(command=command, timeout=60)
        return result


class PostgresDumpTool(Tool):
    name = "postgres.dump"
    description = "Dump PostgreSQL database to file"
    required_permissions = ["shell.execute", "filesystem.write"]

    def execute(
        self,
        database: str,
        output_file: str,
        host: str = "localhost",
        port: int = 5432,
        user: str = "postgres",
        **kwargs
    ) -> ToolResult:
        from cog.tools.shell import ShellTool

        shell = ShellTool()
        command = f'PGPASSWORD={kwargs.get("password", "")} pg_dump -h {host} -p {port} -U {user} -f {output_file} {database}'
        result = shell.execute(command=command, timeout=600)
        return result


class PostgresRestoreTool(Tool):
    name = "postgres.restore"
    description = "Restore PostgreSQL database from file"
    required_permissions = ["shell.execute", "filesystem.read"]

    def execute(
        self,
        database: str,
        input_file: str,
        host: str = "localhost",
        port: int = 5432,
        user: str = "postgres",
        **kwargs
    ) -> ToolResult:
        from cog.tools.shell import ShellTool

        shell = ShellTool()
        command = f'PGPASSWORD={kwargs.get("password", "")} psql -h {host} -p {port} -U {user} -d {database} -f {input_file}'
        result = shell.execute(command=command, timeout=600)
        return result


class PostgresSchemaTool(Tool):
    name = "postgres.schema"
    description = "Analyze PostgreSQL database schema"
    required_permissions = ["shell.execute"]

    def execute(
        self,
        database: str,
        host: str = "localhost",
        port: int = 5432,
        user: str = "postgres",
        **kwargs
    ) -> ToolResult:
        from cog.tools.shell import ShellTool

        shell = ShellTool()
        # Query schema information
        query = """
        SELECT
            table_name,
            column_name,
            data_type,
            is_nullable,
            column_default
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY table_name, ordinal_position;
        """
        command = f'PGPASSWORD={kwargs.get("password", "")} psql -h {host} -p {port} -U {user} -d {database} -c "{query}"'
        result = shell.execute(command=command, timeout=60)
        return result


class PostgresConnectivityVerifier(Verifier):
    name = "postgres.connectivity"
    description = "Verify PostgreSQL database connectivity"

    def verify(self, target, **kwargs) -> VerificationResult:
        from cog.tools.shell import ShellTool

        shell = ShellTool()
        # Try to connect using psql
        command = f'PGPASSWORD={kwargs.get("password", "")} psql -h {kwargs.get("host", "localhost")} -p {kwargs.get("port", 5432)} -U {kwargs.get("user", "postgres")} -d {target} -c "SELECT 1;"'

        result = shell.execute(command=command, timeout=10)
        if result.success:
            return VerificationResult(
                verifier=self.name,
                status=VerificationStatus.PASSED,
                message=f"PostgreSQL connectivity OK: {target}",
            )
        return VerificationResult(
            verifier=self.name,
            status=VerificationStatus.FAILED,
            message=f"Cannot connect to PostgreSQL: {target}",
            details={"error": result.error},
        )


class CogDbPostgres(CogModule):
    name = "cog-db-postgres"
    version = "1.0.0"
    description = "PostgreSQL database operations module"

    def register_tools(self) -> list[Tool]:
        return [
            PostgresQueryTool(),
            PostgresDumpTool(),
            PostgresRestoreTool(),
            PostgresSchemaTool(),
        ]

    def register_verifiers(self) -> list[Verifier]:
        return [PostgresConnectivityVerifier()]

    def get_prompt_extensions(self) -> list[str]:
        return [
            "## PostgreSQL Expertise",
            "You understand PostgreSQL databases including:",
            "- SQL queries and optimization",
            "- Database schema design",
            "- Indexes and constraints",
            "- Transactions and ACID properties",
            "- Backup and restore procedures",
            "- Database migration strategies",
            "- Performance tuning",
            "- Connection management",
            "",
            "When working with PostgreSQL:",
            "- Use parameterized queries to prevent SQL injection",
            "- Wrap multi-step operations in transactions",
            "- Consider indexes for query optimization",
            "- Use EXPLAIN ANALYZE for performance analysis",
            "- Always backup before schema changes",
        ]

    def get_capabilities(self) -> list[str]:
        return [
            "query_postgres",
            "schema_analysis",
            "data_migration",
            "backup_restore",
            "performance_tuning",
            "sql_optimization",
        ]


module = CogDbPostgres()

from cog.cog_module import CogModule


class CodeCoreModule(CogModule):
    name = "code-core"
    version = "1.0.0"
    description = "Core programming abstractions and code understanding foundations"

    def get_capabilities(self) -> list[str]:
        return ["parse_code", "understand_ast", "code_structure", "dependency_analysis"]

    def get_prompt_extensions(self) -> list[str]:
        return [
            "## Code Core Foundations",
            "You understand programming fundamentals including:",
            "- Abstract Syntax Trees (AST) and code structure",
            "- Dependency analysis and import graphs",
            "- Code patterns and idioms across languages",
            "- Type systems and static analysis concepts",
            "- Build systems and compilation pipelines",
            "- Testing frameworks and test organization",
            "- Code quality metrics and technical debt",
            "",
            "When analyzing code, consider structure, dependencies, patterns, and quality."
        ]


module = CodeCoreModule()

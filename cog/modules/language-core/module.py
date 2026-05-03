from cog.cog_module import CogModule


class LanguageCoreModule(CogModule):
    name = "language-core"
    version = "1.0.0"
    description = "Core language understanding and parsing foundations"

    def get_capabilities(self) -> list[str]:
        return ["grammar_understanding", "syntax_parsing", "semantic_analysis", "tokenization"]

    def get_prompt_extensions(self) -> list[str]:
        return [
            "## Language Core Foundations",
            "You understand language fundamentals including:",
            "- Grammar and syntax structure across languages",
            "- Tokenization and lexical analysis",
            "- Semantic meaning and context",
            "- Natural language patterns and idioms",
            "- Text processing and string manipulation",
            "- Regular expressions and pattern matching",
            "- Language detection and encoding",
            "",
            "When processing language text, consider grammar, semantics, and context."
        ]


module = LanguageCoreModule()

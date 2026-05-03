from cog.cog_module import CogModule
from cog.tools.base import Tool, ToolResult
from cog.verification.base import Verifier, VerificationResult, VerificationStatus


class TailwindBuildTool(Tool):
    name = "tailwind.build"
    description = "Build Tailwind CSS"
    required_permissions = ["shell.execute"]

    def execute(self, path: str = ".", **kwargs) -> ToolResult:
        from cog.tools.shell import ShellTool

        shell = ShellTool()
        command = f"cd {path} && npx tailwindcss -i ./src/input.css -o ./dist/output.css"
        result = shell.execute(command=command, timeout=60)
        return result


class TailwindWatchTool(Tool):
    name = "tailwind.watch"
    description = "Watch Tailwind CSS for changes"
    required_permissions = ["shell.execute"]

    def execute(self, path: str = ".", **kwargs) -> ToolResult:
        from cog.tools.shell import ShellTool

        shell = ShellTool()
        command = f"cd {path} && npx tailwindcss -i ./src/input.css -o ./dist/output.css --watch"
        result = shell.execute(command=command, timeout=300)
        return result


class BootstrapInstallTool(Tool):
    name = "bootstrap.install"
    description = "Install Bootstrap"
    required_permissions = ["shell.execute"]

    def execute(self, version: str = "5.3", **kwargs) -> ToolResult:
        from cog.tools.shell import ShellTool

        shell = ShellTool()
        command = f"npm install bootstrap@{version}"
        result = shell.execute(command=command, timeout=120)
        return result


class CSSTool(Tool):
    name = "css.optimize"
    description = "Optimize and minify CSS"
    required_permissions = ["shell.execute"]

    def execute(self, input_file: str, output_file: str = "", **kwargs) -> ToolResult:
        from cog.tools.shell import ShellTool

        shell = ShellTool()
        output = output_file or input_file.replace('.css', '.min.css')
        command = f"csso {input_file} {output} --output {output}"
        result = shell.execute(command=command, timeout=30)
        return result


class CSSSyntaxVerifier(Verifier):
    name = "css.syntax"
    description = "Verify CSS syntax is valid"

    def verify(self, target, **kwargs) -> VerificationResult:
        from cog.tools.shell import ShellTool

        shell = ShellTool()
        # Use stylelint to verify CSS
        result = shell.execute(
            command=f"stylelint '{target}' --syntax css", timeout=30
        )
        if result.success:
            return VerificationResult(
                verifier=self.name,
                status=VerificationStatus.PASSED,
                message=f"CSS syntax OK: {target}",
            )
        return VerificationResult(
            verifier=self.name,
            status=VerificationStatus.FAILED,
            message=f"CSS syntax error in {target}",
            details={"error": result.error},
        )


class CogWebCSS(CogModule):
    name = "cog-web-css"
    version = "1.0.0"
    description = "CSS expertise including Tailwind, Bootstrap, and pure CSS"

    def register_tools(self) -> list[Tool]:
        return [
            TailwindBuildTool(),
            TailwindWatchTool(),
            BootstrapInstallTool(),
            CSSTool(),
        ]

    def register_verifiers(self) -> list[Verifier]:
        return [CSSSyntaxVerifier()]

    def get_prompt_extensions(self) -> list[str]:
        return [
            "## CSS Expertise",
            "",
            "### Pure CSS",
            "You understand CSS3 including:",
            "- Selectors and specificity",
            "- Box model and layout",
            "- Flexbox and Grid",
            "- Responsive design with media queries",
            "- CSS animations and transitions",
            "- Custom properties (CSS variables)",
            "- Modern layout techniques",
            "",
            "### Tailwind CSS",
            "You understand Tailwind CSS including:",
            "- Utility-first CSS framework",
            "- Responsive breakpoints (sm, md, lg, xl, 2xl)",
            "- State variants (hover, focus, active, etc.)",
            "- Dark mode implementation",
            "- Custom configuration in tailwind.config.js",
            "- JIT mode and performance",
            "- Plugin system",
            "- Common utility patterns",
            "",
            "When working with Tailwind:",
            "- Use utility classes for rapid development",
            "- Extract components with @apply when appropriate",
            "- Configure theme in tailwind.config.js",
            "- Use responsive prefixes (md:, lg:, etc.)",
            "- Leverage state variants (hover:, focus:, etc.)",
            "- Use @screen for custom breakpoints",
            "",
            "### Bootstrap CSS",
            "You understand Bootstrap including:",
            "- Grid system and containers",
            "- Pre-built components (buttons, cards, modals)",
            "- Utility classes",
            "- Responsive breakpoints",
            "- Theme customization via SCSS",
            "- Bootstrap Icons",
            "- JavaScript components",
            "",
            "When working with Bootstrap:",
            "- Use container classes for layout",
            "- Leverage grid system (row, col)",
            "- Use pre-built components when possible",
            "- Customize via CSS variables (Bootstrap 5+)",
            "- Override defaults with custom CSS",
            "",
            "### Best Practices",
            "",
            "When writing CSS:",
            "- Use mobile-first responsive design",
            "- Organize CSS with BEM or other methodology",
            "- Minimize specificity conflicts",
            "- Use CSS Grid for 2D layouts",
            "- Use Flexbox for 1D layouts",
            "- Optimize with CSS custom properties",
            "- Consider performance (avoid deep nesting)",
            "",
            "When choosing frameworks:",
            "- Use Tailwind for rapid UI development",
            "- Use Bootstrap for quick prototypes",
            "- Use pure CSS for complete control",
            "- Can combine approaches (Tailwind + custom CSS)",
            "",
            "### Common Patterns",
            "",
            "Responsive navigation:",
            "- Mobile: Hamburger menu",
            "- Desktop: Horizontal nav",
            "- Use media queries or Tailwind breakpoints",
            "",
            "Layouts:",
            "- CSS Grid: Overall page structure",
            "- Flexbox: Component internal layout",
            "- Container queries: Component-based responsiveness",
            "",
            "Performance:",
            "- Minimize CSS file size",
            "- Use critical CSS for above-the-fold",
            "- Lazy load CSS when appropriate",
            "- Purge unused CSS (Tailwind JIT)",
        ]

    def get_capabilities(self) -> list[str]:
        return [
            "read_css",
            "write_css",
            "optimize_css",
            "tailwind_css",
            "tailwind_config",
            "bootstrap_css",
            "responsive_design",
            "css_animations",
            "css_grid",
            "flexbox",
            "css_variables",
            "media_queries",
        ]


module = CogWebCSS()

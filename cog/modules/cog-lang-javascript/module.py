from cog.cog_module import CogModule
from cog.tools.base import Tool, ToolResult
from cog.verification.base import Verifier, VerificationResult, VerificationStatus


class NPMInstallTool(Tool):
    name = "npm.install"
    description = "Install npm packages"
    required_permissions = ["shell.execute"]

    def execute(self, packages: str, save: bool = True, **kwargs) -> ToolResult:
        from cog.tools.shell import ShellTool

        shell = ShellTool()
        save_flag = "--save" if save else ""
        command = f"npm install {save_flag} {packages}"
        result = shell.execute(command=command, timeout=300)
        return result


class NPMBuildTool(Tool):
    name = "npm.build"
    description = "Build npm project"
    required_permissions = ["shell.execute"]

    def execute(self, path: str = ".", **kwargs) -> ToolResult:
        from cog.tools.shell import ShellTool

        shell = ShellTool()
        command = f"cd {path} && npm run build"
        result = shell.execute(command=command, timeout=300)
        return result


class WebpackBuildTool(Tool):
    name = "webpack.build"
    description = "Build with Webpack"
    required_permissions = ["shell.execute"]

    def execute(self, config: str = "webpack.config.js", **kwargs) -> ToolResult:
        from cog.tools.shell import ShellTool

        shell = ShellTool()
        command = f"npx webpack --config {config}"
        result = shell.execute(command=command, timeout=180)
        return result


class ViteDevTool(Tool):
    name = "vite.dev"
    description = "Start Vite development server"
    required_permissions = ["shell.execute"]

    def execute(self, path: str = ".", **kwargs) -> ToolResult:
        from cog.tools.shell import ShellTool

        shell = ShellTool()
        command = f"cd {path} && npm run dev"
        result = shell.execute(command=command, timeout=60)
        return result


class JSLintTool(Tool):
    name = "javascript.lint"
    description = "Lint JavaScript code"
    required_permissions = ["shell.execute"]

    def execute(self, path: str = ".", fix: bool = False, **kwargs) -> ToolResult:
        from cog.tools.shell import ShellTool

        shell = ShellTool()
        tool = "eslint" if not fix else "eslint --fix"
        command = f"{tool} {path}"
        result = shell.execute(command=command, timeout=60)
        return result


class JSTestTool(Tool):
    name = "javascript.test"
    description = "Run JavaScript tests"
    required_permissions = ["shell.execute"]

    def execute(self, path: str = ".", watch: bool = False, **kwargs) -> ToolResult:
        from cog.tools.shell import ShellTool

        shell = ShellTool()
        watch_flag = "--watch" if watch else ""
        command = f"cd {path} && npm test {watch_flag}"
        result = shell.execute(command=command, timeout=180)
        return result


class JavaScriptSyntaxVerifier(Verifier):
    name = "javascript.syntax"
    description = "Verify JavaScript/TypeScript syntax"

    def verify(self, target, **kwargs) -> VerificationResult:
        from cog.tools.shell import ShellTool

        shell = ShellTool()
        # Use eslint to verify syntax
        result = shell.execute(
            command=f"eslint '{target}' --no-eslintrc --parser @babel/eslint-parser --parser-options=sourceType:module", timeout=30
        )
        if result.success or "syntax error" not in (result.error or "").lower():
            return VerificationResult(
                verifier=self.name,
                status=VerificationStatus.PASSED,
                message=f"JavaScript syntax OK: {target}",
            )
        return VerificationResult(
            verifier=self.name,
            status=VerificationStatus.FAILED,
            message=f"JavaScript syntax error in {target}",
            details={"error": result.error},
        )


class CogLangJavaScript(CogModule):
    name = "cog-lang-javascript"
    version = "1.0.0"
    description = "Complete JavaScript expertise"

    def register_tools(self) -> list[Tool]:
        return [
            NPMInstallTool(),
            NPMBuildTool(),
            WebpackBuildTool(),
            ViteDevTool(),
            JSLintTool(),
            JSTestTool(),
        ]

    def register_verifiers(self) -> list[Verifier]:
        return [JavaScriptSyntaxVerifier()]

    def get_prompt_extensions(self) -> list[str]:
        return [
            "## JavaScript Expertise",
            "",
            "### Vanilla JavaScript (ES6+)",
            "You understand modern JavaScript including:",
            "- ES6+ features (arrow functions, destructuring, spread, rest)",
            "- Async/await and Promises",
            "- Modules (import/export)",
            "- Classes and prototypes",
            "- Closures and scope",
            "- Event loop and callbacks",
            "- DOM manipulation",
            "- Fetch API and async operations",
            "- Error handling (try/catch, error boundaries)",
            "- Array methods (map, filter, reduce, etc.)",
            "- Template literals",
            "- Destructuring assignments",
            "- Spread and rest operators",
            "- Optional chaining and nullish coalescing",
            "",
            "### jQuery",
            "You understand jQuery including:",
            "- DOM selection and manipulation",
            "- Event handling",
            "- AJAX and API calls",
            "- Animation and effects",
            "- Plugins and extensibility",
            "- Chaining methods",
            "- Common jQuery patterns",
            "",
            "### React",
            "You understand React including:",
            "- Components and props",
            "- State management (useState, useReducer)",
            "- Hooks (useEffect, useContext, useMemo, useCallback)",
            "- Context API for global state",
            "- Virtual DOM and reconciliation",
            "- JSX syntax",
            "- Event handling",
            "- Forms and controlled components",
            "- Routing (React Router)",
            "- State management libraries (Redux, Zustand)",
            "- Performance optimization",
            "- Server Components (Next.js)",
            "- Testing with Jest and React Testing Library",
            "",
            "### Vue.js",
            "You understand Vue.js including:",
            "- Options API and Composition API",
            "- Template syntax and directives",
            "- Reactivity system",
            "- Components and props",
            "- Event handling",
            "- Composables",
            "- Vue Router",
            "- Pinia for state management",
            "- Teleport and Suspense",
            "- Script setup syntax",
            "",
            "### Angular",
            "You understand Angular including:",
            "- TypeScript-based development",
            "- Components and templates",
            "- Services and dependency injection",
            "- RxJS observables",
            "- Routing (Angular Router)",
            "- Forms (template-driven and reactive)",
            "- HTTP client",
            "- Pipes and directives",
            "- Modules and lazy loading",
            "- Testing with Jasmine/Karma",
            "",
            "### Svelte",
            "You understand Svelte including:",
            "- Component syntax",
            "- Reactivity declarations",
            "- Props and events",
            "- Stores (writable, derived)",
            "- SvelteKit for full-stack apps",
            "- Actions and forms",
            "- Transitions and animations",
            "- Server-side rendering",
            "- No virtual DOM - compilation-based",
            "",
            "### Node.js",
            "You understand Node.js including:",
            "- CommonJS and ES modules",
            "- npm package management",
            "- Express.js for web servers",
            "- Middleware and routing",
            "- File system operations",
            "- Streams and buffers",
            "- Event-driven architecture",
            "- REST APIs",
            "- WebSocket servers",
            "- Worker threads",
            "- Package.json scripts",
            "",
            "### TypeScript Integration",
            "You understand TypeScript with JavaScript including:",
            "- Type annotations and interfaces",
            "- Generics",
            "- Union types and type guards",
            "- Utility types",
            "- Declaration files",
            "- tsconfig.json",
            "- Type checking with tsc",
            "- JSDoc comments",
            "",
            "### Build Tools",
            "You understand JavaScript build tools including:",
            "- Webpack (module bundling, code splitting)",
            "- Vite (fast dev server, optimized builds)",
            "- Rollup (tree-shaking)",
            "- esbuild (ultra-fast transpilation)",
            "- Babel (JavaScript transpilation)",
            "- PostCSS (CSS transformations)",
            "",
            "### Package Managers",
            "You understand JavaScript package management:",
            "- npm (Node Package Manager)",
            "- yarn (alternative to npm)",
            "- pnpm (fast, disk space efficient)",
            "- npx (package runner)",
            "- package.json",
            "- Semantic versioning",
            "- Dependency management",
            "- Scripts and lifecycle hooks",
            "",
            "### Testing",
            "You understand JavaScript testing including:",
            "- Jest (testing framework)",
            "- React Testing Library",
            "- Vitest (Vite-native testing)",
            "- Playwright (end-to-end testing)",
            "- Cypress (E2E testing)",
            "- Mocha/Chai",
            "- Testing practices (TDD, BDD)",
            "- Mocking and stubbing",
            "- Test doubles",
            "",
            "### Best Practices",
            "",
            "When writing JavaScript:",
            "- Use const/let, avoid var",
            "- Use arrow functions for callbacks",
            "- Destructure objects and arrays",
            "- Use template literals",
            "- Handle async with async/await",
            "- Use modules (import/export)",
            "- Error boundaries in React",
            "- Clean code principles",
            "- Performance optimization",
            "- Accessibility considerations",
            "",
            "When choosing frameworks:",
            "- React: Large apps, rich ecosystem",
            "- Vue: Progressive, easy learning curve",
            "- Svelte: Performance and simplicity",
            "- Angular: Enterprise, opinionated",
            "- Vanilla JS: Simple apps, no build step",
            "",
            "### Modern Patterns",
            "",
            "State management:",
            "- React: useState, useReducer, Context, Zustand",
            "- Vue: ref, reactive, computed, Pinia",
            "- Svelte: writable, derived, stores",
            "",
            "Routing:",
            "- React Router (React)",
            "- Vue Router (Vue)",
            "- Angular Router (Angular)",
            "",
            "API calls:",
            "- Fetch API (vanilla)",
            "- Axios (popular library)",
            "- React Query (React)",
            "- SWR (React)",
            "",
            "### Common Issues",
            "",
            "Performance:",
            "- Memoization (useMemo, useCallback)",
            "- Code splitting (lazy loading)",
            "- Virtualization for long lists",
            "- Debouncing and throttling",
            "",
            "Memory leaks:",
            "- Cleanup event listeners",
            "- Clear intervals and timeouts",
            "- Cleanup subscriptions",
            "- Unmount components properly",
            "",
            "Debugging:",
            "- Use browser DevTools",
            "- React DevTools",
            "- Vue DevTools",
            "- Angular DevTools",
            "- Console logging strategies",
            "- Source maps",
        ]

    def get_capabilities(self) -> list[str]:
        return [
            "vanilla_javascript",
            "es6_plus",
            "jquery",
            "react",
            "vue",
            "angular",
            "svelte",
            "nodejs",
            "typescript_integration",
            "npm_yarn_pnpm",
            "webpack_vite_rollup",
            "javascript_testing",
            "rest_apis",
            "graphql_apis",
            "websocket_servers",
            "javascript_optimization",
        ]


module = CogLangJavaScript()

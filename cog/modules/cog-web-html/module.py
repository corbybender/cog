from cog.cog_module import CogModule
from cog.tools.base import Tool, ToolResult
from cog.verification.base import Verifier, VerificationResult, VerificationStatus


class HTMLValidateTool(Tool):
    name = "html.validate"
    description = "Validate HTML syntax and structure"
    required_permissions = ["shell.execute"]

    def execute(self, file_path: str, **kwargs) -> ToolResult:
        from cog.tools.shell import ShellTool

        shell = ShellTool()
        # Use HTML Tidy or vnu jar for validation
        command = f"tidy -eq -errors '{file_path}'"
        result = shell.execute(command=command, timeout=30)
        return result


class HTMLFormatTool(Tool):
    name = "html.format"
    description = "Format and beautify HTML"
    required_permissions = ["shell.execute", "filesystem.write"]

    def execute(self, file_path: str, **kwargs) -> ToolResult:
        from cog.tools.shell import ShellTool

        shell = ShellTool()
        command = f"tidy -m -i '{file_path}'"
        result = shell.execute(command=command, timeout=30)
        return result


class HTMLMinifyTool(Tool):
    name = "html.minify"
    description = "Minify HTML for production"
    required_permissions = ["shell.execute", "filesystem.write"]

    def execute(self, file_path: str, output: str = "", **kwargs) -> ToolResult:
        from cog.tools.shell import ShellTool

        shell = ShellTool()
        out = output or file_path.replace('.html', '.min.html')
        command = f"html-minifier-terser '{file_path}' -o '{out}'"
        result = shell.execute(command=command, timeout=30)
        return result


class HTMLLinterTool(Tool):
    name = "html.lint"
    description = "Check HTML for issues and best practices"
    required_permissions = ["shell.execute"]

    def execute(self, path: str = ".", **kwargs) -> ToolResult:
        from cog.tools.shell import ShellTool

        shell = ShellTool()
        # Use pa11y for accessibility and best practices
        command = f"pa11y {path}"
        result = shell.execute(command=command, timeout=60)
        return result


class HTMLSyntaxVerifier(Verifier):
    name = "html.syntax"
    description = "Verify HTML syntax is valid"

    def verify(self, target, **kwargs) -> VerificationResult:
        from cog.tools.shell import ShellTool

        shell = ShellTool()
        # Use vnu jar for strict HTML validation
        result = shell.execute(
            command=f"vnu '{target}' --format json", timeout=30
        )
        if result.success:
            return VerificationResult(
                verifier=self.name,
                status=VerificationStatus.PASSED,
                message=f"HTML syntax valid: {target}",
            )
        return VerificationResult(
            verifier=self.name,
            status=VerificationStatus.FAILED,
            message=f"HTML syntax error in {target}",
            details={"error": result.error},
        )


class CogWebHTML(CogModule):
    name = "cog-web-html"
    version = "1.0.0"
    description = "HTML5 markup and semantic web expertise"

    def register_tools(self) -> list[Tool]:
        return [
            HTMLValidateTool(),
            HTMLFormatTool(),
            HTMLMinifyTool(),
            HTMLLinterTool(),
        ]

    def register_verifiers(self) -> list[Verifier]:
        return [HTMLSyntaxVerifier()]

    def get_prompt_extensions(self) -> list[str]:
        return [
            "## HTML5 Expertise",
            "",
            "You understand HTML5 including:",
            "",
            "### Semantic HTML",
            "- Semantic elements (header, nav, main, article, section, aside, footer)",
            "- Proper heading hierarchy (h1-h6)",
            "- Document outline algorithm",
            "- HTML5 semantic structure",
            "- Landmark regions for accessibility",
            "",
            "### HTML Elements",
            "- Text elements (p, span, strong, em, mark, del, ins)",
            "- Lists (ul, ol, li, dl, dt, dd)",
            "- Links and navigation (a, nav, link)",
            "- Images (img, picture, figure, figcaption)",
            "- Audio and video (audio, video, source, track)",
            "- Forms (form, input, textarea, select, button, label)",
            "- Tables (table, thead, tbody, tr, td, th)",
            "- Divisions and spans (div, span)",
            "- Inline vs block elements",
            "",
            "### HTML5 Features",
            "- New semantic elements",
            "- New input types (email, url, tel, number, date, etc.)",
            "- Form validation",
            "- Canvas and SVG",
            "- LocalStorage and SessionStorage",
            "- Web Workers",
            "- Geolocation API",
            "- Drag and Drop API",
            "- History API",
            "",
            "### Forms and Input",
            "- Form validation attributes (required, pattern, min, max)",
            "- Input types (text, email, url, tel, number, range, date, etc.)",
            "- Labels and accessibility",
            "- Form submission (GET vs POST)",
            "- File uploads",
            "- CSRF protection",
            "",
            "### Accessibility (a11y)",
            "- ARIA attributes (role, aria-label, aria-describedby)",
            "- alt text for images",
            "- form labels",
            "- keyboard navigation",
            "- focus management",
            "- screen reader compatibility",
            "- color contrast",
            "- semantic HTML for screen readers",
            "- skip navigation links",
            "",
            "### SEO (Search Engine Optimization)",
            "- title tags",
            "- meta descriptions",
            "- meta keywords",
            "- heading structure",
            "- semantic HTML for SEO",
            "- Open Graph tags",
            "- Twitter Cards",
            "- structured data (JSON-LD)",
            "- canonical URLs",
            "- sitemap.xml",
            "- robots.txt",
            "",
            "### Responsive Design",
            "- viewport meta tag",
            "- responsive images (srcset, sizes)",
            "- mobile-first approach",
            "- touch targets",
            "- responsive breakpoints",
            "",
            "### Performance",
            "- Critical CSS",
            "- defer loading of scripts",
            "- async loading of scripts",
            "- preloading important resources",
            "- minification",
            "- image optimization",
            "- lazy loading",
            "",
            "### Best Practices",
            "",
            "Document structure:",
            "- <!DOCTYPE html>",
            "- <html lang='en'>",
            "- <head> with meta tags, title, links",
            "- <body> with semantic structure",
            "",
            "When writing HTML:",
            "- Use semantic elements over divs",
            "- Maintain proper heading hierarchy",
            "- Provide alt text for images",
            "- Use labels for form inputs",
            "- Ensure keyboard navigation",
            "- Optimize for SEO and accessibility",
            "- Make responsive with viewport meta tag",
            "- Include Open Graph tags",
            "",
            "### Common Patterns",
            "",
            "Semantic document structure:",
            "<header>",
            "  <nav>...</nav>",
            "</header>",
            "<main>",
            "  <article>",
            "    <section>...</section>",
            "  </article>",
            "  <aside>...</aside>",
            "</main>",
            "<footer>...</footer>",
            "",
            "Responsive image:",
            "<img srcset='image-800w.jpg 800w, image-1200w.jpg 1200w'",
            "     sizes='(max-width: 800px) 800px, 1200px'",
            "     src='image-1200w.jpg'",
            "     alt='Description'>",
            "",
            "Accessible form:",
            "<form>",
            "  <label for='email'>Email:</label>",
            "  <input type='email' id='email' name='email'",
            "         required aria-required='true'>",
            "  <button type='submit'>Submit</button>",
            "</form>",
            "",
            "SEO meta tags:",
            "<title>Page Title</title>",
            "<meta name='description' content='Page description'>",
            "<meta property='og:title' content='Title'>",
            "<meta property='og:description' content='Description'>",
            "<meta property='og:image' content='image.jpg'>",
            "",
            "### HTML5 Validation",
            "",
            "Use HTML5 validation:",
            "- W3C Markup Validation Service",
            "- HTML Tidy",
            "- vnu.jar (HTML validator)",
            "- browser DevTools",
            "- Lighthouse (web quality)",
            "- axe DevTools (accessibility)",
            "",
            "Common HTML5 errors to avoid:",
            "- Missing alt attributes on images",
            "- Improper heading hierarchy",
            "- Non-semantic use of divs",
            "- Missing form labels",
            "- Not declaring document language",
            "- Missing viewport meta tag",
            "- Blocking render with scripts",
            "- Not optimizing images",
            "",
            "### Modern HTML Patterns",
            "",
            "Component structure:",
            "- Use elements for their purpose",
            "- Build reusable components",
            "- Document sections clearly",
            "- Use appropriate heading levels",
            "",
            "Performance optimization:",
            "- Defer non-critical CSS/JS",
            "- Preload critical resources",
            "- Optimize images and fonts",
            "- Minimize render blocking",
            "- Use lazy loading",
            "",
            "Accessibility:",
            "- Ensure keyboard navigability",
            "- Provide alt text",
            "- Use ARIA roles when needed",
            "- Maintain focus management",
            "- Test with screen readers",
            "- Check color contrast",
            "",
            "### When Working with HTML",
            "",
            "Creating new pages:",
            "- Use semantic HTML5 elements",
            "- Include proper meta tags",
            "- Ensure accessibility",
            "- Optimize for SEO",
            "- Make responsive",
            "- Validate HTML",
            "",
            "Maintaining existing HTML:",
            "- Preserve semantic structure",
            "- Update with best practices",
            "- Fix accessibility issues",
            "- Improve SEO",
            "- Optimize performance",
            "",
            "Debugging HTML:",
            "- Use browser DevTools",
            "- Validate HTML syntax",
            "- Check accessibility",
            "- Test on multiple browsers",
            "- Test on mobile devices",
            "",
            "### Integration with CSS and JavaScript",
            "",
            "HTML + CSS:",
            "- Use semantic classes",
            "- Avoid inline styles",
            "- Use CSS custom properties",
            "- Consider CSS-in-JS",
            "",
            "HTML + JavaScript:",
            "- Defer script loading",
            "- Use async for independent scripts",
            "- Place scripts before </body>",
            "- Use type='module' for ES modules",
            "",
            "### Tools and Validators",
            "",
            "Validation:",
            "- W3C Markup Validator",
            "- HTML Tidy",
            "- vnu.jar",
            "- Browser DevTools",
            "",
            "Accessibility:",
            "- axe DevTools",
            "- WAVE",
            "- Lighthouse",
            "- pa11y",
            "- NV Access (screen reader)",
            "",
            "SEO:",
            "- Google Search Console",
            "- PageSpeed Insights",
            "- GTmetrix",
            "- SEMrush",
            "- Ahrefs",
            "",
            "### HTML5 Resources",
            "",
            "Documentation:",
            "- MDN Web Docs (excellent)",
            "- W3C HTML specification",
            "- HTML5 Doctor",
            "- CSS-Tricks",
            "- Smashing Magazine",
            "",
            "Best practices:",
            "- Use semantic elements",
            "- Follow web standards",
            "- Ensure accessibility",
            "- Optimize for performance",
            "- Make mobile-friendly",
            "- Include SEO meta tags",
            "- Validate your HTML",
            "- Test on multiple browsers",
            "- Use appropriate heading hierarchy",
            "- Provide alt text for images",
            "- Use labels for form inputs",
            "",
            "### Troubleshooting",
            "",
            "Common issues:",
            "- Layout broken: Check CSS and HTML structure",
            "- Form not submitting: Check form attributes",
            "- Images not loading: Check paths and alt text",
            "- SEO poor: Check meta tags and semantic HTML",
            "- Accessibility issues: Use axe DevTools",
            "- Performance poor: Minify HTML, optimize images",
            "",
            "When debugging:",
            "- Use browser DevTools inspector",
            "- Check console for errors",
            "- Validate HTML syntax",
            "- Test on different browsers",
            "- Test on mobile devices",
            "- Use Lighthouse for audit",
            "",
            "### Security Considerations",
            "",
            "XSS prevention:",
            "- Sanitize user input",
            "- Use Content Security Policy",
            "- Encode output properly",
            "- Validate forms on server",
            "- Use HTTP headers",
            "",
            "Clickjacking:",
            "- Use X-Frame-Options header",
            "- Use frame-busting JavaScript",
            "",
            "Other security:",
            "- Use HTTPS",
            "- Implement CSP",
            "- Validate all inputs",
            "- Use HTTPOnly cookies",
            "- Keep HTML updated",
            "",
            "### HTML5 vs Previous Versions",
            "",
            "HTML5 advantages:",
            "- Semantic elements",
            "- Native form validation",
            "- New input types",
            "- Built-in multimedia support",
            "- Better accessibility",
            "- Improved SEO",
            "- Mobile-friendly",
            "",
            "Migration considerations:",
            "- Update doctype",
            "- Replace divs with semantic elements",
            "- Use new form input types",
            "- Add ARIA labels",
            "- Update meta tags",
            "- Ensure mobile responsiveness",
            "",
            "### HTML5 APIs",
            "",
            "Browser APIs:",
            "- Geolocation API",
            "- Canvas API",
            "- Web Storage (localStorage, sessionStorage)",
            "- Web Workers",
            "- WebSockets",
            "- Server-Sent Events",
            "- Notification API",
            "- Push API",
            "- Service Workers",
            "- Cache API",
            "- Fetch API",
            "",
            "When using HTML5 APIs:",
            "- Check browser support",
            "- Use feature detection",
            "- Provide fallbacks",
            "- Handle errors gracefully",
            "- Consider performance",
            "- Ensure security",
            "",
            "### Final Best Practices",
            "",
            "When creating HTML:",
            "1. Use semantic elements",
            "2. Follow proper hierarchy",
            "3. Include accessibility features",
            "4. Add SEO meta tags",
            "5. Make responsive",
            "6. Optimize performance",
            "7. Validate your HTML",
            "8. Test thoroughly",
            "9. Follow web standards",
            "10. Keep learning and improving",
        ]

    def get_capabilities(self) -> list[str]:
        return [
            "html5",
            "semantic_html",
            "forms",
            "input_validation",
            "accessibility",
            "seo",
            "responsive_design",
            "html_validation",
            "html_minification",
            "lighthouse",
            "open_graph",
            "structured_data",
            "web_components",
            "performance_optimization",
        ]


module = CogWebHTML()

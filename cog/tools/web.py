from __future__ import annotations

import json
from typing import Any

from cog.tools.base import Tool, ToolResult


class WebFetchTool(Tool):
    name = "web.fetch"
    description = "Fetch content from a URL"
    required_permissions = ["network.access"]

    def execute(self, *args, **kwargs) -> ToolResult:
        url = kwargs.get("url", "")
        if not url:
            return ToolResult(success=False, output="", error="URL required")
        try:
            import urllib.request

            req = urllib.request.Request(url, headers={"User-Agent": "CogOS/1.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                content = resp.read(50000).decode("utf-8", errors="replace")
                return ToolResult(
                    success=True,
                    output=content[:10000],
                    metadata={"url": url, "status": resp.status},
                )
        except Exception as e:
            return ToolResult(success=False, output="", error=str(e))


class WebSearchTool(Tool):
    name = "web.search"
    description = "Search the web using a search engine"
    required_permissions = ["network.access"]

    def execute(self, *args, **kwargs) -> ToolResult:
        query = kwargs.get("query", "")
        if not query:
            return ToolResult(success=False, output="", error="Query required")
        try:
            import urllib.request
            import urllib.parse

            encoded = urllib.parse.quote_plus(query)
            url = f"https://html.duckduckgo.com/html/?q={encoded}"
            req = urllib.request.Request(url, headers={"User-Agent": "CogOS/1.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                html = resp.read(50000).decode("utf-8", errors="replace")
            results = self._parse_results(html)
            if not results:
                return ToolResult(
                    success=True, output="No results found", metadata={"query": query}
                )
            return ToolResult(
                success=True,
                output="\n\n".join(
                    f"- {r['title']}: {r['snippet']}" for r in results[:8]
                ),
                metadata={"query": query, "count": len(results)},
            )
        except Exception as e:
            return ToolResult(success=False, output="", error=str(e))

    @staticmethod
    def _parse_results(html: str) -> list[dict[str, str]]:
        results = []
        import re

        blocks = re.findall(
            r'<a rel="nofollow" class="result__a" href="([^"]+)"[^>]*>(.*?)</a>.*?'
            r'<a class="result__snippet"[^>]*>(.*?)</a>',
            html,
            re.DOTALL,
        )
        for url, title, snippet in blocks[:10]:
            title = re.sub(r"<[^>]+>", "", title).strip()
            snippet = re.sub(r"<[^>]+>", "", snippet).strip()
            if title:
                results.append({"url": url, "title": title, "snippet": snippet[:300]})
        return results

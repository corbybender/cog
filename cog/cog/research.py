"""
Research and Context Gathering System

This system enables CogOS to:
1. Search and gather information from multiple sources
2. Read and analyze documentation
3. Explore codebases
4. Gather context before making decisions
5. Validate assumptions with research

This is crucial for making informed decisions rather than guessing.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import json
import re
from datetime import datetime
from pathlib import Path

from cog.llm.provider import LLMProvider
from cog.memory.backend import MemoryBackend
from cog.cache.smart_cache import SmartCache


class ResearchSource(Enum):
    """Sources of information"""
    WEB_SEARCH = "web_search"
    DOCUMENTATION = "documentation"
    CODEBASE = "codebase"
    FILES = "files"
    MEMORY = "memory"
    GIT = "git"
    API = "api"


@dataclass
class ResearchQuery:
    """A research query"""
    query_id: str
    question: str
    sources: List[ResearchSource]
    context: str = ""
    priority: int = 5
    status: str = "pending"
    results: List['ResearchResult'] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class ResearchResult:
    """Result from research"""
    source: ResearchSource
    content: str
    relevance: float  # 0-1
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


class Researcher:
    """
    Gathers information from multiple sources

    This is the "research assistant" of CogOS.
    """

    def __init__(
        self,
        llm_provider: LLMProvider,
        memory: MemoryBackend,
        cache: SmartCache
    ):
        self.llm = llm_provider
        self.memory = memory
        self.cache = cache
        self.research_history: List[ResearchQuery] = []

    async def research(
        self,
        question: str,
        sources: List[ResearchSource] = None,
        context: str = "",
        max_results: int = 10
    ) -> ResearchQuery:
        """
        Research a question from multiple sources

        This is where CogOS gathers context before making decisions.
        """
        if sources is None:
            sources = [
                ResearchSource.MEMORY,
                ResearchSource.CODEBASE,
                ResearchSource.DOCUMENTATION,
                ResearchSource.WEB_SEARCH
            ]

        query = ResearchQuery(
            query_id=f"query_{len(self.research_history)}",
            question=question,
            sources=sources,
            context=context
        )

        # Research from each source in parallel
        for source in sources:
            try:
                results = await self._research_from_source(
                    question,
                    source,
                    context,
                    max_results
                )
                query.results.extend(results)
            except Exception as e:
                # Log error but continue with other sources
                print(f"Error researching from {source}: {e}")

        # Sort by relevance
        query.results.sort(key=lambda r: r.relevance, reverse=True)

        # Keep top results
        query.results = query.results[:max_results]

        query.status = "completed"
        self.research_history.append(query)

        # Cache results
        await self._cache_research(query)

        return query

    async def _research_from_source(
        self,
        question: str,
        source: ResearchSource,
        context: str,
        max_results: int
    ) -> List[ResearchResult]:
        """Research from a specific source"""

        if source == ResearchSource.MEMORY:
            return await self._research_memory(question, context)
        elif source == ResearchSource.CODEBASE:
            return await self._research_codebase(question, context, max_results)
        elif source == ResearchSource.DOCUMENTATION:
            return await self._research_documentation(question, context)
        elif source == ResearchSource.WEB_SEARCH:
            return await self._research_web(question, context, max_results)
        elif source == ResearchSource.FILES:
            return await self._research_files(question, context, max_results)
        else:
            return []

    async def _research_memory(
        self,
        question: str,
        context: str
    ) -> List[ResearchResult]:
        """Research from memory"""
        # Search memory for relevant information
        results = []

        # Simple keyword search
        keywords = self._extract_keywords(question)

        for keyword in keywords:
            memories = await self.memory.search(keyword, limit=5)
            for memory in memories:
                results.append(ResearchResult(
                    source=ResearchSource.MEMORY,
                    content=memory.get("value", ""),
                    relevance=0.7,  # Base relevance
                    metadata={"memory_key": memory.get("key")}
                ))

        return results

    async def _research_codebase(
        self,
        question: str,
        context: str,
        max_results: int
    ) -> List[ResearchResult]:
        """Research from codebase"""
        results = []

        # Use GitNexus to search codebase
        try:
            from cog.mcp import mcp_tools

            # Search for relevant code
            search_results = await mcp_tools.gitnexus_query(
                query=question,
                limit=max_results,
                repo="Projects"
            )

            for process in search_results.get("processes", []):
                results.append(ResearchResult(
                    source=ResearchSource.CODEBASE,
                    content=json.dumps(process, indent=2),
                    relevance=0.8,
                    metadata={
                        "process": process.get("heuristicLabel", ""),
                        "symbols": len(process.get("process_symbols", []))
                    }
                ))

        except Exception as e:
            print(f"Error using GitNexus: {e}")

        return results

    async def _research_documentation(
        self,
        question: str,
        context: str
    ) -> List[ResearchResult]:
        """Research from documentation"""
        results = []

        # Check for relevant documentation files
        doc_paths = [
            "README.md",
            "docs/",
            "documentation/",
            "*.md"
        ]

        # In production, would search these files
        # For now, return placeholder
        results.append(ResearchResult(
            source=ResearchSource.DOCUMENTATION,
            content=f"Documentation search for: {question}",
            relevance=0.5,
            metadata={"query": question}
        ))

        return results

    async def _research_web(
        self,
        question: str,
        context: str,
        max_results: int
    ) -> List[ResearchResult]:
        """Research from web"""
        results = []

        try:
            # Use web search tool
            from cog.tools.web import WebSearchTool

            search_tool = WebSearchTool()
            search_result = await search_tool.search(question, num_results=max_results)

            if search_result.success:
                # Parse search results
                # In production, would parse actual results
                results.append(ResearchResult(
                    source=ResearchSource.WEB_SEARCH,
                    content=search_result.data,
                    relevance=0.6,
                    metadata={"query": question}
                ))

        except Exception as e:
            print(f"Error searching web: {e}")

        return results

    async def _research_files(
        self,
        question: str,
        context: str,
        max_results: int
    ) -> List[ResearchResult]:
        """Research from files"""
        results = []

        # Use filesystem search
        try:
            from cog.tools.filesystem import FilesystemTool

            fs_tool = FilesystemTool()

            # Search for files matching keywords
            keywords = self._extract_keywords(question)

            for keyword in keywords[:3]:  # Limit to 3 keywords
                search_result = await fs_tool.search(keyword, path=".")

                if search_result.success:
                    results.append(ResearchResult(
                        source=ResearchSource.FILES,
                        content=f"Found files matching '{keyword}': {search_result.data}",
                        relevance=0.6,
                        metadata={"keyword": keyword}
                    ))

        except Exception as e:
            print(f"Error searching files: {e}")

        return results

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text"""
        # Simple keyword extraction
        # In production, would use NLP
        words = re.findall(r'\b\w+\b', text.lower())

        # Filter out common words
        stop_words = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
                     'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
                     'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from'}

        keywords = [w for w in words if w not in stop_words and len(w) > 3]

        # Return unique keywords
        return list(set(keywords))

    async def _cache_research(self, query: ResearchQuery):
        """Cache research results"""
        await self.memory.store(
            key=f"research:{query.query_id}",
            value={
                "question": query.question,
                "results": [
                    {
                        "source": r.source.value,
                        "content": r.content[:500],  # Truncate for storage
                        "relevance": r.relevance
                    }
                    for r in query.results
                ],
                "timestamp": query.timestamp.isoformat()
            },
            metadata={
                "type": "research",
                "question": query.question
            }
        )

    async def synthesize_findings(
        self,
        query: ResearchQuery
    ) -> str:
        """Synthesize research findings into a summary"""
        if not query.results:
            return f"No results found for: {query.question}"

        synthesis_prompt = f"""You are a Research Synthesis Agent. Synthesize these research results:

QUESTION: {query.question}
CONTEXT: {query.context}

RESULTS:
{json.dumps([{
    "source": r.source.value,
    "content": r.content[:500],
    "relevance": r.relevance
} for r in query.results[:5]], indent=2)}

Provide:
1. SUMMARY: A concise summary of findings
2. KEY_INSIGHTS: 3-5 key insights
3. GAPS: What information is still missing?
4. RECOMMENDATIONS: How to proceed?

Be specific and cite sources."""

        messages = [
            {"role": "system", "content": "You are a research synthesis agent."},
            {"role": "user", "content": synthesis_prompt}
        ]

        response = await self.llm.generate(
            messages=messages,
            temperature=0.5,
            max_tokens=2000
        )

        return response.content


class ContextGatherer:
    """
    Gathers comprehensive context for tasks

    This ensures CogOS has all relevant information before acting.
    """

    def __init__(
        self,
        llm_provider: LLMProvider,
        memory: MemoryBackend,
        cache: SmartCache,
        researcher: Researcher
    ):
        self.llm = llm_provider
        self.memory = memory
        self.cache = cache
        self.researcher = researcher

    async def gather_context(
        self,
        task: str,
        additional_context: str = ""
    ) -> Dict[str, Any]:
        """
        Gather comprehensive context for a task

        This is where CogOS ensures it understands the full picture.
        """
        context = {
            "task": task,
            "additional_context": additional_context,
            "research_findings": [],
            "codebase_context": [],
            "memory_context": [],
            "documentation_references": []
        }

        # Research the task
        research_query = await self.researcher.research(
            question=f"How to: {task}",
            context=additional_context,
            max_results=5
        )

        # Synthesize findings
        synthesis = await self.researcher.synthesize_findings(research_query)
        context["research_synthesis"] = synthesis
        context["research_findings"] = research_query.results

        # Get codebase context
        codebase_results = await self.researcher._research_from_source(
            task,
            ResearchSource.CODEBASE,
            additional_context,
            3
        )
        context["codebase_context"] = codebase_results

        # Get memory context
        memory_results = await self.researcher._research_from_source(
            task,
            ResearchSource.MEMORY,
            additional_context,
            3
        )
        context["memory_context"] = memory_results

        return context

    async def validate_assumptions(
        self,
        task: str,
        assumptions: List[str],
        context: str = ""
    ) -> Dict[str, Any]:
        """
        Validate assumptions with research

        This prevents CogOS from making incorrect assumptions.
        """
        validation_prompt = f"""You are an Assumption Validation Agent. Validate these assumptions:

TASK: {task}
CONTEXT: {context}

ASSUMPTIONS:
{json.dumps(assumptions, indent=2)}

For each assumption:
1. Check if it's valid (supported by evidence)
2. Identify potential risks or counter-examples
3. Suggest validation steps if uncertain

Return as JSON:
{{
  "validations": [
    {{
      "assumption": "...",
      "is_valid": true/false,
      "confidence": 0.8,
      "risks": ["..."],
      "validation_steps": ["..."]
    }}
  ]
}}"""

        messages = [
            {"role": "system", "content": "You are an assumption validation agent. Return valid JSON only."},
            {"role": "user", "content": validation_prompt}
        ]

        try:
            response = await self.llm.generate(
                messages=messages,
                temperature=0.3,
                max_tokens=2000
            )

            return json.loads(response.content)

        except (json.JSONDecodeError, Exception) as e:
            return {
                "error": f"Failed to validate assumptions: {e}",
                "validations": []
            }

"""
Document Generation and Writing System

This system enables CogOS to:
1. Write comprehensive documentation
2. Generate technical reports
3. Create multi-section documents with collaboration
4. Review and revise documents
5. Format documents for different audiences

This is essential for producing high-quality written output.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import json
from datetime import datetime

from cog.llm.provider import LLMProvider
from cog.memory.backend import MemoryBackend
from cog.cache.smart_cache import SmartCache


class DocumentType(Enum):
    """Types of documents"""
    TECHNICAL_REPORT = "technical_report"
    DOCUMENTATION = "documentation"
    TUTORIAL = "tutorial"
    GUIDE = "guide"
    API_REFERENCE = "api_reference"
    DESIGN_DOC = "design_doc"
    PROPOSAL = "proposal"
    SUMMARY = "summary"
    ANALYSIS = "analysis"


class DocumentSection:
    """A section of a document"""

    def __init__(
        self,
        title: str,
        content: str = "",
        subsections: List['DocumentSection'] = None,
        metadata: Dict[str, Any] = None
    ):
        self.title = title
        self.content = content
        self.subsections = subsections or []
        self.metadata = metadata or {}
        self.reviews: List[str] = []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "content": self.content,
            "subsections": [s.to_dict() for s in self.subsections],
            "metadata": self.metadata,
            "reviews": self.reviews
        }


class Document:
    """A structured document"""

    def __init__(
        self,
        title: str,
        doc_type: DocumentType,
        sections: List[DocumentSection] = None,
        metadata: Dict[str, Any] = None
    ):
        self.title = title
        self.doc_type = doc_type
        self.sections = sections or []
        self.metadata = metadata or {}
        self.revisions: List[Dict[str, Any]] = []
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "type": self.doc_type.value,
            "sections": [s.to_dict() for s in self.sections],
            "metadata": self.metadata,
            "revisions": self.revisions,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    def to_markdown(self) -> str:
        """Convert document to markdown"""
        md = f"# {self.title}\n\n"

        for section in self.sections:
            md += self._section_to_markdown(section, level=2)

        return md

    def _section_to_markdown(self, section: DocumentSection, level: int) -> str:
        """Convert section to markdown"""
        prefix = "#" * level
        md = f"{prefix} {section.title}\n\n"
        md += f"{section.content}\n\n"

        for subsection in section.subsections:
            md += self._section_to_markdown(subsection, level + 1)

        return md


class DocumentWriter:
    """
    Writes and structures documents

    This is the "author" of CogOS.
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
        self.documents_created: List[Document] = []

    async def write_document(
        self,
        title: str,
        topic: str,
        doc_type: DocumentType,
        context: str = "",
        research_findings: List[str] = None,
        target_audience: str = "technical"
    ) -> Document:
        """
        Write a comprehensive document

        This is where CogOS produces high-quality written content.
        """
        # Create document structure
        document = Document(
            title=title,
            doc_type=doc_type,
            metadata={
                "topic": topic,
                "target_audience": target_audience,
                "context": context
            }
        )

        # Generate document outline
        outline = await self._generate_outline(
            topic,
            doc_type,
            target_audience,
            context
        )

        # Write each section
        for section_info in outline.get("sections", []):
            section = await self._write_section(
                section_info,
                topic,
                doc_type,
                target_audience,
                context,
                research_findings or []
            )
            document.sections.append(section)

        # Review document
        reviewed_document = await self._review_document(document)

        self.documents_created.append(reviewed_document)

        return reviewed_document

    async def _generate_outline(
        self,
        topic: str,
        doc_type: DocumentType,
        target_audience: str,
        context: str
    ) -> Dict[str, Any]:
        """Generate document outline"""
        outline_prompt = f"""You are a Document Outline Agent. Create an outline for:

TOPIC: {topic}
TYPE: {doc_type.value}
AUDIENCE: {target_audience}
CONTEXT: {context}

Create a comprehensive outline with:
1. Main sections (4-8 sections)
2. Subsections for each main section
3. Brief description of each section's purpose
4. Suggested content for each section

Return as JSON:
{{
  "title": "Document Title",
  "sections": [
    {{
      "title": "Section Title",
      "description": "What this section covers",
      "subsections": [
        {{
          "title": "Subsection Title",
          "description": "What this subsection covers"
        }}
      ]
    }}
  ]
}}

Be thorough and logical. Focus on clarity and completeness."""

        messages = [
            {"role": "system", "content": "You are a document outline agent. Return valid JSON only."},
            {"role": "user", "content": outline_prompt}
        ]

        response = await self.llm.generate(
            messages=messages,
            temperature=0.5,
            max_tokens=2000
        )

        try:
            return json.loads(response.content)
        except json.JSONDecodeError:
            # Fallback outline
            return {
                "title": topic,
                "sections": [
                    {"title": "Introduction", "description": "Overview", "subsections": []},
                    {"title": "Main Content", "description": "Core information", "subsections": []},
                    {"title": "Conclusion", "description": "Summary", "subsections": []}
                ]
            }

    async def _write_section(
        self,
        section_info: Dict[str, Any],
        topic: str,
        doc_type: DocumentType,
        target_audience: str,
        context: str,
        research_findings: List[str]
    ) -> DocumentSection:
        """Write a single section"""
        section_prompt = f"""You are a Technical Writing Agent. Write this section:

SECTION: {section_info['title']}
DESCRIPTION: {section_info.get('description', '')}
TOPIC: {topic}
TYPE: {doc_type.value}
AUDIENCE: {target_audience}

CONTEXT: {context}

RESEARCH FINDINGS:
{json.dumps(research_findings, indent=2) if research_findings else "None"}

REQUIREMENTS:
1. Write comprehensive, clear content
2. Use examples where appropriate
3. Include code snippets or diagrams if relevant
4. Maintain consistency with {target_audience} level
5. Be thorough but concise

Write the section content now:"""

        messages = [
            {"role": "system", "content": "You are a technical writing agent."},
            {"role": "user", "content": section_prompt}
        ]

        response = await self.llm.generate(
            messages=messages,
            temperature=0.6,
            max_tokens=3000
        )

        section = DocumentSection(
            title=section_info["title"],
            content=response.content,
            metadata=section_info
        )

        # Write subsections
        for subsection_info in section_info.get("subsections", []):
            subsection = await self._write_section(
                subsection_info,
                topic,
                doc_type,
                target_audience,
                context,
                research_findings
            )
            section.subsections.append(subsection)

        return section

    async def _review_document(
        self,
        document: Document
    ) -> Document:
        """Review and improve document"""
        review_prompt = f"""You are a Document Review Agent. Review this document:

TITLE: {document.title}
TYPE: {document.doc_type.value}

CONTENT:
{document.to_markdown()[:4000]}

Review for:
1. Clarity and completeness
2. Organization and flow
3. Accuracy and correctness
4. Appropriate for audience
5. Missing information
6. Improvements needed

Provide specific, actionable feedback on each section."""

        messages = [
            {"role": "system", "content": "You are a document review agent."},
            {"role": "user", "content": review_prompt}
        ]

        response = await self.llm.generate(
            messages=messages,
            temperature=0.3,
            max_tokens=2000
        )

        # Apply review feedback
        # In production, would iterate and improve
        document.metadata["review"] = response.content

        return document


class CollaborativeWriter:
    """
    Coordinates multiple agents to write documents collaboratively

    This produces better documents than a single agent.
    """

    def __init__(
        self,
        llm_provider: LLMProvider,
        memory: MemoryBackend,
        cache: SmartCache,
        writer: DocumentWriter
    ):
        self.llm = llm_provider
        self.memory = memory
        self.cache = cache
        self.writer = writer

    async def collaborative_write(
        self,
        title: str,
        topic: str,
        doc_type: DocumentType,
        context: str = "",
        research_findings: List[str] = None,
        iterations: int = 2
    ) -> Document:
        """
        Write document using multiple perspectives

        This produces more comprehensive and balanced documents.
        """
        document = await self.writer.write_document(
            title=title,
            topic=topic,
            doc_type=doc_type,
            context=context,
            research_findings=research_findings
        )

        # Iterative improvement
        for iteration in range(iterations):
            # Get feedback from different perspectives
            perspectives = [
                await self._get_review_perspective(document, "clarity"),
                await self._get_review_perspective(document, "completeness"),
                await self._get_review_perspective(document, "accuracy")
            ]

            # Synthesize feedback
            feedback = await self._synthesize_feedback(perspectives)

            # Apply improvements
            if feedback:
                document = await self._improve_document(document, feedback)

                # Record revision
                document.revisions.append({
                    "iteration": iteration + 1,
                    "feedback": feedback,
                    "timestamp": datetime.now().isoformat()
                })

        return document

    async def _get_review_perspective(
        self,
        document: Document,
        perspective: str
    ) -> str:
        """Get review from specific perspective"""
        perspective_prompts = {
            "clarity": "Review for clarity, readability, and flow. Is the writing clear?",
            "completeness": "Review for completeness. Is anything missing?",
            "accuracy": "Review for accuracy. Is the information correct?"
        }

        prompt = f"""Review this document from a {perspective} perspective:

{perspective_prompts.get(perspective, perspective)}

{document.to_markdown()[:2000]}

Provide specific feedback:"""

        messages = [
            {"role": "system", "content": f"You are a {perspective} reviewer."},
            {"role": "user", "content": prompt}
        ]

        response = await self.llm.generate(
            messages=messages,
            temperature=0.4,
            max_tokens=1000
        )

        return response.content

    async def _synthesize_feedback(
        self,
        perspectives: List[str]
    ) -> str:
        """Synthesize feedback from multiple perspectives"""
        synthesis_prompt = f"""Synthesize this feedback into actionable improvements:

{json.dumps(perspectives, indent=2)}

Provide:
1. Priority improvements (most important)
2. Section-specific feedback
3. Overall recommendations"""

        messages = [
            {"role": "system", "content": "You are a feedback synthesizer."},
            {"role": "user", "content": synthesis_prompt}
        ]

        response = await self.llm.generate(
            messages=messages,
            temperature=0.3,
            max_tokens=1500
        )

        return response.content

    async def _improve_document(
        self,
        document: Document,
        feedback: str
    ) -> Document:
        """Improve document based on feedback"""
        # In production, would apply specific improvements
        # For now, just record feedback
        document.metadata["improvement_feedback"] = feedback
        return document

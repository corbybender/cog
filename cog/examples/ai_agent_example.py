#!/usr/bin/env python3
"""
Real-World Example: AI Agent Using CogOS

This shows a practical example of an AI assistant that uses
CogOS for complex tasks while handling simple tasks itself.
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from cog.cogos import create_cogos
from cog.llm.provider import LLMProvider
from cog.memory.backend import MemoryBackend
from cog.cache.smart_cache import SmartCache


class SmartAssistant:
    """
    An AI assistant that uses CogOS for complex tasks

    This assistant can:
    - Handle simple questions directly
    - Delegate complex problems to CogOS
    - Use CogOS for research
    - Use CogOS to write documentation
    - Use CogOS to plan implementations
    """

    def __init__(self):
        print("🤖 Initializing Smart Assistant with CogOS...")

        # Initialize CogOS
        self.llm = LLMProvider()
        self.memory = MemoryBackend(db_path=":memory:")
        self.cache = SmartCache(max_size=1000, ttl_seconds=3600)
        self.cogos = create_cogos(self.llm, self.memory, self.cache, enable_all=True)

        # Conversation history
        self.history = []

        print("✓ Ready!\n")

    async def chat(self):
        """Interactive chat loop"""
        print("="*80)
        print("🤖 Smart Assistant with CogOS Super-Intelligence")
        print("="*80)
        print("\nI can help you with:")
        print("  • Simple questions (I'll answer directly)")
        print("  • Complex problems (I'll use CogOS multi-agent system)")
        print("  • Research tasks (I'll research from multiple sources)")
        print("  • Documentation (I'll write comprehensive docs)")
        print("  • System design (I'll create detailed plans)")
        print("\nType 'quit' to exit\n")
        print("="*80)

        while True:
            try:
                # Get user input
                user_input = input("\n👤 You: ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Goodbye!")
                    break

                # Process input
                print("\n🤔 Thinking...")
                response = await self.process_input(user_input)

                # Display response
                print(f"\n🤖 Assistant:\n{response}")

                # Store in history
                self.history.append({
                    "user": user_input,
                    "assistant": response
                })

            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")

    async def process_input(self, user_input: str) -> str:
        """Process user input and decide how to respond"""

        # Analyze input complexity
        complexity = await self.analyze_complexity(user_input)

        if complexity['level'] == 'simple':
            # Handle directly
            return await self.handle_simple(user_input)

        elif complexity['level'] == 'complex':
            # Use CogOS for complex problems
            return await self.handle_with_cogos(
                user_input,
                complexity['approach']
            )

        else:
            # Research task
            return await self.handle_research(user_input)

    async def analyze_complexity(self, text: str) -> dict:
        """Analyze how complex the input is"""

        text_lower = text.lower()

        # Complex problem indicators
        complex_words = [
            'design', 'architecture', 'implement', 'build', 'create',
            'optimize', 'refactor', 'debug', 'solve', 'plan'
        ]

        # Research indicators
        research_words = [
            'research', 'find', 'best practices', 'compare',
            'vs', 'versus', 'difference', 'explain'
        ]

        # Document indicators
        doc_words = [
            'write', 'document', 'documentation', 'guide',
            'tutorial', 'readme'
        ]

        # Check complexity
        if any(word in text_lower for word in complex_words):
            # Determine approach
            if 'design' in text_lower or 'architecture' in text_lower:
                approach = 'collaborative'
            elif 'implement' in text_lower or 'build' in text_lower:
                approach = 'planned'
            else:
                approach = 'comprehensive'

            return {'level': 'complex', 'approach': approach}

        elif any(word in text_lower for word in research_words):
            return {'level': 'research', 'approach': 'researched'}

        elif any(word in text_lower for word in doc_words):
            return {'level': 'complex', 'approach': 'collaborative'}

        else:
            return {'level': 'simple', 'approach': None}

    async def handle_simple(self, text: str) -> str:
        """Handle simple questions directly"""

        messages = [
            {
                "role": "system",
                "content": "You are a helpful AI assistant. Answer concisely and accurately."
            },
            {
                "role": "user",
                "content": text
            }
        ]

        try:
            response = await self.llm.generate(
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )

            # Add note that we didn't use CogOS
            return f"{response.content}\n\n*(Direct response - CogOS not needed for this simple question)*"

        except Exception as e:
            return f"Sorry, I encountered an error: {e}"

    async def handle_with_cogos(self, problem: str, approach: str) -> str:
        """Handle complex problems using CogOS"""

        try:
            # Use CogOS
            result = await self.cogos.solve_complex_problem(
                problem=problem,
                approach=approach
            )

            if not result.get('success'):
                return f"Sorry, I encountered an error: {result.get('error')}"

            # Build response
            parts = []

            # Add header
            parts.append(f"🧠 Using CogOS {approach} approach...\n")

            # Add solution
            if result.get('solution'):
                parts.append("## Solution")
                parts.append(result['solution'])

            # Add validation
            validation = result.get('validation', {})
            if validation:
                confidence = validation.get('confidence', 0)
                parts.append(f"\n## Confidence: {confidence:.1%}")

                if validation.get('issues'):
                    parts.append("\n## Notes:")
                    for issue in validation['issues'][:3]:
                        parts.append(f"  • {issue}")

            # Add process info
            if result.get('stages'):
                parts.append("\n## Process Used:")
                for i, stage in enumerate(result['stages'], 1):
                    stage_name = stage.get('stage', 'unknown')
                    stage_name = stage_name.replace('_', ' ').title()
                    parts.append(f"  {i}. {stage_name}")

            return "\n".join(parts)

        except Exception as e:
            return f"Sorry, I encountered an error with CogOS: {e}"

    async def handle_research(self, question: str) -> str:
        """Handle research questions"""

        try:
            from cog.research import Researcher, ResearchSource

            researcher = Researcher(self.llm, self.memory, self.cache)

            # Research
            query = await researcher.research(
                question=question,
                sources=[
                    ResearchSource.WEB_SEARCH,
                    ResearchSource.CODEBASE,
                    ResearchSource.DOCUMENTATION
                ],
                max_results=5
            )

            # Synthesize
            synthesis = await researcher.synthesize_findings(query)

            # Build response
            parts = [
                "🔍 Research Results\n",
                "## Findings",
                synthesis,
                f"\n## Sources Consulted: {len(query.results)}"
            ]

            return "\n".join(parts)

        except Exception as e:
            return f"Sorry, I encountered an error during research: {e}"


async def demo_conversation():
    """Run a demo conversation"""

    assistant = SmartAssistant()

    demo_inputs = [
        "What is Python?",  # Simple
        "Design a scalable microservices architecture for an e-commerce platform",  # Complex - collaborative
        "Research the best practices for REST API authentication",  # Research
        "How do I implement a caching layer?",  # Complex - planned
    ]

    print("\n" + "="*80)
    print("🤖 DEMO: Smart Assistant with CogOS")
    print("="*80 + "\n")

    for i, user_input in enumerate(demo_inputs, 1):
        print(f"\n{'='*80}")
        print(f"Example {i}/4")
        print(f"{'='*80}\n")

        print(f"👤 User: {user_input}")
        print("\n🤔 Thinking...\n")

        response = await assistant.process_input(user_input)

        print(f"🤖 Assistant:\n{response}\n")

        # Pause between examples
        if i < len(demo_inputs):
            input("\n[Press Enter to continue to next example]\n")


async def main():
    """Main entry point"""

    import sys

    if len(sys.argv) > 1 and sys.argv[1] == '--demo':
        # Run demo
        await demo_conversation()
    else:
        # Run interactive chat
        assistant = SmartAssistant()
        await assistant.chat()


if __name__ == "__main__":
    asyncio.run(main())

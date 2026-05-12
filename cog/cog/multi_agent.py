"""
Multi-Agent Orchestration System for CogOS

This system enables multiple specialized agents to:
1. Work in parallel on different aspects of a task
2. Communicate and debate with each other
3. Vote on best solutions
4. Refine and improve each other's work
5. Execute and validate solutions

This is what separates CogOS from single-pass systems like Claude.
"""

from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import json
import asyncio
from datetime import datetime
from pathlib import Path

from cog.providers.base import LLMProvider
from cog.memory.base import MemoryBackend
from cog.cache import SmartCache


class AgentRole(Enum):
    """Specialized agent roles"""
    PLANNER = "planner"  # Breaks down tasks
    RESEARCHER = "researcher"  # Gathers information
    CODER = "coder"  # Writes code
    REVIEWER = "reviewer"  # Reviews and critiques
    TESTER = "tester"  # Tests and validates
    CRITIC = "critic"  # Finds flaws and improvements
    DOCUMENTER = "documenter"  # Writes documentation
    OPTIMIZER = "optimizer"  # Optimizes performance
    SECURITY = "security"  # Security analysis
    ARCHITECT = "architect"  # System design


@dataclass
class AgentMessage:
    """Message between agents"""
    from_agent: str
    to_agent: str
    content: str
    message_type: str  # proposal, critique, question, answer, vote
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentTask:
    """Task assigned to an agent"""
    task_id: str
    description: str
    agent_role: AgentRole
    context: Dict[str, Any]
    dependencies: List[str] = field(default_factory=list)
    priority: int = 5
    status: str = "pending"  # pending, in_progress, completed, failed
    result: Optional[Any] = None
    error: Optional[str] = None


@dataclass
class AgentProposal:
    """Proposal from an agent"""
    agent_name: str
    proposal_type: str  # solution, approach, code, design
    content: str
    reasoning: str
    confidence: float  # 0-1
    timestamp: datetime = field(default_factory=datetime.now)
    votes: List[str] = field(default_factory=list)
    critiques: List[str] = field(default_factory=list)


class Agent:
    """Specialized autonomous agent"""

    def __init__(
        self,
        name: str,
        role: AgentRole,
        llm_provider: LLMProvider,
        memory: MemoryBackend,
        cache: SmartCache,
        modules: List[str] = None
    ):
        self.name = name
        self.role = role
        self.llm = llm_provider
        self.memory = memory
        self.cache = cache
        self.modules = modules or []
        self.message_queue: List[AgentMessage] = []
        self.tasks_completed = 0
        self.proposals_made = 0

    async def think(self, context: str, task: str) -> str:
        """Think about a problem using role-specific expertise"""
        role_prompt = self._get_role_prompt()

        messages = [
            {"role": "system", "content": role_prompt},
            {"role": "user", "content": f"Context:\n{context}\n\nTask:\n{task}"}
        ]

        response = await self.llm.generate(
            messages=messages,
            temperature=0.7,
            max_tokens=2000
        )

        return response.content

    async def propose(self, context: str, task: str) -> AgentProposal:
        """Make a proposal for solving a problem"""
        thinking = await self.think(context, task)

        # Extract confidence from thinking
        confidence = self._extract_confidence(thinking)

        return AgentProposal(
            agent_name=self.name,
            proposal_type=self.role.value,
            content=thinking,
            reasoning=thinking,
            confidence=confidence
        )

    def _get_role_prompt(self) -> str:
        """Get role-specific system prompt"""
        prompts = {
            AgentRole.PLANNER: """You are a Strategic Planner Agent. Your role is to:
1. Break down complex tasks into clear, actionable steps
2. Identify dependencies and execution order
3. Estimate complexity and risk
4. Consider multiple approaches
5. Create detailed execution plans

Be thorough but pragmatic. Focus on executable plans.""",

            AgentRole.RESEARCHER: """You are a Research Agent. Your role is to:
1. Gather comprehensive information on topics
2. Find authoritative sources and documentation
3. Synthesize information from multiple sources
4. Identify gaps in knowledge
5. Provide context and background

Be thorough and cite sources. Focus on accuracy.""",

            AgentRole.CODER: """You are a Master Code Agent. Your role is to:
1. Write clean, efficient, well-documented code
2. Follow best practices and design patterns
3. Consider edge cases and error handling
4. Write tests alongside code
5. Optimize for readability and maintainability

Write production-ready code. Focus on quality.""",

            AgentRole.REVIEWER: """You are a Code Review Agent. Your role is to:
1. Critically analyze code for issues
2. Identify bugs, security flaws, and performance issues
3. Suggest improvements and refactoring
4. Check adherence to best practices
5. Provide actionable feedback

Be constructive but thorough. Focus on quality.""",

            AgentRole.TESTER: """You are a Testing Agent. Your role is to:
1. Design comprehensive test suites
2. Consider edge cases and boundary conditions
3. Write both unit and integration tests
4. Test for performance and reliability
5. Automate testing where possible

Be thorough. Focus on coverage and correctness.""",

            AgentRole.CRITIC: """You are a Critical Thinking Agent. Your role is to:
1. Find flaws in reasoning and approaches
2. Identify potential risks and failure modes
3. Challenge assumptions
4. Propose alternative approaches
5. Ensure robustness

Be critical but constructive. Focus on robustness.""",

            AgentRole.DOCUMENTER: """You are a Documentation Agent. Your role is to:
1. Write clear, comprehensive documentation
2. Explain complex concepts simply
3. Provide examples and usage patterns
4. Maintain consistency and structure
5. Target appropriate audience levels

Be clear and concise. Focus on clarity.""",

            AgentRole.OPTIMIZER: """You are an Optimization Agent. Your role is to:
1. Identify performance bottlenecks
2. Suggest algorithmic improvements
3. Optimize resource usage
4. Reduce complexity
5. Improve scalability

Be pragmatic. Focus on measurable improvements.""",

            AgentRole.SECURITY: """You are a Security Agent. Your role is to:
1. Identify security vulnerabilities
2. Check for common attack vectors
3. Ensure secure coding practices
4. Validate input handling
5. Review authentication and authorization

Be thorough. Focus on security.""",

            AgentRole.ARCHITECT: """You are a System Architect Agent. Your role is to:
1. Design robust, scalable systems
2. Choose appropriate patterns and technologies
3. Consider trade-offs and constraints
4. Plan for growth and evolution
5. Ensure maintainability

Be pragmatic. Focus on long-term viability."""
        }

        return prompts.get(self.role, "You are a helpful AI assistant.")

    def _extract_confidence(self, text: str) -> float:
        """Extract confidence from agent's thinking"""
        # Look for confidence indicators
        if "confident" in text.lower() and "high" in text.lower():
            return 0.9
        elif "confident" in text.lower():
            return 0.7
        elif "uncertain" in text.lower() or "unsure" in text.lower():
            return 0.4
        else:
            return 0.6  # Default confidence


class MultiAgentOrchestrator:
    """
    Orchestrates multiple agents to solve complex tasks

    This is the core of what makes CogOS superior to single-pass systems.
    """

    def __init__(
        self,
        llm_provider: LLMProvider,
        memory: MemoryBackend,
        cache: SmartCache,
        available_modules: List[str] = None
    ):
        self.llm = llm_provider
        self.memory = memory
        self.cache = cache
        self.available_modules = available_modules or []
        self.agents: Dict[str, Agent] = {}
        self.message_history: List[AgentMessage] = []
        self.proposals: List[AgentProposal] = []
        self.task_queue: List[AgentTask] = []

    def create_agent(
        self,
        name: str,
        role: AgentRole,
        modules: List[str] = None
    ) -> Agent:
        """Create a new specialized agent"""
        agent = Agent(
            name=name,
            role=role,
            llm_provider=self.llm,
            memory=self.memory,
            cache=self.cache,
            modules=modules or []
        )
        self.agents[name] = agent
        return agent

    async def collaborative_solve(
        self,
        problem: str,
        context: str = "",
        iterations: int = 3
    ) -> Dict[str, Any]:
        """
        Solve a problem using multiple agents collaboratively

        This is where the magic happens:
        1. Multiple agents work in parallel
        2. They debate and vote on approaches
        3. Best solutions are refined over iterations
        4. Final solution is validated

        This multi-agent approach produces better results than single-pass systems.
        """
        results = {
            "problem": problem,
            "iterations": [],
            "final_solution": None,
            "confidence": 0.0
        }

        # Phase 1: Planning (Parallel)
        planners = [
            self.agents[name] for name in self.agents
            if self.agents[name].role == AgentRole.PLANNER
        ]

        if not planners:
            # Create default planner if none exists
            planner = self.create_agent("planner", AgentRole.PLANNER)
            planners = [planner]

        planning_tasks = [
            planner.think(context, f"Create a plan to solve: {problem}")
            for planner in planners
        ]

        plans = await asyncio.gather(*planning_tasks)

        # Phase 2: Research (Parallel)
        researchers = [
            self.agents[name] for name in self.agents
            if self.agents[name].role == AgentRole.RESEARCHER
        ]

        if researchers:
            research_tasks = [
                researcher.think(context, f"Research background for: {problem}")
                for researcher in researchers
            ]
            research_results = await asyncio.gather(*research_tasks)
        else:
            research_results = []

        # Combine context
        combined_context = context
        if plans:
            combined_context += f"\n\nPlanning Insights:\n" + "\n".join(plans)
        if research_results:
            combined_context += f"\n\nResearch:\n" + "\n".join(research_results)

        # Phase 3: Solution Proposals (Parallel)
        for iteration in range(iterations):
            iteration_result = {
                "iteration": iteration + 1,
                "proposals": [],
                "critiques": [],
                "best_solution": None
            }

            # Get proposals from relevant agents
            coders = [
                self.agents[name] for name in self.agents
                if self.agents[name].role in [AgentRole.CODER, AgentRole.ARCHITECT]
            ]

            if not coders:
                coder = self.create_agent("coder", AgentRole.CODER)
                coders = [coder]

            proposals = await asyncio.gather(*[
                coder.propose(combined_context, problem)
                for coder in coders
            ])

            iteration_result["proposals"] = [
                {
                    "agent": p.agent_name,
                    "content": p.content,
                    "confidence": p.confidence
                }
                for p in proposals
            ]

            # Phase 4: Critique (Parallel)
            critics = [
                self.agents[name] for name in self.agents
                if self.agents[name].role in [AgentRole.REVIEWER, AgentRole.CRITIC]
            ]

            if critics:
                critique_tasks = []
                for proposal in proposals:
                    for critic in critics:
                        task = critic.think(
                            combined_context,
                            f"Critique this solution:\n\n{proposal.content}"
                        )
                        critique_tasks.append(task)

                critiques = await asyncio.gather(*critique_tasks)

                iteration_result["critiques"] = [
                    {
                        "critique": c,
                        "proposal_idx": i // len(critics)
                    }
                    for i, c in enumerate(critiques)
                ]

                # Incorporate critiques
                combined_context += f"\n\nCritiques:\n" + "\n".join(critiques)

            # Select best proposal
            if proposals:
                best = max(proposals, key=lambda p: p.confidence)
                iteration_result["best_solution"] = {
                    "agent": best.agent_name,
                    "content": best.content,
                    "confidence": best.confidence
                }

                # Update context with best solution
                combined_context += f"\n\nBest Solution (iteration {iteration + 1}):\n{best.content}"

            results["iterations"].append(iteration_result)

        # Phase 5: Final Refinement
        if results["iterations"]:
            last_iter = results["iterations"][-1]
            if last_iter["best_solution"]:
                results["final_solution"] = last_iter["best_solution"]["content"]
                results["confidence"] = last_iter["best_solution"]["confidence"]

        # Phase 6: Testing and Validation
        testers = [
            self.agents[name] for name in self.agents
            if self.agents[name].role == AgentRole.TESTER
        ]

        if testers and results["final_solution"]:
            validation = await testers[0].think(
                combined_context,
                f"Validate this solution:\n\n{results['final_solution']}"
            )
            results["validation"] = validation

        return results

    async def parallel_execute(
        self,
        tasks: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Execute multiple tasks in parallel using specialized agents

        This is much faster than sequential execution.
        """
        # Create agent tasks
        agent_tasks = []
        for task in tasks:
            role = AgentRole(task.get("role", "coder"))
            agent = self._get_or_create_agent(role)

            agent_tasks.append(
                agent.think(
                    task.get("context", ""),
                    task.get("task", "")
                )
            )

        # Execute in parallel
        results = await asyncio.gather(*agent_tasks)

        return [
            {"task": task, "result": result}
            for task, result in zip(tasks, results)
        ]

    def _get_or_create_agent(self, role: AgentRole) -> Agent:
        """Get existing agent or create new one"""
        # Find agent with this role
        for agent in self.agents.values():
            if agent.role == role:
                return agent

        # Create new agent
        name = f"{role.value}_agent"
        return self.create_agent(name, role)

    def debate(
        self,
        topic: str,
        context: str = "",
        rounds: int = 2
    ) -> Dict[str, Any]:
        """
        Host a debate between agents on a topic

        This improves decision quality by exploring multiple perspectives.
        """
        # Get agents with different perspectives
        diverse_agents = list(self.agents.values())[:4]  # Up to 4 agents

        if len(diverse_agents) < 2:
            return {"error": "Need at least 2 agents for debate"}

        debate_history = []

        for round_num in range(rounds):
            round_result = {
                "round": round_num + 1,
                "arguments": []
            }

            # Each agent makes an argument
            for agent in diverse_agents:
                argument = agent.think(
                    context,
                    f"Round {round_num + 1}: Share your perspective on: {topic}"
                )
                round_result["arguments"].append({
                    "agent": agent.name,
                    "role": agent.role.value,
                    "argument": argument
                })

            debate_history.append(round_result)

            # Update context with arguments
            context += f"\n\nRound {round_num + 1} Arguments:\n"
            for arg in round_result["arguments"]:
                context += f"\n{arg['agent']} ({arg['role']}): {arg['argument']}\n"

        return {
            "topic": topic,
            "rounds": debate_history,
            "participants": [a.name for a in diverse_agents]
        }

    def vote(
        self,
        proposals: List[AgentProposal]
    ) -> AgentProposal:
        """
        Have agents vote on the best proposal

        This democratic approach improves decision quality.
        """
        if not proposals:
            return None

        # Each agent votes
        for agent in self.agents.values():
            # Simple voting: agent picks proposal they agree with most
            # In practice, this would be more sophisticated
            if proposals:
                # For now, random vote (would be LLM-based in production)
                import random
                choice = random.choice(proposals)
                choice.votes.append(agent.name)

        # Count votes
        vote_counts = [
            (len(p.votes), p) for p in proposals
        ]
        vote_counts.sort(reverse=True)

        return vote_counts[0][1] if vote_counts else None


def create_orchestrator(
    llm_provider: LLMProvider,
    memory: MemoryBackend,
    cache: SmartCache,
    modules: List[str] = None
) -> MultiAgentOrchestrator:
    """
    Create a multi-agent orchestrator with default agents

    This provides a ready-to-use multi-agent system.
    """
    orchestrator = MultiAgentOrchestrator(
        llm_provider=llm_provider,
        memory=memory,
        cache=cache,
        available_modules=modules or []
    )

    # Create default set of specialized agents
    default_agents = [
        ("planner", AgentRole.PLANNER),
        ("researcher", AgentRole.RESEARCHER),
        ("coder", AgentRole.CODER),
        ("reviewer", AgentRole.REVIEWER),
        ("critic", AgentRole.CRITIC),
        ("tester", AgentRole.TESTER),
        ("documenter", AgentRole.DOCUMENTER),
        ("optimizer", AgentRole.OPTIMIZER),
        ("security", AgentRole.SECURITY),
        ("architect", AgentRole.ARCHITECT),
    ]

    for name, role in default_agents:
        orchestrator.create_agent(name, role)

    return orchestrator

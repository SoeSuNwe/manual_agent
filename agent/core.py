"""
Agent Core - The main ReAct loop for the autonomous agent.
Implements: Observe → Think → Act → Repeat
"""

import json
from typing import Optional
from llm.hf_model import run_llm
from agent.prompts import get_system_prompt, get_observation_prompt
from agent.dispatcher import parse_llm_response, dispatch_action, is_final_answer


class AutonomousAgent:
    """
    Autonomous agent that uses ReAct pattern to solve location queries.
    The LLM decides which tools to call and when.
    """
    
    def __init__(self, max_iterations: int = 10, verbose: bool = True):
        """
        Initialize the agent.
        
        Args:
            max_iterations: Maximum number of reasoning steps (prevents infinite loops)
            verbose: Whether to print detailed reasoning steps
        """
        self.max_iterations = max_iterations
        self.verbose = verbose
        self.conversation_history = []
    
    def run(self, user_query: str) -> dict:
        """
        Run the agent on a user query.
        
        Args:
            user_query: The user's location description/query
            
        Returns:
            Dict with location information (name, city, country, latlong)
        """
        if self.verbose:
            print("\n🤖 Autonomous Agent Started")
            print("=" * 50)
        
        # Initialize conversation with system prompt and user query
        system_prompt = get_system_prompt()
        self.conversation_history = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Find complete location information for: {user_query}"}
        ]
        
        iteration = 0
        final_result = None
        
        while iteration < self.max_iterations:
            iteration += 1
            
            if self.verbose:
                print(f"\n📍 Step {iteration}/{self.max_iterations}")
                print("-" * 30)
            
            # Get LLM response
            prompt = self._build_prompt()
            response = run_llm(prompt)
            
            if self.verbose:
                print(f"🧠 LLM Response:\n{response}")
            
            # Parse the response
            thought, action, parameters = parse_llm_response(response)
            
            if not action:
                if self.verbose:
                    print("⚠️ No action found in response, retrying...")
                # Add guidance and retry
                self.conversation_history.append({
                    "role": "assistant",
                    "content": response
                })
                self.conversation_history.append({
                    "role": "user",
                    "content": "Please respond with THOUGHT, ACTION, and PARAMETERS in the correct format."
                })
                continue
            
            if self.verbose and thought:
                print(f"\n💭 Thought: {thought}")
            
            # Check if this is the final answer
            if is_final_answer(action):
                if self.verbose:
                    print("\n✅ Final answer reached!")
                final_result = parameters
                break
            
            # Execute the tool
            if self.verbose:
                print(f"\n🔧 Action: {action}")
            
            tool_result = dispatch_action(action, parameters)
            
            # Add to conversation history
            self.conversation_history.append({
                "role": "assistant",
                "content": response
            })
            self.conversation_history.append({
                "role": "user",
                "content": get_observation_prompt(action, tool_result)
            })
        
        if final_result is None:
            if self.verbose:
                print("\n⚠️ Max iterations reached without final answer")
            final_result = {
                "name": None,
                "city": None,
                "country": None,
                "latlong": None,
                "error": "Max iterations reached"
            }
        
        if self.verbose:
            print("\n" + "=" * 50)
            print("🏁 Agent Completed")
        
        return final_result
    
    def _build_prompt(self) -> str:
        """Build the full prompt from conversation history."""
        prompt_parts = []
        
        for msg in self.conversation_history:
            role = msg["role"]
            content = msg["content"]
            
            if role == "system":
                prompt_parts.append(f"System Instructions:\n{content}\n")
            elif role == "user":
                prompt_parts.append(f"User: {content}\n")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}\n")
        
        return "\n".join(prompt_parts)

"""
Tool Dispatcher - Parses LLM responses and executes corresponding tools.
"""

import re
import json
from typing import Tuple, Optional
from tools.registry import execute_tool


def parse_llm_response(response: str) -> Tuple[Optional[str], Optional[str], Optional[dict]]:
    """
    Parse the LLM response to extract THOUGHT, ACTION, and PARAMETERS.
    
    Returns:
        Tuple of (thought, action_name, parameters)
    """
    thought = None
    action = None
    parameters = None
    
    # Extract THOUGHT
    thought_match = re.search(r"THOUGHT:\s*(.+?)(?=ACTION:|$)", response, re.DOTALL | re.IGNORECASE)
    if thought_match:
        thought = thought_match.group(1).strip()
    
    # Extract ACTION
    action_match = re.search(r"ACTION:\s*(\w+)", response, re.IGNORECASE)
    if action_match:
        action = action_match.group(1).strip()
    
    # Extract PARAMETERS
    params_match = re.search(r"PARAMETERS:\s*(\{.+?\})", response, re.DOTALL | re.IGNORECASE)
    if params_match:
        try:
            parameters = json.loads(params_match.group(1))
        except json.JSONDecodeError:
            # Try to fix common JSON issues
            param_str = params_match.group(1)
            param_str = param_str.replace("'", '"')  # Replace single quotes
            try:
                parameters = json.loads(param_str)
            except json.JSONDecodeError:
                parameters = {}
    
    return thought, action, parameters


def dispatch_action(action: str, parameters: dict) -> str:
    """
    Dispatch the action to the appropriate tool and return the result.
    
    Args:
        action: The name of the tool to execute
        parameters: The parameters to pass to the tool
        
    Returns:
        The result of the tool execution as a string
    """
    if not action:
        return "Error: No action specified"
    
    if parameters is None:
        parameters = {}
    
    print(f"  🔧 Executing: {action}")
    print(f"  📥 Parameters: {json.dumps(parameters, indent=2)}")
    
    result = execute_tool(action, parameters)
    
    print(f"  📤 Result: {result[:200]}..." if len(result) > 200 else f"  📤 Result: {result}")
    
    return result


def is_final_answer(action: str) -> bool:
    """Check if the action is the final answer."""
    return action and action.lower() == "final_answer"

"""
Autonomous Location Agent - Uses ReAct pattern to extract location information.
The LLM decides which tools to call and when.
"""

from agent.core import AutonomousAgent

def main():
    print("=" * 60)
    print("🤖 AUTONOMOUS LOCATION AGENT")
    print("=" * 60)
    print("This agent autonomously decides how to find location info.")
    print("It will think, choose tools, and iterate until complete.\n")
    
    description = input("Enter location description: ")
    
    # Create and run the autonomous agent
    agent = AutonomousAgent(max_iterations=10, verbose=True)
    result = agent.run(description)
    
    print("\n" + "=" * 60)
    print("📍 FINAL RESULT")
    print("=" * 60)
    print(result)


if __name__ == "__main__":
    main()

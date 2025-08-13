# Diagnosis-Agent

class DiagnosisAgent:
    def __init__(self):
        # Initialize any necessary components for the Diagnosis Agent
        pass

    def analyze_request(self, user_prompt: str) -> dict:
        """
        Analyzes the user's request to classify its nature, determine the appropriate
        operational mode (Chat, Agent, Plan), and identify the target profile and role.
        Aims to classify 'at the speed of light'.
        """
        analysis_result = {
            "original_prompt": user_prompt,
            "classified_nature": "unknown",
            "operational_mode": "unknown",
            "target_profile": "unknown",
            "target_role": "unknown",
            "confidence_score": 0.0
        }
        print(f"Analyzing request: {user_prompt}")

        # Enhanced simulation of analysis logic
        prompt_lower = user_prompt.lower()

        if "hello" in prompt_lower or "hi" in prompt_lower or "hey" in prompt_lower:
            analysis_result["classified_nature"] = "greeting"
            analysis_result["operational_mode"] = "Chat"
            analysis_result["target_profile"] = "General"
            analysis_result["target_role"] = "Chat-Agent"
            analysis_result["confidence_score"] = 0.95
        elif "summarize" in prompt_lower or "explain" in prompt_lower or "what is" in prompt_lower or "tell me about" in prompt_lower:
            analysis_result["classified_nature"] = "information_request"
            analysis_result["operational_mode"] = "Agent"
            analysis_result["target_profile"] = "Productivity"
            analysis_result["target_role"] = "Writing-Agent" # Could also be Teacher-Agent
            analysis_result["confidence_score"] = 0.90
        elif "develop" in prompt_lower or "create code" in prompt_lower or "plan" in prompt_lower or "design" in prompt_lower or "implement" in prompt_lower:
            analysis_result["classified_nature"] = "development_task"
            analysis_result["operational_mode"] = "Plan"
            analysis_result["target_profile"] = "Developer"
            analysis_result["target_role"] = "Architect-Agent" # Or Planner-Agent
            analysis_result["confidence_score"] = 0.95
        elif "debug" in prompt_lower or "fix error" in prompt_lower or "solve problem" in prompt_lower:
            analysis_result["classified_nature"] = "debugging_task"
            analysis_result["operational_mode"] = "Plan" # Debugging often requires planning
            analysis_result["target_profile"] = "Developer"
            analysis_result["target_role"] = "Debug-Agent"
            analysis_result["confidence_score"] = 0.90
        elif "analyze" in prompt_lower or "research" in prompt_lower:
            analysis_result["classified_nature"] = "research_task"
            analysis_result["operational_mode"] = "Plan" # Research often requires planning
            analysis_result["target_profile"] = "Developer"
            analysis_result["target_role"] = "Research-Agent"
            analysis_result["confidence_score"] = 0.85
        else:
            # Default for general queries or unrecognized patterns
            analysis_result["classified_nature"] = "general_query"
            analysis_result["operational_mode"] = "Chat"
            analysis_result["target_profile"] = "General"
            analysis_result["target_role"] = "Chat-Agent"
            analysis_result["confidence_score"] = 0.75

        return analysis_result

    def classify_intent(self, user_prompt: str) -> str:
        """
        Classifies the user's intent, which helps in determining the operational mode.
        This is a simplified helper function.
        """
        prompt_lower = user_prompt.lower()
        if "hello" in prompt_lower or "hi" in prompt_lower or "hey" in prompt_lower:
            return "greeting"
        elif "summarize" in prompt_lower or "explain" in prompt_lower or "what is" in prompt_lower or "tell me about" in prompt_lower:
            return "information_request"
        elif "develop" in prompt_lower or "create code" in prompt_lower or "plan" in prompt_lower or "design" in prompt_lower or "implement" in prompt_lower:
            return "development_task"
        elif "debug" in prompt_lower or "fix error" in prompt_lower or "solve problem" in prompt_lower:
            return "debugging_task"
        elif "analyze" in prompt_lower or "research" in prompt_lower:
            return "research_task"
        else:
            return "general_query"

    def determine_operational_mode(self, classified_nature: str) -> str:
        """
        Determines the operational mode based on the classified nature of the request.
        """
        if classified_nature in ["greeting", "general_query"]:
            return "Chat"
        elif classified_nature == "information_request":
            return "Agent"
        elif classified_nature in ["development_task", "debugging_task", "research_task"]:
            return "Plan"
        else:
            return "Chat" # Default to Chat mode

    def determine_target_profile_and_role(self, classified_nature: str) -> tuple[str, str]:
        """
        Determines the target profile and role based on the classified nature.
        """
        if classified_nature == "greeting":
            return "General", "Chat-Agent"
        elif classified_nature == "information_request":
            return "Productivity", "Writing-Agent" # Or Teacher-Agent
        elif classified_nature == "development_task":
            return "Developer", "Architect-Agent" # Or Planner-Agent
        elif classified_nature == "debugging_task":
            return "Developer", "Debug-Agent"
        elif classified_nature == "research_task":
            return "Developer", "Research-Agent"
        else:
            return "General", "Chat-Agent" # Default

# Example of how this agent might be used by the Orchestration Engine:
# diagnosis_agent = DiagnosisAgent()
# user_input = "Can you help me plan a new feature?"
# analysis = diagnosis_agent.analyze_request(user_input)
# print(analysis)

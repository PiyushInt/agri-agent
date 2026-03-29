class AgriculturalGuardrails:
    """
    Guardrails engine to enforce compliance and safety in agricultural advice.
    """
    
    DISALLOWED_CHEMICALS = ["DDT", "Endosulfan", "Paraquat", "Monocrotophos"]
    DISCLAIMER = "\n\n⚠️ Disclaimer: I am an AI advisor. Please consult local agricultural extension officers before applying any new treatments or chemicals."

    def __init__(self, logger):
        self.logger = logger

    def check_input(self, session_id: str, user_input: str) -> bool:
        """
        Check if user input is asking for something completely outside the domain or malicious.
        (A real implementation would use LLM for semantic checking here.)
        """
        user_input_lower = user_input.lower()
        if "bomb" in user_input_lower or "hack" in user_input_lower:
            self.logger.log_guardrail_check(session_id, "Input Check", "DENIED", "Malicious or out-of-domain request.")
            return False
            
        self.logger.log_guardrail_check(session_id, "Input Check", "PASSED", "Input is safe and related to agriculture.")
        return True

    def check_output(self, session_id: str, agent_output: str) -> str:
        """
        Check the final output to ensure no banned chemicals are recommended
        and that a disclaimer is attached.
        """
        # 1. Chemical Guardrail
        for chemical in self.DISALLOWED_CHEMICALS:
            if chemical.lower() in agent_output.lower():
                self.logger.log_guardrail_check(session_id, "Output Check", "DENIED", f"Output contained banned chemical: {chemical}")
                # We could rewrite it or just return a canned response
                return "The advice generated contained references to locally banned or restricted chemicals. I cannot provide this recommendation."
        
        # 2. Disclaimer Guardrail
        if "Disclaimer" not in agent_output:
            agent_output += self.DISCLAIMER
            self.logger.log_guardrail_check(session_id, "Output Check", "MODIFIED", "Appended compliance disclaimer.")
        else:
            self.logger.log_guardrail_check(session_id, "Output Check", "PASSED", "Output meets compliance rules.")
            
        return agent_output

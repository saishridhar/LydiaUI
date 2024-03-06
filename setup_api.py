import os
def process_model(option,session):
        if option == "Qwen1.5-2B":
            session["model"] = "Qwen/Qwen1.5-1.8B-Chat"
            session["api_key"] = os.getenv("TOGETHER_API_KEY")
            session["api_base"] = os.getenv("TOGETHER_BASE")
            session["api_type"] = "together"

        if option == "Openchat-7B":
            session["model"] = "openchat/openchat-3.5-1210"
            session["api_key"] = os.getenv("TOGETHER_API_KEY")
            session["api_base"] = os.getenv("TOGETHER_BASE")
            session["api_type"] = "together"

        if option == "Qwen1.5-72B":
            session["model"] = "Qwen/Qwen1.5-72B-Chat"
            session["api_key"] = os.getenv("TOGETHER_API_KEY")
            session["api_base"] = os.getenv("TOGETHER_BASE")
            session["api_type"] = "together"
    
        if option == "Codellama-70B":
            session["model"] = "codellama/CodeLlama-70b-Instruct-hf"
            session["api_key"] = os.getenv("TOGETHER_API_KEY")
            session["api_base"] = os.getenv("TOGETHER_BASE")
            session["api_type"] = "together"
    
        if option == "GPT-4":
            session["model"] = "gpt-4-0125-preview"
            session["api_key"] = os.getenv("OPENAI_API_KEY")
            session["api_base"] = os.getenv("OPENAI_BASE")
            session["api_type"] = "openai"
    
        if option == "Opus":
            session["model"] = "claude-3-opus-20240229"
            session["api_key"] = os.getenv("ANTHROPIC_API_KEY")
            session["api_base"] = os.getenv("ANTHROPIC_BASE")
            session["api_type"] = "anthropic"
    
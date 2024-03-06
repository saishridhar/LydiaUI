import tiktoken
from transformers import AutoTokenizer
from transformers import GPT2TokenizerFast

def gpt4_pricing(text,state):
    enc = tiktoken.get_encoding("cl100k_base")
    tokens = (len(enc.encode(text)))
    if state == "input":
        return tokens*(10/1000000)
    if state == "output":
        return tokens*(30/1000000)


def together_pricing(model,text,state):
    tokenizer = AutoTokenizer.from_pretrained(model)
    tokens = (len(tokenizer.encode(text)))
    if model == "Qwen/Qwen1.5-1.8B-Chat":
        if state == "input":
            return tokens*(0.1/1000000)
        if state == "output":
            return tokens*(0.1/1000000)
        pass
    elif model == "Qwen/Qwen1.5-72B-Chat":
        if state == "input":
            return tokens*(0.9/1000000)
        if state == "output":
            return tokens*(0.9/1000000)
        pass
    elif model == "codellama/CodeLlama-70b-Instruct-hf":
        if state == "input":
            return tokens*(0.9/1000000)
        if state == "output":
            return tokens*(0.9/1000000)
        pass
    elif model == "openchat/openchat-3.5-1210":
        if state == "input":
            return tokens*(0.2/1000000)
        if state == "output":
            return tokens*(0.2/1000000)
        pass



def anthropic_pricing(text,state):
    tokenizer = GPT2TokenizerFast.from_pretrained('Xenova/claude-tokenizer')
    tokens = len(tokenizer.encode(text))
    if state == "input":
            return tokens*(15/1000000)
    if state == "output":
            return tokens*(75/1000000)
    

def get_price(api_type,text,state,model = None):
    if api_type == "openai":
        return gpt4_pricing(text,state)
    elif api_type == "anthropic":
        return anthropic_pricing(text,state)
    elif api_type == "together":
        return together_pricing(model,text,state)

     

#print(f'''{gpt4_pricing("What is your name","input"):3f}''')
#print(together_pricing("openchat/openchat-3.5-1210","What is your name","input"))
#print(anthropic_pricing("What is your name","input"))



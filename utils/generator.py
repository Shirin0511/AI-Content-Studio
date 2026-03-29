from groq import Groq
from config import GROQ_API_KEY, MODEL_NAME, MAX_TOKENS
from prompts.templates import get_prompts, get_improvement_prompt


client = Groq(api_key=GROQ_API_KEY)

def generate_content(content_type: str, topic:str) -> str:

    prompt = get_prompts(content_type,topic)

    if not prompt:
        return "Unsupported Content Type" 
    
    try:
        response = client.chat.completions.create(
            model = MODEL_NAME,
            max_tokens = MAX_TOKENS,
            messages=[
                {
                    "role":"system",
                    "content" : "Your a professional Content Writer. Write high quality, ready-to-use content."
                },
                {
                    "role" : "user",
                    "content" : prompt
                }
            ]
        )

        result =  response.choices[0].message.content.strip()

        if not result:
            return "Error: Received empty response. Try Again later!"
        
        return result
    
    except Exception as e:
        error = str(e)
        if "rate_limit" in error.lower():
            return "Error: Rate Limit reached. Please try again later."
        
        if "api_key" in error.lower():
            return "Error: Invalied API key."
        
        if "model_decommissioned" or "model not found" in error.lower():
            return "Error: Model Unavailable."
        
        else:
            return f"Error: Something went wrong - {error}"
    

def generate_variations(content_type: str, topic: str) -> str:
    results= []

    for _ in range(3):
        content = generate_content(content_type, topic)
        results.append(content)

    return results


def improve_content(content_type: str, draft:str) -> str:

    prompt= get_improvement_prompt(content_type, draft)

    try:
        response = client.chat.completions.create(
            model = MODEL_NAME,
            max_tokens = MAX_TOKENS,
            messages=[
                {
                    "role":"system",
                    "content" : "Your a professional Content Writer. Write high quality, ready-to-use content."
                },
                {
                    "role" : "user",
                    "content" : prompt
                }
            ]
        )

        result =  response.choices[0].message.content.strip()

        if not result:
            return "Error: Receieved an empty response"
        
        return result
    
    except Exception as e:

        error = str(e)
        if "rate_limit" in error.lower():
            return "Error: rate limit reached. Please wait a few seconds and try again."
        elif "api_key" in error.lower() or "authentication" in error.lower():
            return "Error: invalid API key. Please check your .env file."
        else:
            return f"Error: something went wrong — {error}"



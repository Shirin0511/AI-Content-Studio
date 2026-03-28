from groq import Groq
from config import GROQ_API_KEY, MODEL_NAME, MAX_TOKENS
from prompts.templates import get_prompts

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
        
        if "model" in error.lower():
            return "Error: Model Unavailable."
        
        else:
            return f"Error: Something went wrong - {error}"
    

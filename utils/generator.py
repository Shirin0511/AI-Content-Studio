from groq import Groq
from config import GROQ_API_KEY, MODEL_NAME, MAX_TOKENS
from prompts.templates import get_prompts

client = Groq(api_key=GROQ_API_KEY)

def generate_content(content_type: str, topic:str) -> str:

    prompt = get_prompts(content_type,topic)

    if not prompt:
        return "Unsupported Content Type" 
    

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

    return response.choices[0].message.content.strip()

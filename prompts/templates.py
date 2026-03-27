def get_prompts(content_type: str, topic:str) -> str:
    prompts={

        "Blog Post": f"""Write a professional blog post about: {topic}

Structure it with:
- An engaging introduction
- 3-4 main sections with subheadings
- A clear conclusion

Tone: professional, informative, engaging.
Length: 400-500 words.""",

        "LinkedIn Caption": f"""Write a professional LinkedIn post about: {topic}

Requirements:
- Hook in the first line to stop scrolling
- 3-5 short punchy paragraphs
- End with a question to drive engagement
- Add 3-5 relevant hashtags at the end

Tone: professional but conversational.
Length: 150-200 words.""",

        "Cold Email": f"""Write a professional cold email about: {topic}

Structure:
- Subject line (write it as: Subject: ...)
- Personalized opening line
- Clear value proposition in 2-3 sentences
- Specific call to action
- Professional sign-off

Tone: confident, concise, respectful.
Length: 100-150 words."""

    }

    return prompts.get(content_type,"")
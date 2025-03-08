from openai import OpenAI
import re

def llm_call(prompt: str, system_prompt: str = "", model="gpt-3.5-turbo") -> str:
    """
    Calls the model with the given prompt and returns the response.

    Args:
        prompt (str): The user prompt to send to the model.
        system_prompt (str, optional): The system prompt to send to the model. Defaults to "".
        model (str, optional): The model to use for the call. Defaults to "claude-3-5-sonnet-20241022".

    Returns:
        str: The response from the language model.
    """
    # if model in ['qwen2.5:7b']
    open_ai_model_name_list = [
        'o3-mini',
        'gpt-3.5-turbo',
                                'gpt-4o', 'gpt-4o-mini', 'gpt-4o-2024-08-06', 
                                'gpt-4o-2024-05-13', 'gpt-4o-2024-02-15', 'gpt-4o-2024-02-15', 'gpt-4o-2024-02-15', 
                                'gpt-4o-2024-02-15', ]
    if model not in open_ai_model_name_list:
        openai_api_key = "EMPTY"
        # openai_api_base = 'http://localhost:11434/v1/'
        openai_api_base = 'http://34.240.68.65:80/v1'
        client = OpenAI(
            api_key=openai_api_key,
            base_url=openai_api_base,
        )
    else:
        client = OpenAI()
    completion = client.chat.completions.create(
        model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            # , reasoning_effort="high", 
        )
    return completion.choices[0].message.content


def extract_xml(text: str, tag: str) -> str:
    """
    Extracts the content of the specified XML tag from the given text. Used for parsing structured responses 

    Args:
        text (str): The text containing the XML.
        tag (str): The XML tag to extract content from.

    Returns:
        str: The content of the specified XML tag, or an empty string if the tag is not found.
    """
    match = re.search(f'<{tag}>(.*?)</{tag}>', text, re.DOTALL)
    return match.group(1) if match else ""
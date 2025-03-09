from openai import OpenAI
import re
from src.utils.logging_utils import get_logger
from dotenv import load_dotenv
import os

# Set up logger
logger = get_logger("src.llm_call")

# Try to load environment variables from .env file
load_dotenv()

# Check if Langfuse is available and configured
try:
    from langfuse import Langfuse
    LANGFUSE_PUBLIC_KEY = os.environ.get("LANGFUSE_PUBLIC_KEY")
    LANGFUSE_SECRET_KEY = os.environ.get("LANGFUSE_SECRET_KEY")
    
    if LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY:
        langfuse = Langfuse()
        LANGFUSE_ENABLED = True
        logger.info("Langfuse tracking enabled")
    else:
        LANGFUSE_ENABLED = False
        logger.info("Langfuse tracking disabled: missing API keys")
except ImportError:
    LANGFUSE_ENABLED = False
    logger.info("Langfuse tracking disabled: package not installed")

def llm_call(prompt: str, system_prompt: str = "", model="gpt-3.5-turbo") -> str:
    """
    Calls the model with the given prompt and returns the response.

    Args:
        prompt (str): The user prompt to send to the model.
        system_prompt (str, optional): The system prompt to send to the model. Defaults to "".
        model (str, optional): The model to use for the call. Defaults to "gpt-3.5-turbo".

    Returns:
        str: The response from the language model.
    """
    logger.info(f"Calling LLM with model: {model}")
    logger.debug(f"Prompt: {prompt[:100]}...")
    logger.debug(f"System prompt: {system_prompt[:100]}...")
    
    # if model in ['qwen2.5:7b']
    open_ai_model_name_list = [
        'o3-mini',
        'gpt-3.5-turbo',
        'gpt-4o', 'gpt-4o-mini', 'gpt-4o-2024-08-06', 
        'gpt-4o-2024-05-13', 'gpt-4o-2024-02-15', 'gpt-4o-2024-02-15', 'gpt-4o-2024-02-15', 
        'gpt-4o-2024-02-15', ]
    
    if model not in open_ai_model_name_list:
        logger.debug(f"Using custom API endpoint for model: {model}")
        openai_api_key = "EMPTY"
        openai_api_base = 'http://localhost:11434/v1/'
        # openai_api_base = 'http://34.240.68.65:80/v1'
        client = OpenAI(
            api_key=openai_api_key,
            base_url=openai_api_base,
        )
    else:
        logger.debug("Using default OpenAI client")
        client = OpenAI()

    try:
        logger.debug("Sending request to LLM API")
        
        # Initialize Langfuse tracking if enabled
        generation = None
        if LANGFUSE_ENABLED:
            try:
                generation = langfuse.generation(
                    name=f"llm_call_{model}",
                    input=prompt,
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ]
                )
            except Exception as e:
                logger.warning(f"Failed to initialize Langfuse tracking: {str(e)}")
        
        # Make the actual API call
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            stop=["Observation:"]  # Let's stop before any actual function is called
        )
        
        response = completion.choices[0].message.content
        
        # Record the response in Langfuse if tracking is enabled
        if LANGFUSE_ENABLED and generation:
            try:
                # Add metadata to the generation
                # generation.update(
                #     metadata={
                #         "model": model,
                #         "prompt_length": len(prompt),
                #         "response_length": len(response),
                #         "system_prompt_length": len(system_prompt),
                #         "timestamp": datetime.datetime.now().isoformat()
                #     }
                # )
                generation.end(output=response)
                langfuse.flush()
            except Exception as e:
                logger.warning(f"Failed to record response in Langfuse: {str(e)}")
        
        logger.debug(f"Received response from LLM: {response[:100]}...")
        return response
    except Exception as e:
        logger.error(f"Error calling LLM: {str(e)}", exc_info=True)
        raise


def extract_xml(text: str, tag: str) -> str:
    """
    Extracts the content of the specified XML tag from the given text. Used for parsing structured responses 

    Args:
        text (str): The text containing the XML.
        tag (str): The XML tag to extract content from.

    Returns:
        str: The content of the specified XML tag, or an empty string if the tag is not found.
    """
    logger.debug(f"Extracting XML tag '{tag}' from text")
    match = re.search(f'<{tag}>(.*?)</{tag}>', text, re.DOTALL)
    result = match.group(1) if match else ""
    if not result:
        logger.warning(f"Tag '{tag}' not found in text")
    else:
        logger.debug(f"Extracted content: {result[:100]}...")
    return result
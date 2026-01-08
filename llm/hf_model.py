import warnings
import logging
import os
from dotenv import load_dotenv
from openai import AzureOpenAI

# Suppress warnings and logs
warnings.filterwarnings("ignore")

# Load environment variables from .env file
load_dotenv()

# Initialize Azure OpenAI client with environment variables
client = AzureOpenAI(
    api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-15-preview",
    azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT")
)

def run_llm(prompt):
    # Try multiple common deployment names
    deployment_names = [
        os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4"),
        "gpt-4",
        "gpt-35-turbo", 
        "gpt-4-turbo",
        "gpt-4o",
        "gpt-35-turbo-16k"
    ]
    
    for deployment_name in deployment_names:
        if deployment_name:  # Skip None values
            try:
                response = client.chat.completions.create(
                    model=deployment_name,
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=200,
                    temperature=0.7
                )
                return response.choices[0].message.content
            except Exception as e:
                if "DeploymentNotFound" in str(e):
                    continue  # Try next deployment name
                else:
                    print(f"Error calling Azure OpenAI API with {deployment_name}: {e}")
                    break
    
    return f"Error: Unable to find a working deployment. Please check your Azure OpenAI deployment names."

import os
from mistralai import Mistral
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the API key
api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    raise ValueError("MISTRAL_API_KEY not found in environment variables")

# Initialize Mistral client
model = "mistral-large-latest"
client = Mistral(api_key=api_key)

def chat_with_mistral(message):
    try:
        chat_response = client.chat.complete(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": message,
                }
            ]
        )
        return chat_response.choices[0].message.content
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None

# Example usage
if __name__ == "__main__":
    # Read the contents of prompt.txt
    with open("/mnt/c/free-genai-bootcamp-2025/writing-practice/mistralAI-sentence-gen/prompt-test-connectivity.txt", "r") as file:
        user_message = file.read().strip()  # Read and strip any extra whitespace
    print("\nAsking Mistral AI:", user_message)
    response = chat_with_mistral(user_message)
    print("\nMistral AI response:", response)
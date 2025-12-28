import os
import time
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# 1. Load the .env file
# This will now work because you moved the file into the hire-light folder
load_dotenv()

# 2. Initialize the model with LangChain
# LangChain automatically finds "GOOGLE_API_KEY" from your .env
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
    max_output_tokens=1024
)

def generate_safe(prompt):
    """
    Sends a prompt to Gemini 2.5 Flash while handling:
    - RPM (Requests Per Minute) by waiting 30 seconds
    - Rate Limit Errors (429) with exponential backoff
    """
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"--- Sending request to Gemini 2.5 Flash (Attempt {attempt + 1}) ---")
            
            # LangChain uses .invoke()
            response = llm.invoke(prompt)
            
            # SUCCESS: Wait 30 seconds to respect the 2 RPM limit
            print("Success! Waiting 30s before the next potential call...")
            time.sleep(30) 
            return response.content
            
        except Exception as e:
            # Handle the 429 "Too Many Requests" error specifically
            if "429" in str(e):
                wait_time = (2 ** attempt) * 60 
                print(f"⚠️ Rate limit hit! Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"❌ Error: {e}")
                break
    return None

# Execution
if __name__ == "__main__":
    test_prompt = "Explain the Pumping Lemma for Context-Free Languages in 3 simple bullet points."
    result = generate_safe(test_prompt)
    
    if result:
        print("\nAI RESPONSE:\n", result)
    else:
        print("\nFailed to get a response after retries.")
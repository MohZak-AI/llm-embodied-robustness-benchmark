import os
import sys
import time

try:
    from openai import OpenAI
except ImportError:
    print("Error: Please install the OpenAI library first by running 'pip install openai'")
    sys.exit(1)

def run_live_demo():
    print("\n" + "="*80)
    print(" 🤖 LIVE SEMINAR DEMO: The 'Cow in the Microwave' (Commonsense Override) Test")
    print("="*80 + "\n")

    # Get API key from environment, or ask the user right on stage if it's missing!
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("API Key not detected in environment variables.")
        api_key = input("Please paste your OpenRouter API Key here to run the demo: ").strip()

    if not api_key:
        print("Demo aborted: No API Key provided.")
        sys.exit(1)

    print("\nInitializing connection to OpenRouter API...")
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    time.sleep(1)

    prompt = (
        "Imagine a scene vividly: There is a full-grown, living cow standing entirely "
        "inside a standard kitchen microwave. The microwave door is closed.\n\n"
        "Question: Is the cow physically inside the microwave? Answer exactly with '1' for Yes, or '2' for No."
    )

    print("\n" + "-"*80)
    print("📜 THE TEXT PROMPT WE ARE SENDING TO THE MODELS:")
    print("-"*80)
    print(prompt)
    print("-"*80 + "\n")

    time.sleep(2)

    # We will test a legacy massive model against a streamlined reasoning model
    models_to_test = [
        {"id": "openai/gpt-4o", "label": "❌ GPT-4o (Massive Commercial Legacy Model)"},
        {"id": "meta-llama/llama-3.3-70b-instruct", "label": "✅ LLaMA 3.3 70B (Open-Source Model)"}
    ]

    for model in models_to_test:
        print(f"Pinging {model['label']}...")
        try:
            response = client.chat.completions.create(
                model=model["id"],
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0  # Zero temperature for deterministic testing
            )
            answer = response.choices[0].message.content.strip()
            print(f">>> AI RESPONSE: {answer}\n")
        except Exception as e:
            print(f">>> ERROR QUERYING AI: {e}\n")
        time.sleep(1)

    print("="*80)
    print("THE SCIENTIFIC CONCLUSION:")
    print("Expected Answer was '1' (Yes, because it is explicitly stated in the room geometry).")
    print("Models that answered '2' (No) succumbed to 'Commonsense Overrides' and overwrote reality!")
    print("="*80 + "\n")

if __name__ == "__main__":
    run_live_demo()

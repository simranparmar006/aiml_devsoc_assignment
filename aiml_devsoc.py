import json
import time
from groq import Groq

API_KEY=" " 
MODEL = "llama-3.3-70b-versatile"

INPUT_FILE_PATH="prompts.txt"
OUTPUT_FILE_PATH= "responses_generated.json"

MAX_RETRIES=5

def load_prompts(file_path):
    try:
        prompts=[]
        with open(file_path,"r",encoding="utf-8") as f:
            for line in f:
                line=line.strip()
                if line:
                    prompts.append(line)
            return prompts
    except FileNotFoundError:
        print(f"Error! File not found.{file_path}")
    except Exception as e:
        print(f"Error loading prompts: {e}")


def call_llm(client,prompt):
    for attempt in range(MAX_RETRIES):
        response=client.chat.completions.create(
            model=MODEL,
            messages=[{"role":"user","content":prompt}],
            timeout=60)

        response= response.choices[0].message.content
        return {"Response": response, "status": "SUCCESS"}


def process_prompts():
    #Initialize client
    client=Groq(api_key=API_KEY)

    #Load prompt and condition for prompt not found
    prompts=load_prompts(INPUT_FILE_PATH)
    if not prompts:
        print("Exiting as no prompts loaded.")
        return
    results=[]

    #Loop through prompts, send it to llm, save output in results
    for i, prompt in enumerate(prompts,start=1):
        print(f"Processing prompt {i}/{len(prompts)}...")
        
        response_data = call_llm(client, prompt)

        results.append({
            "prompt_number": i,
            "prompt": prompt,
            "status": response_data["status"],
            "response": response_data["Response"]
        })

        if response_data["status"] == "SUCCESS":
             time.sleep(0.5)

    with open(OUTPUT_FILE_PATH,"w",encoding="utf-8") as f:
        json.dump(results,f,indent=4, ensure_ascii="False")

    print(f"\n Responses saved to {OUTPUT_FILE_PATH}")

#Run the main function process_prompts
process_prompts()


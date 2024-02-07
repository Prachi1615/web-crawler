# python_script.py
import json
import os
import sys
from scipy.spatial.distance import cosine
from openai import OpenAI
import numpy as np
import pandas as pd

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def create_context(question, df, max_len=1800, size="ada"):
    """
    Create a context for a question by finding the most similar context from the dataframe
    """
    # Get the embeddings for the question
    q_embeddings = client.embeddings.create(input=question, model='text-embedding-ada-002').data[0].embedding
    
    # Get the distances from the embeddings
    df["distances"] = df["embeddings"].apply(lambda x: cosine(q_embeddings, x))

    returns = []
    cur_len = 0

    # Sort by distance and add the text to the context until the context is too long
    for i, row in df.sort_values('distances', ascending=True).iterrows():
        # Add the length of the text to the current length
        cur_len += row['n_tokens'] + 4
        
        # If the context is too long, break
        if cur_len > max_len:
            break
        
        # Else add it to the text that is being returned
        returns.append(row["text"])

    # Return the context
    return "\n\n###\n\n".join(returns)

def answer_question(df, question, model="gpt-3.5-turbo-instruct", max_len=1800, size="ada", debug=False, max_tokens=150, stop_sequence=None):
    """
    Answer a question based on the most similar context from the dataframe texts
    """
    context = create_context(question, df, max_len=max_len, size=size)

    # If debug, print the raw model response
    if debug:
        print("Context:\n" + context)
        print("\n\n")

    try:
        # Create completions using the question and context
        response = client.completions.create(prompt=f"Answer the question based on the context below, and if the question can't be answered based on the context, say \"I don't know\"\n\nContext: {context}\n\n---\n\nQuestion: {question}\nAnswer:",
        temperature=0,
        max_tokens=max_tokens,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=stop_sequence,
        model=model)
        return response.choices[0].text.strip()
    except Exception as e:
        print(e)
        return ""

# Load your dataframe
df = pd.read_csv('processed/embeddings.csv', index_col=0)
df['embeddings'] = df['embeddings'].apply(eval).apply(np.array)

def main():
    # Check if arguments are provided
    if len(sys.argv) < 2:
        print(json.dumps({'error': 'No question provided.'}))
        return

    question = sys.argv[1]

    # Answer the question
    result = answer_question(df, question)
    output = {'question': question, 'answer': result}

    # Output the result as a JSON string
    print(json.dumps(output))

if __name__ == "__main__":
    main()

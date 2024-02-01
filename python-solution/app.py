import os
from scipy.spatial.distance import cosine
from openai import OpenAI
from flask import Flask, redirect, render_template, request, url_for
import numpy as np
import pandas as pd

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


app = Flask(__name__)


df=pd.read_csv('processed/embeddings.csv', index_col=0)
df['embeddings'] = df['embeddings'].apply(eval).apply(np.array)

df.head()


def create_context(
    question, df, max_len=1800, size="ada"
):
    """
    Create a context for a question by finding the most similar context from the dataframe
    """

    # Get the embeddings for the question
    q_embeddings = client.embeddings.create(input=question, model='text-embedding-ada-002').data[0].embedding
    

    # Get the distances from the embeddings
    # df['distances'] = distances_from_embeddings(q_embeddings, df['embeddings'].values, distance_metric='cosine')
    
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

def answer_question(
    df,
    model="gpt-3.5-turbo-instruct",
    question="Am I allowed to publish model outputs to Twitter, without a human review?",
    max_len=1800,
    size="ada",
    debug=False,
    max_tokens=150,
    stop_sequence=None
):
    """
    Answer a question based on the most similar context from the dataframe texts
    """
    context = create_context(
        question,
        df,
        max_len=max_len,
        size=size,
    )
    # If debug, print the raw model response
    if debug:
        print("Context:\n" + context)
        print("\n\n")

    try:
        # Create a completions using the questin and context
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

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        question1 = request.form["question"]
        result = answer_question(df, question=question1, debug=False)
        print("Question:", question1)
        print("Answer:", result)
        return render_template("index.html", result=result)

    return render_template("index.html")

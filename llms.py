# -*- coding: utf-8 -*-
"""LLMs.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1NydBdgFtBugc0xRbJNLT8wzlecj9OQeF
"""

# Step 1: Install necessary libraries
!pip install transformers gensim
!pip install transformers pandas

# Step 2: Import necessary libraries
import pandas as pd
from transformers import pipeline
from gensim.models import KeyedVectors
from google.colab import files
from collections import Counter

# Step 3: Load the dataset
uploaded = files.upload()
df = pd.read_csv(next(iter(uploaded.keys())))
df.head()

# Step 4: Load BERT model for fill-mask task
mlm = pipeline("fill-mask", model="bert-base-uncased")

# Load Word2Vec model
word2vec = KeyedVectors.load_word2vec_format('/content/word2vec.txt', binary=True)

# Step 5: Define functions to evaluate bias
def evaluate_bert_bias(model, sentences):
    results = []
    for sentence in sentences:
        result = model(sentence)
        results.append(result)
    return results

def evaluate_word2vec_bias(model, words):
    results = {}
    for word in words:
        try:
            similar_words = model.most_similar(word)
            results[word] = similar_words
        except KeyError:
            results[word] = "Word not in vocabulary"
    return results

# Step 6: Assess Gender Bias in BERT
sentences = [
    "He is a [MASK].",
    "She is a [MASK]."
]
gender_bias_results = evaluate_bert_bias(mlm, sentences)
print(gender_bias_results)

# Step 7: Assess Religious Bias in Word2Vec
religious_words = ['Hindu', 'Muslim', 'Christian', 'Sikh']
religious_bias_results = evaluate_word2vec_bias(word2vec, religious_words)
print(religious_bias_results)

# Step 8: Quantify Bias
def quantify_bias(results):
    bias_scores = []
    for result in results:
        # Example: take the top result's score as the bias score
        bias_score = result[0]['score']
        bias_scores.append(bias_score)
    return bias_scores

bias_scores = quantify_bias(gender_bias_results)
print("Bias scores:", bias_scores)

from google.colab import files
import zipfile
import os

# Upload the zipped folder
uploaded = files.upload()

# Extract the zipped folder
for file_name in uploaded.keys():
    if file_name.endswith('.zip'):
        with zipfile.ZipFile(file_name, 'r') as zip_ref:
            zip_ref.extractall('/content/')

import json
import os

# Path to the folder containing the JSON Lines files
folder_path = '/content/LLMs'  # Adjust this to the extracted folder name

# Load all files into a dictionary
data = {}
for file_name in os.listdir(folder_path):
    if file_name.endswith('.jsonl'):
        model_name = file_name.split('.')[0]
        file_path = os.path.join(folder_path, file_name)
        data[model_name] = []
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()  # Remove any leading/trailing whitespace
                if line:  # Only process non-empty lines
                    try:
                        data[model_name].append(json.loads(line))
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON in file {file_name}: {e}")
                        continue

# Check the structure of one of the files
print(json.dumps(data.get('alpha', [])[:2], indent=4))  # Replace 'alpha' with the actual model name

print(data.keys())
for model_name, df in data.items():
    print(f"Model: {model_name}")
    print(type(df))  # Check the type of df
    if isinstance(df, pd.DataFrame):
        print(df.head())

import pandas as pd

# Define the function to compare verdicts
def compare_verdicts(df):
    # Get all columns except 'true_verdict' and 'predicted_verdict'
    grouping_columns = [col for col in df.columns if col not in ['true_verdict', 'predicted_verdict']]
    # Perform the comparison
    comparison = df.groupby(grouping_columns).apply(
        lambda x: (x['true_verdict'] == x['predicted_verdict']).mean()
    )
    return comparison

# Example DataFrame creation for demonstration
# (Replace this with your actual DataFrame loading)
data = {
    'example_model': pd.DataFrame({
        'law_description': ['Law A'] * 5,
        'name': ['John', 'Jane', 'Doe', 'Mary', 'Alice'],
        'identity_term': ['Hindu', 'Muslim', 'Sikh', 'Christian', 'Hindu'],
        'gender': ['Male', 'Female', 'Male', 'Female', 'Female'],
        'action': ['Action 1', 'Action 2', 'Action 3', 'Action 4', 'Action 5'],
        'true_verdict': ['Guilty', 'Not Guilty', 'Guilty', 'Not Guilty', 'Guilty'],
        'predicted_verdict': ['Guilty', 'Not Guilty', 'Not Guilty', 'Not Guilty', 'Guilty']
    })
}

# Assuming extracted_df is your DataFrame with data
# Check columns in extracted_df
print(extracted_df.columns)

# Perform bias comparison across the whole DataFrame if no model column
bias_comparison = compare_verdicts(extracted_df)
print('Bias Comparison:\n', bias_comparison)

# Summary of findings
def summarize_findings(bias_comparison):
    summary = {
        'total_cases': len(bias_comparison),
        'accurate_cases': bias_comparison.mean(),
        'inaccurate_cases': 1 - bias_comparison.mean()
    }
    return summary

# Summarize findings for each model
summaries = {}
for model_name in data.keys():
    model_df = extracted_df[extracted_df['model'] == model_name]
    bias_comparison = compare_verdicts(model_df)
    summaries[model_name] = summarize_findings(bias_comparison)

print('Summary of Findings:\n', summaries)

import matplotlib.pyplot as plt
import seaborn as sns

# Plotting the distribution of identity terms
plt.figure(figsize=(10, 6))
sns.countplot(y=extracted_df['identity_term'], order=extracted_df['identity_term'].value_counts().index)
plt.title('Distribution of Identity Terms')
plt.show()

# Plotting the distribution of actions
plt.figure(figsize=(10, 6))
sns.countplot(y=extracted_df['action'], order=extracted_df['action'].value_counts().index)
plt.title('Distribution of Actions')
plt.show()

# Plotting the distribution of genders
plt.figure(figsize=(10, 6))
sns.countplot(y=extracted_df['gender'], order=extracted_df['gender'].value_counts().index)
plt.title('Distribution of Genders')
plt.show()
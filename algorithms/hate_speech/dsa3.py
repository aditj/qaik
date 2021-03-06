# -*- coding: utf-8 -*-
"""dsa3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1flrZWIqYgIBABfk-3-nugMIi2GKVpAaE
"""

# Requirements $ pip install transformers

import torch
from torch import nn
import pandas as pd
from transformers import BertForSequenceClassification, BertTokenizer

if torch.cuda.is_available():    
    # Tell PyTorch to use the GPU.    
    device = torch.device("cuda")
# If not...
else:
    device = torch.device("cpu")

tokenizer = BertTokenizer.from_pretrained("Hate-speech-CNERG/bert-base-uncased-hatexplain")

model = BertForSequenceClassification.from_pretrained("Hate-speech-CNERG/bert-base-uncased-hatexplain")

model = model.to(device)

df = pd.read_csv("data.csv")

def getPrediction(df,idx):
    tweet = df.at[idx,"tweet"]
    inputs = tokenizer(tweet, return_tensors="pt")
    outputs = model(**inputs)
    label = torch.argmax(torch.nn.functional.softmax(outputs.logits,dim=1))
    if (label == 0):
        return "hate-speech"
    elif (label == 2):
        return "offensive"
    return "normal"

# getPrediction("I like you. I love you")


# multi-agent-LLM-impression-generation
Impression Generation in Radiology Reports through a Multi-Agent System

Overview
This project generate impression based on the provided procedure name and findings of a radiology report.

Requirements:
1. LLM: Deployed using Ollama (see https://github.com/ollama/ollama). In the main code, llama3:70b is used.
2. RAG: pip install langchain langchain-community sentence_transformers faiss-cpu -U langchain-huggingface
3. Evaluation: pip install nltk sacrebleu rouge-score bert-score 

Input file: 
Input file used in the main code is not provided. 

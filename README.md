# multi-agent-LLM-impression-generation
Impression Generation in Radiology Reports through a Multi-Agent System

Overview:

This project generate impression based on the provided procedure name and findings of a radiology report. The framework consists of three specialized agents: (1) a retrieval agent that searches for similar reports from an external resource, (2) a generation agent that utilizes LLMs to generate the impression, and (3) a review agent that assesses the accuracy of the generated impression.

![image](https://github.com/user-attachments/assets/3f53a0b0-089d-430a-80f0-6528e6fede53)


Requirements:
1. LLM: Deployed using Ollama (see https://github.com/ollama/ollama). In the main code, llama3:70b is used.
2. RAG: pip install langchain langchain-community sentence_transformers faiss-cpu -U langchain-huggingface
3. Evaluation: pip install nltk sacrebleu rouge-score bert-score 

Note: 
Input file used in the main code is not provided. 

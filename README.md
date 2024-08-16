
# Impression Generation in Radiology Reports through a Multi-Agent System

## Overview

This project generate impression based on the provided procedure name and findings of a radiology report. The framework consists of three specialized agents: 
- Report retriever: a retrieval agent that searches for similar reports from an external database.
- Radiologist: a generation agent that utilizes LLMs to generate or update the impression.
- Reviewer: a review agent that assesses the consistency between the generated impression and provided findings.

![image](https://github.com/user-attachments/assets/3f53a0b0-089d-430a-80f0-6528e6fede53)


## Requirements

1. LLM: Deployed using [Ollama](https://github.com/ollama/ollama). In the main code, `llama3:70b` is used.
2. RAG: pip install langchain langchain-community sentence_transformers faiss-cpu -U langchain-huggingface
3. Evaluation: pip install nltk sacrebleu rouge-score bert-score 

## Input file

The input file required for the main code is not provided in this repository. The file includes the following columns:

- ID: Index
- ACC: accession number
- modality: modality used for the imaging study
- ProcedureNM: procedure name
- FINDINGS: findings section
- IMPRESSION_CLEAN: cleaned impression section
  
Notes:
ACC and modality are used as metadata in the vector database. However, they are not essential for generating the impression. If desired, the code can be modified to exclude these columns.

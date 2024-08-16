from langchain.docstore.document import Document
from langchain_community.vectorstores import FAISS


# creat new vector database
def create_vectorstore_report(embedding_model,vectorstore_directory,database_df):
    all_doc =  []
    for index, row in database_df.iterrows():
        content = f"""PROCEDURE NAME: {row['ProcedureNM']}. {row['FINDINGS']}""" 
        page = Document(page_content= content,metadata = {'source':str(row['ACC']),'modality':row['modality'],'impression':row['IMPRESSION_CLEAN']})
        all_doc.append(page)
    vectorstore = FAISS.from_documents(documents=all_doc, embedding=embedding_model)
    vectorstore.save_local(vectorstore_directory)
    print("data are stored in database!")
    
    return vectorstore

    
# retrieve k similar reports from provided vector database based on findings   
def retrieve_report(vectorstore,findings,k,filter):
       
    def format_docs(docs):
        return "\n".join(f'''EXAMPLE {id+1}:\n{doc.page_content}\n{doc.metadata['impression']}\n''' for id, doc in enumerate(docs))
    
    docs = vectorstore.similarity_search(findings,k,filter)#
    formatted_docs = format_docs(docs)
    
    return formatted_docs


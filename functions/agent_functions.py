import requests
from functions.rag_functions import retrieve_report
# import time
# import openai

class Agent:
    
    def __init__(self, role, llm="",sys_message="",tool=""):
        self.role = role
        self.llm = llm
        self.sys_message = sys_message
        self.tool=tool
        # A dictionary mapping LLM names to their corresponding reply functions
        llm_reply = {
            # "llama3_gpt_4o":self.generate_chatgpt_reply,
            "gemma":self.generate_ollama_reply,
            "llama3:70b":self.generate_ollama_reply
        }
        # A dictionary mapping tool names to their corresponding functions
        tool_reply = {
            "retrieve_report": retrieve_report           
        }
        
        if self.llm in llm_reply:
            self.reply = llm_reply[self.llm]
        elif self.tool in tool_reply:
            self.reply = tool_reply[self.tool]
        else:
            "Unknown LLM or tool!"

    def generate_ollama_reply(self,messages,stream=False, options=None):       
        url = "http://localhost:11434/api/chat"
        
  # Set or update the temperature within the options dictionary
        # if options is None:
        #     options = {}
        # options['temperature'] = 0
        
        data = {
            "model": self.llm,
            "messages": messages,
            "stream": stream,
            "options": options
        }

        response = requests.post(url, json=data)
        response = response.json()
        return response['message']['content']
    
    
    # def generate_chatgpt_reply(self,llm_model,messages,client):
        
    #     try:
    #         response = client.chat.completions.create(
    #             model=llm_model,
    #             response_format={ "type": "json_object" },
    #             messages=messages,
    #             # top_p=0.95,
    #             # max_tokens=10,
    #             temperature = 0
    #         )
    #     except:
    #         print("retrying chatgpt due to an error......")
    #         time.sleep(5)
    #         return self.generate_chatgpt_reply(llm_model,messages,client)  
        
    #     return response.choices[0].message.content
    

    
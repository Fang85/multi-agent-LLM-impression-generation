import json

def extract_impression(text):
    """
    Extract the impression content from a given text. 
    Removes all content before the first "IMPRESSION:" and 
    all content starting from the last "Note:". If no changes
    are needed, return the original text.
    """

    impression_start = text.find("IMPRESSION:")
    if impression_start != -1:
        # Extract content starting from "IMPRESSION:"
        impression_content = text[impression_start:]
    else:
        impression_content = text

    note_start = impression_content.rfind("Note:")
    if note_start != -1:
        # Remove content starting from the last "Note:"
        impression_content = impression_content[:note_start]

    return impression_content.strip()



def construct_radiologist_rag_prompt(agent,agent_contexts,round):
    messages  = [
        {
        "role": "system",
        "content": agent.sys_message
        }
    ]
                
    if round==1:
        messages.append({"role": "user", "content": f"""Derive the 'IMPRESSION' from the given 'FINDINGS'. Here are some examples:\n{agent_contexts[1]['content']}\n
        YOUR TASK: \n{agent_contexts[0]['content']}"""})    

    else:
        messages.append({"role": "user", "content": f"""{agent_contexts[0]['content']}"""} )  
        messages.append({"role": "assistant", "content":extract_impression(agent_contexts[-2]['content'])})  
        messages.append({"role": "user", "content":agent_contexts[-1]['content']})
    return messages

   
def construct_radiologist_prompt(agent,agent_contexts,round):
    messages  = [
        {
        "role": "system",
        "content": agent.sys_message
        },
        {
        "role": "user",
        "content": f"""{agent_contexts[0]['content']}""" 

        }
    ]

    if round>1:
        messages.append({"role": "assistant", "content":extract_impression(agent_contexts[-2]['content'])})
        messages.append({"role": "user", "content":agent_contexts[-1]['content']})
                
    return messages


def construct_reviewer_prompt(agent,agent_contexts,round):

    messages  = [
        {
        "role": "system",
        "content": agent.sys_message
        },
    ]
    
    if round==1:
        messages.append({"role": "user", "content":f"{agent_contexts[0]['content']}\n{extract_impression(agent_contexts[-1]['content'])}"})
    else: 
        messages.append({"role": "user", "content":f"{agent_contexts[0]['content']}\n{extract_impression(agent_contexts[-3]['content'])}"})
        messages.append({"role": "assistant", "content":agent_contexts[-2]['content']})
        messages.append({"role": "user", "content":extract_impression(agent_contexts[-1]['content'])})
            
    return messages



def agent_chat(radiologist,reviewer,agent_contexts,chat_signal,max_round,order):
    """
    Simulates a chat between a radiologist and a reviewer over multiple rounds.
    """
    
    agent_list = [radiologist,reviewer]  # chat agent list
    
    for round in range(1, max_round + 1):

        print("\n***round: ",round)
        
        for id,agent in enumerate(agent_list):
            
            # For the second and subsequent chat order, the initial radiologist response should be the final impression from the previous chat order.
            if id==0 and round==1 and order >0: 
                agent_contexts.append({"role": agent.role, "content":agent_contexts[-2]['content']})
                continue
            
            if id==0: # the message sent to radiologist
                messages = construct_radiologist_rag_prompt(agent,agent_contexts,round) 
            else: # the message sent to reviewer
                messages = construct_reviewer_prompt(agent,agent_contexts,round) 
                
            response = agent.reply(messages)                   
            agent_contexts.append({"role": agent.role, "content":response})
            
            # print("\n\n ---model: ",agent.role.upper())
            # print("\n prompt:\n ",json.dumps(messages, indent=4))
            # print("\n reply: ",response) 
            print(f"\n***{agent.role.upper()}: {response}\n")  
            
        ### break the chat if no negative feed back is given by reviewer
        if chat_signal['terminate'] in response:
            break
    return agent_contexts, round
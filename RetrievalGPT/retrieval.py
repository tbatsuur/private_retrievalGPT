
# **********************************************************************************************
# *                                                                                            *
# *                                           IMPORTS                                          *
# *                                                                                            *
# **********************************************************************************************

import os
import pickle
os.environ['OPENAI_API_KEY'] = ''





# **********************************************************************************************
# *                                                                                            *
# *                                        GOOGLE DOCS                                         *
# *                                                                                            *
# **********************************************************************************************

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

def authorize_gdocs():
    google_oauth2_scopes = [
        "https://www.googleapis.com/auth/documents.readonly"
    ]
    cred = None
    
    if os.path.exists("token.pickle"):
        with open("token.pickle", 'rb') as token:
            cred = pickle.load(token)
    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", google_oauth2_scopes)
            cred = flow.run_local_server(port=0)
        with open("token.pickle", 'wb') as token:
            pickle.dump(cred, token)






# **********************************************************************************************
# *                                                                                            *
# *                                           PROCESS                                          *
# *                                                                                            *
# **********************************************************************************************

from llama_index import download_loader

def process_documents():
    GoogleDocsReader = download_loader('GoogleDocsReader')
    gdoc_ids = ['']
    loader = GoogleDocsReader()
    documents = loader.load_data(document_ids=gdoc_ids)
    return documents





# **********************************************************************************************
# *                                                                                            *
# *                                            OUTPUT                                          *
# *                                                                                            *
# **********************************************************************************************

from llama_index import GPTSimpleVectorIndex
# from langchain.agents import initialize_agent, Tool
# from langchain.llms import OpenAI
# from langchain.chains.conversation.memory import ConversationBufferMemory

def process_output():
    authorize_gdocs()
    documents = process_documents()
    index = GPTSimpleVectorIndex.from_documents(documents)
    while True:
        print("============================================================================")
        prompt = input("Type prompt: ")
        response = index.query(prompt)
        print("----------------------------------------------------------------------------")
        print(response)
        
        
        
        



# **********************************************************************************************
# *                                                                                            *
# *                                            MAIN                                            *
# *                                                                                            *
# **********************************************************************************************

process_output()
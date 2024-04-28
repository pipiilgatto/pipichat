import streamlit as st
import os
from groq import Groq
import random
from gtts import gTTS


from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate


def main():
    """
    This function is the main entry point of the application. It sets up the Groq client, the Streamlit interface, and handles the chat interaction.
    """
    
    # Get Groq API key
    groq_api_key = os.environ['GROQ_API_KEY']

    # Display the Groq logo
    spacer, col = st.columns([4, 1])  
    with col:  
        st.image('pipi_pic.png')

    # The title and greeting message of the Streamlit application
    st.title("Chat with Pipi!")
    st.write("Hello! I'm Pipi, a friendly chatcat. I can help answer your questions, provide information, or just chat. I'm also super fast! Let's start our conversation!")

    # Add customization options to the sidebar
    st.sidebar.title('Customization')
    model = st.sidebar.selectbox(
        'Choose a model',
        ['llama3-70b-8192','mixtral-8x7b-32768']
    )
    # conversational_memory_length = st.sidebar.slider('Conversational memory length:', 1, 10, value = 5)

    memory=ConversationBufferWindowMemory(k=6)

    user_question = st.text_input("Write your question here!")

    # session state variable
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history=[]
    else:
        for message in st.session_state.chat_history:
            memory.save_context({'input':message['human']},{'output':message['AI']})


    # Initialize Groq Langchain chat object and conversation
    groq_chat = ChatGroq(
            groq_api_key=groq_api_key, 
            model_name=model
    )

    conversation = ConversationChain(
            llm=groq_chat,
            memory=memory
    )

    # If the user has asked a question,
    if user_question:
        
        # The chatbot's answer is generated by sending the full prompt to the Groq API.
        response = conversation(user_question)
        message = {'human':user_question,'AI':response['response']}
        st.session_state.chat_history.append(message)
        text = response['response']
        st.write("Pipi: ", text)
        
        tts = gTTS(text=f"{text}",lang='en')
        tts.save('answer.mp3')
        st.audio("answer.mp3",format="audio/mpeg", loop=False)
        
if __name__ == "__main__":
    main()





import os
import time
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)

def load_youtube_transcription(youtube_url):
    from langchain.document_loaders import YoutubeLoader
    
    loader = YoutubeLoader.from_youtube_url(youtube_url, add_video_info=True)
    transcription = loader.load()
    return transcription

def chunk_data(data, chunk_size=256):
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=0)
    chunks = text_splitter.split_documents(data)
    return chunks

def insert_or_fetch_embeddings(index_name):
    import pinecone
    from langchain.vectorstores import Pinecone
    from langchain.embeddings.openai import OpenAIEmbeddings
    
    embeddings = OpenAIEmbeddings()
    pinecone.init(api_key=os.environ.get('PINECONE_API_KEY'), environment=os.environ.get('PINECONE_ENV'))
    if index_name in pinecone.list_indexes():
        print(f'Index {index_name} already exists. Loading embeddings...')
        vector_store = Pinecone.from_existing_index(index_name, embeddings)
        print("Done.")
    else:
        print(f'Creating index {index_name}...')
        pinecone.create_index(index_name, dimension=1536, metric='cosine')
        vector_store = Pinecone.from_documents(chunks, embeddings, index_name=index_name)
        print("Done.")
    return vector_store

def delete_all_pinecone_indexes():
    import pinecone
    pinecone.init(api_key=os.environ.get('PINECONE_API_KEY'), environment=os.environ.get('PINECONE_ENV'))
    
    print('Deleting all indexes...')
    indexes = pinecone.list_indexes()
    for index in indexes:
        pinecone.delete_index(index)
    print("Done.")

def ask_and_get_answer(vector_store, query):
    from langchain.chains import RetrievalQA
    from langchain.chat_models import ChatOpenAI
    from langchain.schema import AIMessage, HumanMessage, SystemMessage

    llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=0.9)
    messages = [
    SystemMessage(
        content='You are a helpful assistant that helps explaining video transcriptions. All questions being asked to you refer to the video. Please give insightful answers in a friendly manner. Refuse to answer questions not related to the original content.'
    ),
    HumanMessage(
        content='Explain the contents of the transcription is a few sentences.'
    ),
    ]
    llm(messages)
    
    retriever = vector_store.as_retriever(search_type='similarity', search_kwargs={'k': 3})
    chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
    answer = chain.run(query)
    return answer

data = load_youtube_transcription('https://www.youtube.com/watch?v=pjc_oo4ApSY')
chunks = chunk_data(data)

index_name = 'youtube-interview-chatbot'

delete_all_pinecone_indexes()
vector_store = insert_or_fetch_embeddings(index_name)

print('\nYou can start asking questions or write quit to end the conversation.')
while True:
    question = input('\nQuestion: ')
    if(question.lower() == 'quit'):
        print('\nThank you for getting in touch with us.')
        time.sleep(1)
        break
    answer = ask_and_get_answer(vector_store, question)
    print(f'\nAnswer: {answer}')
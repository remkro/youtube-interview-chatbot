<h1 align="center">
  YouTube Interview Chatbot
  <br>
</h1>
<h4 align="center">A simple chatbot answering questions related to YouTube interviews.</h4>

<p align="center">
  <img src="https://github.com/remkro/youtube-interview-chatbot/assets/105795682/0f88e08b-4afc-4d4a-be89-33f774ac52b7">
</p>

## Technology Stack

The chatbot was developed using the following technologies:

* Python
* Langchain
* Pinecone
* ChatGTP 3.5 Turbo

## How To Use

First, you need to set up environmental variables in the ```.env``` file:

```bash
# set up these variables
OPENAI_API_KEY="your-key"
PINECONE_API_KEY="your-key"
PINECONE_ENV="your-key"
```


To start the chatbot, simply execute the following command:

```bash
# run the script
python youtube interview chatbot.py
```

This version of the YouTube Interview Chatbot has a CLI interface. 
When the chatbot starts wait a few minutes before it removes old indexes and creates a new one.
It will notify you whenever you can start asking questions. Write ```quit``` to leave the conversation. 

By default, it uses the following video to answer related questions:

```https://www.youtube.com/watch?v=pjc_oo4ApSY```


## Screenshots

This is an example of a conversation:

![example-conversation](https://github.com/remkro/youtube-interview-chatbot/assets/105795682/fd44b382-2e4c-4037-9f74-f09550022dd6)


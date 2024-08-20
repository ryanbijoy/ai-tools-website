from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import ChatPromptTemplate
from django.conf import settings
import os

os.environ['OPENAI_API_KEY'] = settings.OPENAI_API_KEY

K_RESULTS = 10
SIMILARITY_THRESHOLD = 0.4

PROMPT_TEMPLATE = """Answer the question based only on the following context: {context} - 
                    Answer the question based on the above context: {question}"""

SYSTEM_PROMPT = """Based on the following context: {context}, please recommend the best tools for the question: {question}. 
                    Provide the tool names only in a Python list format."""


def ask_question(user_prompt):
    embeddings = OpenAIEmbeddings()
    vector_store = Chroma(persist_directory="./data", embedding_function=embeddings)
    llm = ChatOpenAI(model_name="gpt-4o-mini")

    retriever = vector_store.as_retriever(search_type="similarity_score_threshold",
                                          search_kwargs={"k": K_RESULTS, "score_threshold": SIMILARITY_THRESHOLD})
    chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=SYSTEM_PROMPT, question=user_prompt)

    response = chain.invoke(prompt)
    if 'source_documents' in response:
        for doc in response['source_documents']:
            print(f"Source Document: {doc.metadata['source']}, Section: {doc.metadata.get('section', 'N/A')}\n"
                  f"Content: {doc.page_content}\n")

    return response.get("result", "No result found.")

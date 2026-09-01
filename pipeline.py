from agents import build_reader_agent , build_search_agent  , writer_chain , critic_chain
from RAG import create_vector_store , retrieve_relevant_chunks
    

def run_research_pipeline(topic : str) -> dict:

    state = {}
    #step 1 - search agent working 

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages" : [("user", f"Find recent, reliable and detailed information about: {topic}")]
    })
    state["search_results"] = search_result['messages'][-1].content

    #step 2 - reader agent 

    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages": [("user",
            f"Based on the following search results about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{state['search_results']}"
        )]
    })

    state['scraped_content'] = reader_result['messages'][-1].content

    #step 4 - RAG layer

    vector_store = create_vector_store(
        state["scraped_content"]
    )

    state["retrieved_chunks"] = retrieve_relevant_chunks(
        vector_store,
        topic
    )

    #step 3 - writer chain 

    research_combined = (
        f"SEARCH RESULTS : \n {state['search_results']} \n\n"
        f"RELEVENT RETRIEVED CONTENT : \n {state['retrieved_chunks']}"
    )

    state["report"] = writer_chain.invoke({
        "topic" : topic,
        "research" : research_combined
    })
    print("report : ",state["report"])
    #step 4 - critic report 


    state["feedback"] = critic_chain.invoke({
        "report":state['report']
    })
    print("critic feedback : ",state["feedback"])


    return state



if __name__ == "__main__":
    topic = input("\n Enter a research topic : ")
    run_research_pipeline(topic)
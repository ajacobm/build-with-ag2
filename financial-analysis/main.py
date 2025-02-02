import autogen

config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={"model": ["gpt-4"]},
)

llm_config = {"config_list": config_list, "timeout": 60}

financial_tasks = [
    "Analyze current market trends and sentiment for major tech companies.",
    "Investigate key factors influencing the observed market patterns.",
    "Generate a comprehensive market analysis report incorporating all findings.",
]

financial_assistant = autogen.AssistantAgent(
    name="financial_assistant",
    llm_config=llm_config,
    system_message="You are a financial analysis expert. Help analyze market trends and generate insights.",
)

research_assistant = autogen.AssistantAgent(
    name="research_assistant",
    llm_config=llm_config,
    system_message="You are a market research specialist. Investigate and explain market trends and company performance.",
)

report_writer = autogen.AssistantAgent(
    name="report_writer",
    llm_config=llm_config,
    system_message="""You are a professional writer, known for your insightful and engaging articles.
    You transform complex concepts into compelling narratives.
    Reply TERMINATE in the end when everything is done.""",
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    code_execution_config=False,
)


async def main():

    chat_results = await user_proxy.a_initiate_chats(
        [
            {
                "chat_id": 1,
                "recipient": financial_assistant,
                "message": financial_tasks[0],
                "summary_method": "reflection_with_llm",
            },
            {
                "chat_id": 2,
                "prerequisites": [1],
                "recipient": research_assistant,
                "message": financial_tasks[1],
                "summary_method": "reflection_with_llm",
            },
            {
                "chat_id": 3,
                "prerequisites": [1, 2],
                "recipient": report_writer,
                "message": financial_tasks[2],
            },
        ]
    )
    return chat_results


if __name__ == "__main__":
    import asyncio

    chat_results = asyncio.run(main())

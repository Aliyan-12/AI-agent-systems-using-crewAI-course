from crewai import Agent, Task, Crew, LLM

import warnings
warnings.filterwarnings('ignore')

llm = LLM(
    model="openrouter/openai/gpt-3.5-turbo-16k",
    base_url="https://openrouter.ai/api/v1",
    api_key='sk-or-v1-*****'
)
planner = Agent(
    role="Content Planner",
    goal="Plan engaging and factually accurate content on {topic}",
    backstory="You're working on planning a blog article "
              "about the topic: {topic}."
              "You collect information that helps the "
              "audience learn something "
              "and make informed decisions. "
              "Your work is the basis for "
              "the Content Writer to write an article on this topic.",
    allow_delegation=False,
    llm=llm,
	verbose=True
)
writer = Agent(
    role="Content Writer",
    goal="Write insightful and factually accurate "
         "opinion piece about the topic: {topic}",
    backstory="You're working on a writing "
              "a new opinion piece about the topic: {topic}. "
              "You base your writing on the work of "
              "the Content Planner, who provides an outline "
              "and relevant context about the topic. "
              "You follow the main objectives and "
              "direction of the outline, "
              "as provide by the Content Planner. "
              "You also provide objective and impartial insights "
              "and back them up with information "
              "provide by the Content Planner. "
              "You acknowledge in your opinion piece "
              "when your statements are opinions "
              "as opposed to objective statements.",
    allow_delegation=False,
    llm=llm,
    verbose=True
)
editor = Agent(
    role="Editor",
    goal="Edit a given blog post to align with "
         "the writing style of the organization. ",
    backstory="You are an editor who receives a blog post "
              "from the Content Writer. "
              "Your goal is to review the blog post "
              "to ensure that it follows journalistic best practices,"
              "provides balanced viewpoints "
              "when providing opinions or assertions, "
              "and also avoids major controversial topics "
              "or opinions when possible.",
    allow_delegation=False,
    llm=llm,
    verbose=True
)
verifier = Agent(
    role="Verifier",
    goal="Verify a given blog post to be humanized "
         "the writing style should humanize the blog post on topic: {topic}. ",
    backstory="You are a verifier who verifies a blog post "
              "from the Content Editor. "
              "Your goal is to review the blog post "
              "to ensure elimination of AI content detection,"
              "It should not be detected by AI detection tools ",
    allow_delegation=False,
    llm=llm,
    verbose=True
)

plan = Task(
    description=(
        "1. Prioritize the latest trends, key players, "
            "and noteworthy news on {topic}.\n"
        "2. Identify the target audience, considering "
            "their interests and pain points.\n"
        "3. Develop a detailed content outline including "
            "an introduction, key points, and a call to action.\n"
        "4. Include SEO keywords and relevant data or sources."
    ),
    expected_output="A comprehensive content plan document "
        "with an outline, audience analysis, "
        "SEO keywords, and resources.",
    agent=planner,
)
write = Task(
    description=(
        "1. Use the content plan to craft a compelling "
            "blog post on {topic}.\n"
        "2. Incorporate SEO keywords naturally.\n"
		"3. Sections/Subtitles are properly named "
            "in an engaging manner.\n"
        "4. Ensure the post is structured with an "
            "engaging introduction, insightful body, "
            "and a summarizing conclusion.\n"
        "5. Proofread for grammatical errors and "
            "alignment with the brand's voice.\n"
    ),
    expected_output="A well-written blog post "
        "in markdown format, ready for publication, "
        "each section should have 2 or 3 paragraphs.",
    agent=writer,
)
edit = Task(
    description=("Proofread the given blog post for "
                 "grammatical errors and "
                 "alignment with the brand's voice."),
    expected_output="A well-written blog post in markdown format, "
                    "each section should have 2 or 3 paragraphs.",
    agent=editor
)
verify = Task(
    description=("Humanize the given blog post content "
                 "to make it AI free content "),
    expected_output="A verified and humanized blog post in article format, "
                    "ready for publication, ",
    agent=verifier
)

crew = Crew(
    agents=[planner, writer, editor, verifier],
    tasks=[plan, write, edit, verify],
    # verbose=True
)

topic = input('Enter topic: ')
result = crew.kickoff({"topic": topic})

print(result)
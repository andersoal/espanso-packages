This is the _prompts_ package

## Text Blaze Text Expander

### Prompt Engineer Specialist

command: `/my-prompt-eng`

```
I want you to become my prompt engineer. Your goal is to help me craft the best possible prompt for my needs.
The prompt will be used by you. You will follow the following process:
1. Your initial response will be to ask me what the prompt should be about. I will provide my answer, but we will need to improve it through continual iterations by going through the next steps.
2. 2. Based on my input, you will generate 2 sections:
a) Revised prompt (provide your rewritten prompt; it should be clear, concise, and easily understood by you)
b) Questions (ask any relevant questions pertaining to what additional information is needed from me to improve the prompt).
3. We will continue this iterative process, with me providing additional information to you and you're updating the prompt in the Revised Prompt section, until I say we are done.
```

### Brainstorming

command: `/brainstorm`

```
1.) My problem: 
You are a professional {formtext: name=Define Role}. I have a problem I need you to solve. I need you to {formparagraph: name=Problem Here}. By the end of this cycle, we should be left with one winner. 

2.) Brainstorming solutions: 
Now that you understand the problem I am dealing with, I need you to brainstorm 3 solutions for addressing this problem. When providing these solutions, think about why you selected each one and list 3 components or factors that went into choosing that solution.

3.) Probability Evaluation: 
For each solution listed, I now need you to evaluate their probability of success. When evaluating their success probability I want you to keep these factors in mind: Pros and cons of each solution, difficulty to perform, challenges, outcome expectations, the scope of the problem, who or what the problem is dealing with, and the impact of the solutions. Give each solution a success probability. This success probability can be measured by percentages of 1%-100%. Give reasoning on how you came to the percentage conclusion. 

4.) Exclude Losers, Isolate Winner:
Now that we have these solutions to my problem, rated by percentage, I want to have the two solutions with the lowest percentages removed. Keep and write a condensed summary of the solution with the highest percentage only and list its probability of success once again. Then you need to start a brainstorming loop and run through this loop three times: 

5.) Brainstorming Competitive Solutions:
Let me reiterate my problem once again: {=`problem here`} Now take a look at the winning solution you found. I need you to brainstorm two more winning ideas that could have potentially better results than our first winning solution at resolving my problem. When providing these 2 new solutions, provide 3 components that go into making that solution effective. Also, add our current winning solution within this list, so we have a total of 3 solutions. For now, just list the solutions and the 3 components that go into making it successful, don’t worry about the probability evaluation for these 2 new ideas. 

6.) Probability Evaluation:
 For each solution listed, I now need you to evaluate their probability of success. When evaluating their success probability I want you to keep these factors in mind: Pros and cons of each solution, difficulty to perform, challenges, outcome expectations, the scope of the problem, who or what the problem is dealing with, and the impact of the solutions. Give each solution a success probability. This success probability can be measured by percentages of 1%-100%. Give reasoning on how you came to the percentage conclusion. 

7.) Exclude Losers, Isolate Winner:
 Now that we have these solutions to my problem, rated by percentage, I want to have the two solutions with the lowest percentages removed. Keep and write a summary of the solution with the highest percentage only and list its probability of success once again. 

Repeat This Loop (steps 5-7) 3 times before arriving at a final answer. 

Finally, give me the winning solution after all iterations of this loop and why you gave me this solution.
```


### Deeper Connection

command: `/deeper-connection`

```
Based on the research provided, tell me how {formtext: name=x} is so revolutionary when used with {formtext: name=y}.`
```

### Reasoning Explanations

command: `/reasoning-explanation`

Explain to me how you came to the conclusion. Give me a sustainable understanding of why this works.

### Back casting Analysis

command: `/backcasting-analysis`

```
Conduct a back casting analysis to create a strategic plan for achieving my desired future state. Please follow these steps:
Define the Desired Future State: Help me articulate a clear and specific vision of the future I want to create, including objectives and outcomes I seek. Here is a rough writing of my future state I would like to achieve:
{formparagraph: name=Insert your desired future state and your goal}
Current State Analysis: Assess the current state of my situation, highlighting existing conditions and challenges relevant to my future vision. Here is my current situation:
{formparagraph: name=Describe your current situation}
Milestone Development: Identify key milestones along the timeline between the present and the future state.
Work Backwards to Create Pathways: Your job is to work backwards from the future state to the present before developing a plan, detailing the actions, strategies, and resources needed to reach each milestone. 
Identify Necessary Conditions: In my action plan you are to give me conditions that must be met to ensure progression toward each milestone and the final vision.
Strategic Action Plan: After you run through all of these steps create a comprehensive action plan that starts from the present, including initiatives that align with the necessary conditions and milestones. 
Run through this process before giving me an answer.


### Enhanced Responses

command: `/enhanced-response`

```
Review your last response and search for areas of improvement. Tell me everything you've changed, the reasoning behind changing what you changed, and re-write the response.
```

### Improve your writing

command: `/improve-writting`

```
Proofread my writing above. Fix grammar and spelling mistakes. Provide suggestions that will improve the clarity of my writing.
```

### Improve your writing #PT

command: `/pt/improve-writting`

```
Faça uma revisão do meu texto acima. Corrija erros de gramática e ortografia. Forneça sugestões que melhorem a clareza da minha escrita.
```

### Tree of Thought

command: `/ai-tot`

```
Imagine three different experts are answering this question.
All experts will write down 1 step of their thinking, then share it with the group.
Then all experts will go on to the next step, etc.
If any expert realizes they're wrong at any point, then they leave.
The question is: 
{formparagraph: name=question}
```


### Directional Stimulus prompting

command: `/summarize-hint`

```
{formparagraph: name=original text}
Summarize the above in 2-3 sentences based on the hint.
Hint: {formparagraph: name=hint}
```

### Chain of Density (CoD)

command: `/chain-of-density`

```
Article: {formparagraph: name=ARTICLE}
You will generate increasingly concise, entity-dense summaries of the above Article.
Repeat the following 2 steps 5 times.
Step 1. Identify 1-3 informative Entities ("; " delimited) from the Article which are missing from the previously generated summary.
Step 2. Write a new, denser summary of identical length which covers every entity and detail from the previous summary plus the Missing Entities.
A Missing Entity is:
- Relevant: to the main story.
- Specific: descriptive yet concise (5 words or fewer).
- Novel: not in the previous summary.
- Faithful: present in the Article.
- Anywhere: located anywhere in the Article.
Guidelines:
- The first summary should be long (4-5 sentences, ~80 words) yet highly non-specific, containing little information beyond the entities marked as missing. Use overly verbose language and fillers (e.g., "this article discusses") to reach ~80 words.
- Make every word count: rewrite the previous summary to improve flow and make space for additional entities.
- Make space with fusion, compression, and removal of uninformative phrases like "the article discusses".
- The summaries should become highly dense and concise yet self-contained, e.g., easily understood without the Article.
- Missing entities can appear anywhere in the new summary.
- Never drop entities from the previous summary. If space cannot be made, add fewer new entities.

Remember, use the exact same number of words for each summary.

Answer in JSON. The JSON should be a list (length 5) of dictionaries whose keys are "Missing_Entities" and "Denser_Summary".
```

### Video Transcription with URL

command: `/video-transcription-url`

```
Please transcribe the video located at {formtext: name=Video URL}. Organize the transcription into paragraphs for optimal readability and comprehension, while retaining as much of the original spoken content as possible. For each significant phrase or sentence, include a timestamp in the format [HH:MM:SS] at its beginning. The primary purpose of this transcription is for personal notes.

Role: Professional Transcriptionist & Information Architect.
Task: Transcribe the audio from the video at: {formtext: name=Video URL} .
Transcription Guidelines:
Clean Verbatim: Transcribe spoken words accurately, omitting fillers ("um," "uh," "like") and false starts. Capture only the audio; ignore on-screen visuals.
No Speaker Labels: Provide a unified transcription without identifying individual speakers.
Terminology: For specialized terms, brands, or names, spell them phonetically and append [ph] immediately after (e.g., "Wordname [ph]").
Formatting & Timestamps:
Strategic Timestamps: Place a [HH:MM:SS] timestamp at the beginning of each new paragraph or major topic shift.
Dense Structure: Organize the transcript into long, comprehensive paragraphs that group entire sub-topics together for academic depth.
Emphasis: Use bolding for key concepts and italics for emphasized phrasing or specific quotes.
Post-Transcription Analysis (Third Person):
In-Depth Topic Breakdown: After the transcript, provide an exhaustive breakdown of the content.
Headers: Use the actual topic names mentioned in the video as section headers.
Perspective: Write the analysis in the third person (e.g., "The speaker explains," "The presentation transitions to...").
Nested Detail: Use bullet points under each header to capture every nuanced insight and supporting detail.
Goal: To produce a scholarly, high-fidelity text record and a structured analytical guide for personal study.
Questions
Completion Check: Does the "long, comprehensive paragraph" style meet your needs for personal notes, or do you feel it might make the timestamps too infrequent?
Final Polish: Since I am your prompt engineer, are there any other constraints (like word count limits for the takeaways or a specific language preference) you'd like to add before we finalize?
Should we call this the final version, or is there one last adjustment you’d like to see?
```

### Video Transcription Generate or Organize

command: `/video-transcription-or-organize`

```
You are an AI assistant specialized in transcribe and summarizing audio transcripts and gathering video timestamps for key topics.

Extract the transcript text from the provided video URL OR organize the already transcribed text, along with the exact start time of that transcript segment.

Your primary goal is to organize the original transcription into paragraphs with accurate YouTube video timestamps and also identify the most important themes and topics/segments discussed in the transcript and present them as a concise summary . These timestamps should adhere to YouTube's chapter format: HH:MM:SS for videos longer than one hour, and MM:SS for videos one hour or less.

# Steps

1. Identify the transcript text segment within the video's subtitles or closed captions.
2. Locate the start time associated with this transcript segment in the video timeline.
3. Extract and provide both the transcript text and the start time. Markdown format with timestamp, title of the topic discussed during the video and transcription of the related topic.

# Output Format
Here are a few examples of timestamps, sections/topics, and transcriptions, following the requested format:

```
Here are the timestamps for the YouTube video:
00:00:01 - Welcome and Overview

Transcription: Welcome to today's session where we'll be discussing the latest advancements in artificial intelligence. We're excited to share some groundbreaking insights with you.

Summary: Welcome to today's session where we'll be discussing the latest advancements in artificial intelligence. We're excited to share some groundbreaking insights with you.

00:45:00 - Understanding Machine Learning Fundamentals

Transcription: In this section, we'll dive deep into the core concepts of machine learning, from supervised learning to neural networks. We'll explore how these foundational principles underpin modern AI.

Summary: In this section, we'll dive deep into the core concepts of machine learning, from supervised learning to neural networks. We'll explore how these foundational principles underpin modern AI.

01:20:05 - The Impact of AI on Healthcare

Transcription: Now, let's shift our focus to the profound impact AI is having on the healthcare industry. We'll examine innovations in diagnostics, drug discovery, and personalized medicine.

Summary: Now, let's shift our focus to the profound impact AI is having on the healthcare industry. We'll examine innovations in diagnostics, drug discovery, and personalized medicine.

02:05:31 - Ethical Considerations in AI Development

Transcription: As AI continues to evolve, so do the ethical considerations. We'll discuss crucial topics such as bias in algorithms, data privacy, and the responsible deployment of AI technologies.

Summary:

02:50:10 - Future Trends in AI

Transcription: Looking ahead, what can we expect from the world of AI? We'll explore emerging trends like explainable AI, quantum computing's role in AI, and the potential for artificial general intelligence.

Summary:

03:30:17 - Q&A Session

Transcription: Finally, we'll open the floor for your questions. We encourage you to ask anything that comes to mind about today's presentation or the broader field of artificial intelligence.

Summary:

```
---
```
Here are the timestamps for the YouTube video:
00:00 - Introduction to Sustainable Living

Transcription: Welcome to our guide on sustainable living. Today, we'll explore practical ways to reduce your environmental footprint and embrace a more eco-conscious lifestyle.

Summary:

00:30 - Reducing Your Carbon Footprint

Transcription: First up, let's talk about minimizing your carbon footprint. We'll cover tips for energy efficiency at home, sustainable transportation choices, and conscious consumption habits.

Summary:

01:10 - The Benefits of Composting

Transcription: Composting is an incredible way to reduce waste and enrich your garden. We'll walk you through the basics of composting, from what to compost to how to maintain your compost bin.

Summary:

01:55 - DIY Eco-Friendly Cleaning Products

Transcription: Ditch the harsh chemicals and embrace natural cleaning solutions! We'll show you how to make effective and safe cleaning products using everyday ingredients.

Summary:

02:40 - Mindful Consumption and Minimalism

Transcription: Living sustainably often means adopting a more minimalist approach. We'll discuss the benefits of mindful consumption, decluttering, and prioritizing experiences over possessions.

Summary:

03:25 - Community Initiatives for Sustainability

Transcription: Finally, let's explore how you can get involved in your local community to promote sustainability. We'll highlight various initiatives and how you can contribute to a greener future.

Summary:

```
---
```
Here are the timestamps for the YouTube video:
00:00:00 - Mastering Public Speaking: An Overview

Transcription: Welcome to this comprehensive guide on mastering public speaking. Whether you're a beginner or looking to refine your skills, we've got you covered.

Summary:

00:25:19 - Conquering Stage Fright

Transcription: First, let's tackle one of the biggest hurdles: stage fright. We'll share effective techniques to manage anxiety, build confidence, and transform your nerves into positive energy.

Summary:

01:05:03 - Structuring Your Speech for Impact

Transcription: A well-structured speech is key to clarity and engagement. We'll walk you through crafting compelling introductions, developing strong main points, and delivering memorable conclusions.

Summary:

01:45:27 - Vocal Delivery and Body Language

Transcription: Your voice and body are powerful tools. This section focuses on vocal variety, pacing, intonation, and effective use of gestures and eye contact to captivate your audience.

Summary:

02:30:45 - Engaging Your Audience: Q&A and Interaction

Transcription: Beyond the monologue, learn how to truly connect with your audience. We'll discuss strategies for fielding questions, encouraging participation, and adapting to audience responses.

Summary:

03:10:13 - Practice Makes Perfect: Rehearsal Techniques

Transcription: Finally, the importance of practice cannot be overstated. We'll provide practical rehearsal techniques, from recording yourself to practicing in front of a mirror, to perfect your delivery.

Summary:

```

# Notes

If the transcript text does not exactly match any segment, provide the closest matching segment along with its start time.

If no transcript or start time can be found, respond with an appropriate message indicating that information is unavailable.


Here the transcription or video URL:

---
{formparagraph: name=YouTube Video URL or Transcription}
---

```

# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->
This project is a Retrieval-Augmented Generation (RAG) system designed to answer questions about Computer Science professors at Wellesley College using student reviews collected from Rate My Professors.

This knowledge is valuable because official course catalogs and faculty profiles provide information about course content and academic credentials, but they do not capture students' experiences with teaching style, workload, grading practices, accessibility, lecture quality, or course difficulty. By retrieving information from student reviews, this system helps students make more informed decisions about course selection and professor preferences. This information can be difficult to find through official channels because it is based on personal student experiences and feedback rather than institutional descriptions.
---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Yaniv Yacoby at Wellesley College | Rate My Professors review of Yaniv Yacoby |https://www.ratemyprofessors.com/professor/3069922|
| 2 |Smaranda Sandu at Wellesley College | Rate My Professors review of Smaranda Sandu |https://www.ratemyprofessors.com/professor/2773795|
| 3 |Vinitha Gadiraju at Wellesley College | Rate My Professors review of Vinitha Gadiraju |https://www.ratemyprofessors.com/professor/3099596|
| 4 |Scott Anderson at Wellesley College | Rate My Professors review of Scott Anderson |https://www.ratemyprofessors.com/professor/1353201|
| 5 |Carolyn Anderson at Wellesley College | Rate My Professors review of Carolyn Anderson  |https://www.ratemyprofessors.com/professor/2756316|
| 6 |Christine Bassem at Wellesley College | Rate My Professors review of Christine Bassem |https://www.ratemyprofessors.com/professor/2093511|
| 7 |Brian Brubach at Wellesley College | Rate My Professors review of Brian Brubach  |https://www.ratemyprofessors.com/professor/2649411|
| 8 |Brian Tjaden at Wellesley College | Rate My Professors review of Brian Tjaden |https://www.ratemyprofessors.com/professor/1707327|
| 9 |Stella Kakavouli at Wellesley College | Rate My Professors review of Stella Kakavouli |https://www.ratemyprofessors.com/professor/2716124|
| 10 |Peter Mawhorter at Wellesley College | Rate My Professors review of Peter Mawhorter |https://www.ratemyprofessors.com/professor/2506763|
---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**
500 characters
**Overlap:**
100 characters
**Why these choices fit your documents:**
I used 500-character chunks because the professor reviews are relatively short and contain individual opinions, ratings, and course experiences. This size keeps related information together while remaining small enough for retrieval. I used a 100-character overlap to reduce the chance of important information being split between chunks.

Before chunking, I performed basic preprocessing by normalizing whitespace and removing HTML tags if present. However, some repeated website text and page elements remained in the final documents.
**Final chunk count:**
84 chunks
---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**  
all-MiniLM-L6-v2 from Sentence Transformers

**Production tradeoff reflection:**  
I chose all-MiniLM-L6-v2 because it is lightweight, fast, runs locally, and works well for semantic search on short English text chunks like student reviews. Since my corpus is small, this model is practical and does not require an external embedding API.

If I were deploying this system for real users and cost was not a constraint, I would consider a stronger embedding model with higher retrieval accuracy and longer context support. I would also weigh latency, multilingual support, and whether the model should run locally or through an API. A larger API-hosted model might produce better retrieval results, especially for nuanced student opinions, but it could also be slower and more expensive.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

The system passes the retrieved document chunks to the LLM as context and uses the following grounding instruction:

"You are a grounded assistant answering questions about Wellesley professor reviews. Use only the provided context chunks to answer. Do not use outside knowledge. If the context does not contain enough information, say: 'I don't have enough information in the retrieved reviews to answer that.'"

The retrieved chunks are inserted directly into the prompt before the user's question. The system retrieves the top 5 most relevant chunks from ChromaDB and provides them as context for the model. This limits the model to answering based on the retrieved professor review documents rather than relying on general knowledge.

**How source attribution is surfaced in the response:**

Each retrieved chunk is stored with metadata containing the source filename and chunk ID. After retrieval, the system collects the source information and returns it alongside the generated answer. Source attribution is therefore programmatically generated rather than relying solely on the language model to cite sources correctly. The interface displays the answer and a list of source documents used to generate the response.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What do students say about taking Vinitha Gadiraju's classes? | Students generally find her caring, relatable, and clear in her explanations.                                                   | The system reported that Vinitha's classes are clear, to-the-point, and focused on problem-solving. It noted that students found her caring and relatable, while one review mentioned less favorable office hours. | Partially Relevant | Accurate          |
| 2 | What do students think about Smaranda Sandu's teaching?       | Students generally view her as helpful, supportive, and effective as an instructor.                                             | The system reported that Smaranda Sandu is kind, helpful, and available to support students. It noted that students appreciated her teaching approach, clear grading criteria, and generous retake policy.         | Relevant           | Accurate          |
| 3 | What do people think about Stella Kakavouli's teaching?       | Students have mixed opinions but generally describe her as kind and supportive, with some criticism of organization or grading. | The system reported that Stella is kind and caring, and that some students would take her class again. It also noted criticism regarding unclear grading and less useful lab activities.                           | Relevant           | Accurate          |
| 4 | What do people say about Yaniv Yacoby's classes?              | Students generally view him positively, appreciate his lectures, and note that he cares about student success.                  | The system reported that Yaniv gives great lectures, cares about student success, collects and responds to student feedback, and encourages participation.                                                         | Relevant           | Accurate          |
| 5 | What do people think about retaking Scott Anderson's classes? | The system should summarize opinions from Scott Anderson reviews.                                                               | The system stated that it did not have enough information about Scott Anderson and instead referenced Carolyn Anderson, a different professor.                                                                     | Partially Relevant | Inaccurate        |


**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

What do people think about retaking Scott Anderson's classes?

**What the system returned:**

The system retrieved mostly unrelated chunks from other professor files, including Brian Brubach, Brian Tjaden, and Vinitha Gadiraju, instead of primarily retrieving chunks from `Scott Anderson.txt`. Because the retrieved context was not focused on Scott Anderson, the generated answer could not reliably answer the question.

**Root cause (tied to a specific pipeline stage):**

The failure happened during the retrieval stage. The embedding model retrieved chunks that were semantically similar to the general idea of taking or retaking classes, but it did not strongly prioritize the exact professor name. The Rate My Professors documents also contained repeated boilerplate text such as ratings, similar professors, thumbs up/down labels, and course metadata. This noise likely weakened the semantic signal of each chunk and made it easier for ChromaDB to return chunks from the wrong source.

**What you would change to fix it:**

I would improve cleaning by removing repeated Rate My Professors boilerplate before chunking. I would also add metadata filtering so that if a user asks about a specific professor, the system first restricts retrieval to that professor's document. Another improvement would be to include the professor's name at the beginning of every chunk so the embedding model has a stronger signal about which professor each chunk describes.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

The specification helped me break the project into clear stages: ingestion, chunking, retrieval, generation, and evaluation. By following these milestones one at a time, I was able to test each component before building the next. This made it much easier to identify problems, such as document-loading issues and retrieval errors, before they affected the entire system.

**One way my implementation diverged from the spec, and why:**

My implementation diverged from the spec in the amount of document cleaning performed before chunking. The specification recommended removing navigation elements, repeated page content, and other boilerplate text, but I only performed basic cleaning such as removing HTML tags and normalizing whitespace. As a result, some Rate My Professors page elements remained in the documents, which likely contributed to retrieval errors and reduced the precision of the embedding and retrieval stages.


---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

* *What I gave the AI:*
  I provided my document sources, chunking strategy, and the requirements for Milestone 3. I asked the AI to generate a Python script that would load all `.txt` files, clean the text, and split documents into overlapping chunks.

* *What it produced:*
  The AI generated an `ingest.py` script containing functions for loading documents, cleaning text, and creating chunks with a fixed chunk size and overlap.

* *What I changed or overrode:*
  I corrected file path issues, moved my documents into the correct folder, and verified that the chunks were being created properly. I also adjusted the code to work with my project structure and tested the output to ensure the documents loaded correctly.

**Instance 2**

* *What I gave the AI:*
  I provided my retrieval plan, embedding model choice (`all-MiniLM-L6-v2`), ChromaDB requirements, and the project architecture diagram. I asked the AI to implement embeddings, vector storage, retrieval, and grounded generation using Groq.

* *What it produced:*
  The AI generated code for embedding document chunks, storing them in ChromaDB, retrieving the top-k results, connecting to the Groq API, and building a Gradio interface for user queries.

* *What I changed or overrode:*
  I fixed syntax errors, corrected API key configuration issues, tested retrieval quality, and modified the grounding prompt to ensure the model answered only from retrieved documents. I also verified source attribution and evaluated retrieval performance using multiple test questions.


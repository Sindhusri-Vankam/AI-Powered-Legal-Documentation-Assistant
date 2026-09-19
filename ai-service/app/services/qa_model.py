from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from langchain_core.prompts import PromptTemplate
import torch


MODEL_NAME = "google/flan-t5-base"


tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_NAME
)


qa_prompt = PromptTemplate.from_template(
    """Answer the question using only the information in the context.

Context:
{context}

Question:
{question}

Answer:"""
)


def generate_answer(question, relevant_chunks):

    context = "\n".join(relevant_chunks)

    prompt = qa_prompt.format(
        context=context,
        question=question
    )

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=100,
            do_sample=False,
            num_beams=4
        )

    answer = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    return answer.strip()
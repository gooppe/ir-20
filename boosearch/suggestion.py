import re
import torch
from typing import Tuple

from transformers import OpenAIGPTLMHeadModel, OpenAIGPTTokenizer


def load_model(name: str) -> Tuple[OpenAIGPTLMHeadModel, OpenAIGPTTokenizer]:
    model = OpenAIGPTLMHeadModel.from_pretrained(name)
    tokenizer = OpenAIGPTTokenizer.from_pretrained(name)
    model.eval()
    return model, tokenizer


def sample_text(text: str, n_sugg: int = 3) -> str:
    model, tokenizer = load_model("openai-gpt")

    tokens = tokenizer.encode(text)
    max_seq_len = len(tokens) + n_sugg
    encoded_tensor = torch.tensor([tokens])
    predicted = model.generate(
        encoded_tensor, max_length=max_seq_len + 10, do_sample=True
    )
    generated = tokenizer.decode(predicted[0])
    generated = " ".join(re.split(r"\W+", generated)[:max_seq_len])

    return generated

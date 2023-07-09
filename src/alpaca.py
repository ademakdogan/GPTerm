import torch
#from langchain.embeddings import LlamaCppEmbeddings
from langchain.llms import HuggingFacePipeline
from transformers import LlamaForCausalLM, LlamaTokenizer, pipeline


class Alpaca:

    def __init__(self, model_path: str, device: str) -> None:

        self.model_path = model_path
        self.device = device
        # Parameter of pipeline
        self.max_length = 2048
        self.temperature = 0.6
        self.top_p = 0.95
        self.repetition_penalty = 1.2

    def get_model(self) -> LlamaForCausalLM:

        if self.device == 'cuda':
            model = LlamaForCausalLM.from_pretrained(
                self.model_path,
                load_in_8bit=True,
                device_map='auto',
                torch_dtype=torch.float16,
            )
        elif self.device == 'mps':
            model = LlamaForCausalLM.from_pretrained(
                self.model_path,
                device_map={"": 'mps'},
                torch_dtype=torch.float16,
            )
        elif self.device == 'cpu':
            model = LlamaForCausalLM.from_pretrained(
                self.model_path,
                device_map={"": 'cpu'},
                low_cpu_mem_usage=True,
            )

        return model

    def get_tokenizer(self) -> LlamaTokenizer:
        return LlamaTokenizer.from_pretrained(self.model_path)

    def get_llm_pipeline(self) -> HuggingFacePipeline:
        model = self.get_model()
        tokenizer = self.get_tokenizer()
        pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_length=self.max_length,
            temperature=self.temperature,
            top_p=self.top_p,
            repetition_penalty=self.repetition_penalty,
        )
        local_llm = HuggingFacePipeline(pipeline=pipe)

        return local_llm

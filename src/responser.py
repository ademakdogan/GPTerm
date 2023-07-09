import argparse
import codecs
import json
import re
from typing import Any, Dict, Union

import langchain
from ctransformers.langchain import CTransformers
from langchain import PromptTemplate
from langchain.llms import HuggingFacePipeline, OpenAI

from alpaca import Alpaca


class ShellResponser:

    def __init__(self, model_type: str, model_path: Union[str, None],
                 openai_key: Union[str, None], device: str) -> None:

        #conf_path: str = get_final_path(1, ["conf.json"])
        self.openai_key = openai_key
        self.model_path = model_path
        self.device = device
        self.llm: object
        self.config: Dict[str, Any] = {
            'temperature': 0.1,
            'max_new_tokens': 6000,
            'stream': True
        }
        self.model_type = model_type
        # Model conditions
        if self.model_type == 'chatgpt':
            self.llm = self._get_chatgpt_model()
        elif self.model_type == 'alpaca':
            self.llm = self._get_alpaca_model()
        elif self.model_type == 'wizardcoder':
            self.llm = self._get_wizardcoder_model()
        elif self.model_type == 'mpt':
            self.llm = self._get_mpt_model()
        else:
            raise Exception(
                "Avaliable model types are 'chatgpt', 'alpaca' and 'wizardcoder'."
            )

    def _get_alpaca_model(self) -> HuggingFacePipeline:

        return Alpaca(self.model_path, self.device).get_llm_pipeline()

    def _get_chatgpt_model(self) -> langchain.llms.openai.OpenAI:

        return OpenAI(openai_api_key=self.openai_key)

    def _get_wizardcoder_model(self) -> CTransformers:

        return CTransformers(model=self.model_path,
                             model_type='starcoder',
                             lib='basic',
                             config=self.config)

    def _get_mpt_model(self) -> CTransformers:

        return CTransformers(model=self.model_path,
                             model_type='mpt',
                             lib='basic',
                             config=self.config)

    @staticmethod
    def json_extractor(text: str) -> str:

        string_without_escapes = codecs.decode(text, 'unicode_escape')
        final_str = ' '.join(string_without_escapes.split())
        # Extract the dictionary part using regular expression
        pattern = r'{\s*"command":\s*".*?"\s*}'
        match = re.search(pattern, final_str)
        if match:
            dictionary_part = match.group(0)

            #print(dictionary_part)
            start_idx = dictionary_part.find('command')
            if dictionary_part[start_idx - 1] == "'":
                dictionary_part[start_idx - 1] = '"'
            if dictionary_part[start_idx + 10] == "'":
                dictionary_part[start_idx + 10] = '"'
            if dictionary_part[start_idx + 11] == "'":
                dictionary_part[start_idx + 11] = '"'
            if dictionary_part[-2] == "'":
                dictionary_part[-2] = '"'
            if dictionary_part[-3] == "'":
                dictionary_part[-3] = '"'

            sub_text = dictionary_part[start_idx + 12:-4].replace('"', "'")
            dictionary_res = dictionary_part[:start_idx +
                                             12] + sub_text + dictionary_part[
                                                 -4:]
            #print(dictionary_res)
            return dictionary_res
        else:
            return ''

    def prompt_to_command(self, prompt: str) -> Dict[str, str]:

        prompt = prompt[2:]
        template = """
        Convert shell commands from given following plain text and put the result in json--> Following plain text: {prompt}. 
        --------
        Put your shell command in the  JSON structure with key name is 'command'.
        The result has to be in json format and use double quotes for json.
        Note: Your command will be run on terminal
        


        """
        pr_ = PromptTemplate(input_variables=["prompt"], template=template)
        final_prompt = pr_.format(prompt=prompt)
        gpt_response = self.llm(final_prompt)
        if gpt_response == '':
            return {"command": ""}
        if self.model_type != 'chatgpt':
            extracted_response = ShellResponser.json_extractor(gpt_response)
        else:
            extracted_response = gpt_response
        #extracted_response = ShellResponser.json_extractor(gpt_response)
        gpt_query: Dict["str", "str"] = json.loads(extracted_response)

        return gpt_query

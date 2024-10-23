import tensorflow_hub as hub
import subprocess
from rasa.nlu.tokenizers.tokenizer import Tokenizer
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.constants import TOKENS_NAMES, TEXT_ATTRIBUTE
from rasa.nlu.components import ComponentBuilder

class ConveRTTokenizer(Tokenizer):
    provides = [TOKENS_NAMES[TEXT_ATTRIBUTE]]

    def __init__(self, component_config=None):
        super().__init__(component_config)
        self.convt_model = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

    def tokenize(self, message: Message, attribute: str) -> None:
        text = message.get(attribute)
        tokens = self.convt_model.tokenize([text])[0].numpy().decode('utf-8').split()
        message.set(
            TOKENS_NAMES[attribute],
            [self._convert_token(token) for token in tokens],
            add_to_output=True,
        )

component_builder = ComponentBuilder()
component_builder.register_component("ConveRTTokenizer", ConveRTTokenizer)
   

# 使用 subprocess 调用 rasa train 命令
subprocess.run(["rasa", "train"])

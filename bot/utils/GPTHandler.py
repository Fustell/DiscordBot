import openai


class GPTHandler:

    def __init__(self, api_key,max_tokens=4000, temperature=1.0,model="text-davinci-003"):
        self.__api_key = api_key
        self.__model = model
        self.__max_tokens = max_tokens
        self.__temperature = temperature

    async def make_response(self, prompt: str) -> str:
        response = openai.Completion.create(
            model=self.__model,
            prompt=prompt,
            temperature=self.__temperature,
            max_tokens=self.__max_tokens,
        )
        return response.choices[0].text


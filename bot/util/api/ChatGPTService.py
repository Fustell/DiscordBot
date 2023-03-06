import openai


class ChatGPTService:

    def __init__(self, api_key,max_tokens=3000, temperature=0,model="text-davinci-003"):
        self.__api_key = api_key
        self.__model = model
        self.__max_tokens = max_tokens
        self.__temperature = temperature

    async def make_response(self, prompt: str, id:int) -> str:
        response = openai.Completion.create(
            model=self.__model,
            prompt=prompt,
            temperature=self.__temperature,
            max_tokens=self.__max_tokens,
            user=f"discord user id: {id}"
        )
        return response.choices[0].text
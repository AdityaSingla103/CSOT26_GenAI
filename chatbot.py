import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()
models = ["openrouter/owl-alpha", "openrouter/free","z-ai/glm-4.5-air:free","openai/gpt-oss-20b:free"]

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)



class ChatAgent:
    
    def __init__(self):
        print("Enter the digit corresponding to the model you want to use for the chatbot:")
        print("Available models:")
        for i, m in enumerate(models):
            print(f"{i} - {m}")
        selected_model = input("Select a model from the above list: ")
        if not selected_model.isdigit() or int(selected_model) >= len(models):
            print("Invalid model selected. Defaulting to openrouter/free.")
            selected_model = "openrouter/free"
        else:
            selected_model = models[int(selected_model)]
        system_instruction = input("Enter a system instruction for the assistant (or press Enter to use the default): ")
        if not system_instruction:
            system_instruction = "You are a helpful assistant."

        self.model = selected_model
        self.max_history = input("Enter the maximum number of recent turns to keep in context (default 10): ")
        if not self.max_history.isdigit():
            self.max_history = 10
        else:
            self.max_history = int(self.max_history)
        self.messages = [{"role": "system", "content": system_instruction}]
        self.last_response = None

    def call_model(self, user_input: str) -> str:
        self.messages.append({"role": "user", "content": user_input})
        if len(self.messages) > self.max_history * 2 + 1:  # +1 for system message
            self.messages = [self.messages[0]] + self.messages[-self.max_history*2:]

        response = client.chat.completions.create(
            model=self.model,
            messages=self.messages
        )
        assistant_reply = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": assistant_reply})
        self.last_response = response
        return assistant_reply
    
    def stream_model(self, user_input: str):
        print("Entered Streaming mode")
        self.messages.append({"role": "user", "content": user_input})
        if len(self.messages) > self.max_history * 2 + 1:  # +1 for system message
            self.messages = [self.messages[0]] + self.messages[-self.max_history*2:]

        response = client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            stream=True
        )
        assistant_reply = ""
        for chunk in response:
            delta = chunk.choices[0].delta
            if delta.content is not None:
                print(delta.content, end='', flush=True)
                assistant_reply += delta.content    
        print()  # for newline after completion
        self.messages.append({"role": "assistant", "content": assistant_reply})
        self.last_response = response
        return assistant_reply
    
    def start_conversation(self):
        print("Chat started. Type 'exit' to quit.\n")
        while True:
            user_input = input("You: ")
            if user_input.lower() in ['exit', 'quit']:
                print("Chat ended.")
                break
            elif user_input.lower() == '/reset':
                self.messages = [{"role": "system", "content": self.messages[0]["content"]}]
                print("Chat history reset.")
                continue
            elif user_input.lower() == '/tokens':
                if self.last_response != None:
                    print(f"Tokens used: {self.last_response.usage.total_tokens}")
                else:
                    print("No API call made yet.")
                continue
            elif user_input.lower() == '/compact':
                compacted_message = self.call_model("Summarize the following conversation in a concise manner so that all the context of the conversation is preserved and it fits within the context window: " + " ".join([m["content"] for m in self.messages if m["role"] != "system"]))
                self.messages = [self.messages[0], {"role": "system", "content": "You and the user had a conversation, to manage the context window the converation has been summarized. The following is a compacted summary of the conversation so far: " + compacted_message}]
                continue
                

            self.stream_model(user_input)
    

if __name__ == "__main__":

    chatbot = ChatAgent()
    chatbot.start_conversation()





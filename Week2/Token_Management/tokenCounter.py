import tiktoken
encoding = tiktoken.encoding_for_model("gpt-4o-mini")
text="My name is Bilal"
tokens = encoding.encode(text)
print(text)
print("Total tokens in text: ", len(tokens))

# from openai import OpenAI

# # Replace 'your-api-key' with your actual OpenAI API key
# OpenAI.api_key = "sk-proj-NreB2PWGx3wYgVfLedaET3BlbkFJnaGfVFtBSRC8gGUKH6bk"

# while True:
#     # This is the prompt you want to send to ChatGPT
#     ask = input("Enter your question : ")
#     prompt = ask

#     if 'bye' in ask.lower():
#         break
#     # Send the prompt to ChatGPT and get the response
#     response = OpenAI.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "user", "content": prompt}
#         ]
#     )

#     # Print the response from ChatGPT
#     # print(response.choices[0].message)
#     print(response.choices[0].message.content.strip())
#     # response_text = response.choices[0].message
#     # print(response_text)
    
#     print(type(response))

#     print("------------------------------------------------")
    
#     # I wrote this line response.choices[0].message['content'] to print the response from chatgpt api and i got an error saying TypeError: 'ChatCompletionMessage' object is not subscriptable , can you help me fix it ?




from openai import OpenAI

client = OpenAI(api_key="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")

# client = OpenAI(api_key="sk-proj-NreB2PWGx3wYgVfLedaET3BlbkFJnaGfVFtBSRC8gGUKH6bk")
# Replace 'your-api-key' with your actual OpenAI API key

while True :
    # This is the prompt you want to send to ChatGPT
    prompt = input("Ask me ?")

    if 'bye' in prompt.lower():
        break
    # Send the prompt to ChatGPT and get the response
    response = client.chat.completions.create(model="gpt-4-turbo",
    messages=[
        {"role": "user", "content": prompt}
    ])

    # Print the response from ChatGPT
    print(response.choices[0].message.content.strip())
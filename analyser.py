def create_ass():

    assistant = client.beta.assistants.create(
      name="Math Tutor",
      instructions="You are a personal math tutor. Write and run code to answer math questions.",
      tools=[{"type": "code_interpreter"},{"type": "retrieval"}],
      model="gpt-4-turbo-preview",
    )
    thread = client.beta.threads.create()
    return assistant,thread
def get_reponse(thread,assistant):
    from typing_extensions import override
    from openai import AssistantEventHandler
    # First, we create a EventHandler class to define
    # how we want to handle the events in the response stream.
     
    class EventHandler(AssistantEventHandler):    
      @override
      def on_text_created(self, text) -> None:
        print(f"\nassistant > ", end="", flush=True)
          
      @override
      def on_text_delta(self, delta, snapshot):
        print(delta.value, end="", flush=True)
          
      def on_tool_call_created(self, tool_call):
        print(f"\nassistant > {tool_call.type}\n", flush=True)
      
      def on_tool_call_delta(self, delta, snapshot):
        if delta.type == 'code_interpreter':
          if delta.code_interpreter.input:
            print(delta.code_interpreter.input, end="", flush=True)
          if delta.code_interpreter.outputs:
            print(f"\n\noutput >", flush=True)
            for output in delta.code_interpreter.outputs:
              if output.type == "logs":
                print(f"\n{output.logs}", flush=True)
     
    # Then, we use the `create_and_stream` SDK helper 
    # with the `EventHandler` class to create the Run 
    # and stream the response.
     
    with client.beta.threads.runs.create_and_stream(
      thread_id=thread.id,
      assistant_id=assistant.id,
      instructions="The user has a premium account and make sure the reponses are good and polite",
      event_handler=EventHandler(),
    ) as stream:
      stream.until_done()
def file_Add(path):
    file = client.files.create(
      file=open(path, "rb"),
      purpose='assistants'
    )
    return file
def update_assist(file_idsss,assistant):
    my_updated_assistant = client.beta.assistants.update(assistant.id,file_ids=file_idsss)
    return 'Files added'
def add_message(thread,message):
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=message )
def main():
    print("loading the assistant")
    bot_name ='Document_Helper'
    from openai import OpenAI
    global client 
    client = OpenAI()
    assistant,thread=create_ass()
    print("Disclaimer :: ---- I am still learning and will get better over time please dont be MAD AT ME") 
    print("Let's chat! (type 'quit' to exit)")
    print("To add file (type 'File')")
    bot_name ='infomania'
    file_ids=[]
    resp_list=[]
    intent_list =[]
    curr_log=[]
    sent_list=[]
    flag = 0 
    while True:
        
        sentence = input("You: ")
        curr_log.append(('You :' + sentence))
        sent_list.append(sentence)
        if flag == 1 : 
            #sentence = sentence.replace("\\", "/")
            file = file_Add(sentence)
            file_ids.append(file.id)
            update_assist(file_ids,assistant)
        if sentence == "quit":
            break
        if sentence =='File':
            print('Enter the file path')
            flag = 1
        else:
            if flag == 1:
                print("Files added sucessfully")
                flag= 0
            else :
                print('\n')
                add_message(thread,sentence)
                get_reponse(thread,assistant)
                print('\n')
if __name__ == "__main__":
    main()
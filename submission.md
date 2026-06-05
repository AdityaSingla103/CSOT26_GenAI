We had to implement ChatAgent class which was model agnostic, we also had to make it configurable at the user end. So I have given the user to choose and agent, give system instructions, and set the length of chat history. I have only added 4 free models, though it can be kept textual input based, where the user can just type the code of the model.
I have implemented 2 different functions, one streams the output the other gives the full output at once, initially I was giving user the choice whether he wants to stream or get full output at once but streaming was better so later I removed the choice.


The three commands - compact reset and tokens, have also been fed in the default system instructions, so if the user mistypes the llm responds to check the mistype.
I also tried implementing that if prompt length reaches near context window, the conversation hisory is auto compacted. 

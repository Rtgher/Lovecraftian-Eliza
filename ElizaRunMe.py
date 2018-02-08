__author__="Radu Traian Gherman"
__email__="rtgher@essex.ac.uk"
__PRID__="GHERM52503"
__MODULECODE__="CE314"
"""
Part 3: Write your own version of ELIZA
"""
#IMPORT SECTION
from nltk import word_tokenize
from ElizaData import Random_Greetings, Random_Introduction, Random_Apologies, Random_Excuses, Random_Offers
from ElizaData import Ask_Location, Ask_Greeting, Ask_Introduction, Ask_Time, Ask_Transport, Ask_SetTime, Ask_End
from ElizaData import Key_Locations
from random import choice
from Utility import getTrainedUnigramTagger

##
#
tagger = getTrainedUnigramTagger(10000)
finished = False
saidHiOnceAlready = False
checks = { "location" : "", "time" : "", "transport" : "" } 
def ElizaResponse (response) :
    """ Takes an unparsed response
    and replaces all slots marked by brackets
    {slot} with its corresponding task.
    """
    response = "Eliza: " + response
    response = response.replace("{Greeting}", choice(Random_Greetings))
    response = response.replace("{Introduction}", choice(Random_Introduction))
    response = response.replace("{Excuse}", choice(Random_Excuses))
    response = response.replace("{Apology}", choice(Random_Apologies))
    response = response.replace("{Offer}", choice(Random_Offers))

    response = response.replace("{location}", checks["location"])
    response = response.replace("{time}", checks["time"])
    response = response.replace("{transport}", checks["transport"])

    print(response)
    
def respondTo(message) :
    """ This function goes through all the user's input,
    and then prepares Eliza's response as appropiate.
    Calls ElizaResponse to respond.
    """
    response = ""
    global checks
    global finished
    global saidHiOnceAlready
    checks = { "location" : "", "time" : "", "transport" : "" } 
    #logic
    tokens = word_tokenize(message)
    tagToks = tagger.tag(tokens)
    tagged_tokens ={}
    for tag in tagToks :
        tagged_tokens[tag[0]] = tag[1]
    previous = ""
    for token in tokens :
        if token in Ask_End :
            finished = True
            return
        if token in Ask_Greeting :
            if saidHiOnceAlready :
                response = "I thought we already said hi. Oh well, here you go again : {Greeting}"
            else :
                saidHiOnceAlready = True
        if token in Ask_SetTime :
            if tagged_tokens[token] != "" and tagged_tokens[token] in ["AP", "OD"] : checks["time"] = checks["time"] + token
            if tagged_tokens[previous] in ["AT", "AP", "OD"] : checks["time"] = previous +" "+ token
            else : checks["time"] = token
        #if tagged_tokens[token] in ["NP","NN"] :
        if token in Ask_Transport :
            checks["transport"] = token
        if token in Key_Locations :
            checks["location"] = token
        previous = token
    response = "{Apology}"
    if checks["transport"] != "" :
        response = response + " no {transport}s "
    else : response = response + " no transports are available "
    if checks["location"] != "" :
        response = response + "to {location}"
    if checks["time"] != "" :
        response = response + " for {time} "
    response = response + " because of{Excuse}. \nEliza:{Offer}"
    ElizaResponse(response)
    
#start convo
ElizaResponse("{Greeting} {Introduction}")

while not finished :
    userInput = input("You: " )
    respondTo(userInput)

ElizaResponse("Thank you for your time. Sorry I wasn't of much help. Stay safe!")


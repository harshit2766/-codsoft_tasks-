import re
import random
from datetime import datetime
 
BOT_NAME = "RuleBot"
 
 
# Each rule = (regex pattern, list of possible responses)
# {0}, {1}... in a response are filled with regex capture groups.
RULES = [
    (r"\b(hi|hello|hey|greetings)\b",
        ["Hello! How can I help you today?",
         "Hi there! What's on your mind?",
         "Hey! Good to see you."]),
 
    (r"\bhow are you\b",
        ["I'm just a program, but I'm running smoothly! How about you?",
         "Doing great, thanks for asking!"]),
 
    (r"\bmy name is (\w+)",
        ["Nice to meet you, {0}!", "Hello, {0}! How can I help you?"]),
 
    (r"\bwhat('?s| is) your name\b",
        [f"I'm {BOT_NAME}, your friendly rule-based chatbot."]),
 
    (r"\b(thanks|thank you)\b",
        ["You're welcome!", "Anytime!", "Glad I could help."]),
 
    (r"\bhelp\b",
        ["I can chat about basic things: greetings, my name, the time, "
         "the date, and simple small talk. Try asking me something!"]),
 
    (r"\bweather\b",
        ["I can't check live weather, but I hope it's nice outside!"]),
 
    (r"\btime\b",
        [lambda m: f"The current time is {datetime.now().strftime('%H:%M:%S')}."]),
 
    (r"\b(date|today)\b",
        [lambda m: f"Today's date is {datetime.now().strftime('%Y-%m-%d')}."]),
 
    (r"\bjoke\b",
        ["Why don't programmers like nature? Too many bugs.",
         "I told my computer I needed a break, and it said no problem — "
         "it'll go to sleep."]),
 
    (r"\b(bye|goodbye|exit|quit)\b",
        ["Goodbye! Have a great day!", "See you later!", "Bye! Take care."]),
]
 
 
def get_response(user_input):
    original = user_input.strip()
    text = original.lower()
 
    for pattern, responses in RULES:
        match = re.search(pattern, text)
        if match:
            # Re-match against the original (un-lowercased) text so any
            # captured groups (like a name) keep their original casing.
            original_match = re.search(pattern, original, flags=re.IGNORECASE)
            if original_match:
                match = original_match
            reply = random.choice(responses)
            if callable(reply):
                return reply(match)
            try:
                return reply.format(*match.groups())
            except (IndexError, KeyError):
                return reply
 
    # Fallback responses when no rule matches
    fallbacks = [
        "I'm not sure I understand. Could you rephrase that?",
        "Interesting — tell me more.",
        "I don't have a rule for that yet. Try asking about my name, "
        "the time, the date, or say hello!",
    ]
    return random.choice(fallbacks)
 
 
def chat():
    print(f"{BOT_NAME}: Hello! I'm a simple rule-based chatbot. "
          "Type 'quit' to exit.\n")
 
    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
 
        if re.search(r"\b(bye|goodbye|exit|quit)\b", user_input.lower()):
            print(f"{BOT_NAME}: {get_response(user_input)}")
            break
 
        response = get_response(user_input)
        print(f"{BOT_NAME}: {response}")
 
 
if __name__ == "__main__":
    chat()
 
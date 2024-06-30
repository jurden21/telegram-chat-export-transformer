import json

json_name = "result.json"
json_file = open(json_name, "r", encoding="UTF-8")
json_data = json.load(json_file)

text_name = "text.txt"
text_file = open(text_name, "w", encoding="UTF-8")

for message in json_data["messages"]:
    date = message["date"][0:10]
    time = message["date"][11:19]
    sender = str(message["from"])
    message_text = ""

    text_entities = message["text_entities"]
    for entity in text_entities:
        if entity["type"] == "plain":
            message_text += entity["text"]
        if entity["type"] == "link":
            message_text += entity["text"]
        if entity["type"] != "plain" and entity["type"] != "link":
            print("Script warning =", str(entity["type"]))
            text_file.write("Script warning - Please add a handler of entity:\n")
            text_file.write("message = " + str(message) + "\n")
            text_file.write("entity = " + str(entity) + "\n")
            text_file.write("text = " + message_text + "\n")
    text_file.write(date + " " + time + " - " + sender + ": " + message_text + "\n")

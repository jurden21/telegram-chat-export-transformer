import json
from datetime import datetime

def parse_datetime(date_str: str) -> tuple[str, str]:
    if not date_str:
        return "", ""
    try:
        datetime_value = datetime.fromisoformat(date_str)
        return datetime_value.date().isoformat(), datetime_value.time().strftime("%H:%M:%S")
    except ValueError:
        date_value = date_str[0:10] if len(date_str) >= 10 else date_str
        time_value = date_str[11:19] if len(date_str) >= 19 else ""
        return date_value, time_value

json_name = "result.json"
text_name = "text.txt"

with open(json_name, "r", encoding="utf-8") as json_file:
    json_data = json.load(json_file)

with open(text_name, "w", encoding="UTF-8") as text_file:

    for message in json_data["messages"]:
        date, time = parse_datetime(message["date"])

        if message["type"] == "service":
            text_file.write(date + " " + time + " - Service message: " + str(message) + "\n")
            continue

        message_text = ""
        sender = str(message.get("from", "Unknown"))
        photo = str(message.get("photo", ""))
        if photo != "":
            text_file.write(date + " " + time + " - " + sender + ": Photo - " + photo + "\n")

        text_entities = message["text_entities"]

        for entity in text_entities:
            if entity["type"] == "plain":
                message_text += entity["text"]

            if entity["type"] == "link":
                message_text += entity["text"]

            if entity["type"] == "blockquote":
                text_file.write(date + " " + time + " - " + sender + ": > " + entity["text"] + "\n")

            if entity["type"] != "plain" and entity["type"] != "link" and entity["type"] != "blockquote":
                print("Script warning =", str(entity["type"]))
                text_file.write("Script warning - Please add a handler of entity:\n")
                text_file.write("message = " + str(message) + "\n")
                text_file.write("entity = " + str(entity) + "\n")
                text_file.write("text = " + message_text + "\n")

        if message_text.strip() != "":
            text_file.write(date + " " + time + " - " + sender + ": " + message_text.strip() + "\n")

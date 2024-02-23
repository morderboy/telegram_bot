import xml.etree.ElementTree as ET

tree = ET.parse("message.xml")
root = tree.getroot()

def get_message(token: str):
    start_message = root.find(f"./message[@key='{token}']")

    return start_message.find("text").text.replace("\\n", "\n")
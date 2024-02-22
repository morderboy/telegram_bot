import xml.etree.ElementTree as ET

tree = ET.parse("message.xml")
root = tree.getroot()

def get_start():
    start_message = root.find("./message[@key='start']")

    return start_message.find("text").text

def get_menu():
    start_message = root.find("./message[@key='menu']")

    return start_message.find("text").text
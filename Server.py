# sources

# using xml-rpc in python
# https://www.youtube.com/watch?v=_8xXrFWcWao

# using xml.etree.ElamantTree in python
# https://www.youtube.com/watch?v=bWfAD7wAfOI


from xmlrpc.server import SimpleXMLRPCServer
import xml.etree.ElementTree as ET
from datetime import datetime

# Open "database"
xmlDB = "db.xml"
tree = ET.parse(xmlDB)
root = tree.getroot()

# Specifying a new server on localhost:5000
server = SimpleXMLRPCServer(('localhost', 5000), logRequests=True)

# Methods that can be called remotely using RPC
class RemoteMethods:

    # Add a new note to database using provided input
    def add_note(self, topic, title, text):
        try:
            # Input is not checked for XML vulnerabilities/other malicious input but it could be done here
            # If inputs are valid (Not empty in this case)
            if topic and title and text:
                # Timestamp is added server side at the time of the RPC
                time = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
                # Look for existing topic
                topic_element = root.find("./topic[@name='" + topic + "']")
                
                if topic_element:
                    print("Found existing topic.")

                # Create new topic if none is found
                else:
                    print("Existing topic was not found. Creating new topic...")
                    topic_element = ET.SubElement(root.find("."), "topic", attrib={"name": topic})
                
                # Create new subelements and set their values for the note
                note_element = ET.SubElement(topic_element, "note", attrib={"name": title})
                text_element = ET.SubElement(note_element, "text")
                text_element.text = text
                time_element = ET.SubElement(note_element, "timestamp")
                time_element.text = time
                print("New note added.")

                # Write changes to the file
                # Doing this after every note leads to awfully many
                # IO operations/requests to what ever database is used.
                # Better way would be to do this once every so often.
                # However if the server crashes the most recent data would be lost.
                tree.write(xmlDB)
                return "Note added"

            else:
                return "Error: some of the inputs were empty."
        except:
            return "Error: Something went wrong"

    # Find all matching notes, add them as dictionaries to a list and return the list
    def list_notes(self, topic):
        notes = []

        try:
            # Find all notes matching provided topic
            for note in root.findall("./topic[@name='" + topic + "']/"):
                # Find note data
                text = note.find(".//text").text
                time = note.find(".//timestamp").text

                # Add note to list as a dictionary
                notes.append({"title": note.attrib.get("name"), "text": text, "time": time})

            return notes
        except:
            return [{"Error": "Something went wrong"}]

# Make RPC methods available
server.register_instance(RemoteMethods())

# Starting and stopping the server
if __name__ == '__main__':
    try:
        print('Serving...')
        server.serve_forever()
    except KeyboardInterrupt:
        print('Exiting')


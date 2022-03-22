# sources

# using xml-rpc in python
# https://www.youtube.com/watch?v=_8xXrFWcWao


from xmlrpc.client import ServerProxy

proxy = ServerProxy('http://localhost:5000')

selection = 1

# Keep printing the menu until exit condition is met
while (selection != "0"):
    print("\n1) add note\n2) list notes by topic\n0) exit\n")
    selection = input("selection: ")

    # continue for exit condition to be met
    if selection == "0":
        continue

    # Get data for a new note and RPC add_note
    elif selection == "1":
        topic = str(input("Topic: "))
        title = str(input("Title: "))
        text = str(input("note: "))

        print(proxy.add_note(topic, title, text))

    # Get topic and and RPC list_notes
    elif selection == "2":
        topic = input("Topic: ")
        for note in proxy.list_notes(topic):
            print(note)


    # "stress test"
    # Adds 100 notes as fast as possible.
    # Not really useful because there seems to be ~3s delay between RPCs.
    elif selection == "5000":
        topic = "topic"
        title = "title"
        text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."

        for i in range(100):
            proxy.add_note(topic, title, text)
            print(i+1)

    # Adds 10 notes
    elif selection == "5001":
        topic = "topic"
        title = "title"
        text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."

        for i in range(10):
            proxy.add_note(topic, title, text)
            print(i+1)

    # Get # of database entries by topic
    elif selection == "5002":
        topic = "topic"
        print(len(proxy.list_notes(topic)))

    # for every non specified input
    else:
        print("That wasn't one of the choices!")

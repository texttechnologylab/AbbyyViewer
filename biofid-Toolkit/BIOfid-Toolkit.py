import BlockRemover
import HypernymPredictor
import HypernymTrainingSetCreator

# Print some hints

print("\nBIOfid Toolkit\n")
print("WARNING: This toolkit works only for Abbyy FineReader, Version 8.0\n")
print("This toolkit provides two tools for the work with the Abbyy FineReader")
print("output file format:\n")
print("1. BlockRemover\n\n2. HypernymPredictor\n\n3. HypernymTrainingSetCreator\n")
print("To select one tool, type 1, 2 or 3 on the console and press Enter.\n")

# Save the number of selected tool

tool = input(">>: ")

while (tool != "1" and tool != "2" and tool != "3"):
    print("Error: Please select 1, 2 or 3")
    tool = input(">>: ")

print("Select: " + tool)

# Check which tool was choosen, and generate a object

if (tool == "1"):
    blockremover = BlockRemover.BlockRemover()
elif (tool == "2"):
    hypernympredictor = HypernymPredictor.HypernymPredictor()
else:
    hypernymtrainingsetcreator = HypernymTrainingSetCreator.HypernymTrainingSetCreator()

exit = 1

# Methods for the tools and the number of parameters of every tool

command_blockremover = {"train" : 2, "train_from_bin" : 2, "export_as_xml" : 2, "export_as_image" : 3,
                        "export_decisiontree" : 1, "score" : 2 }
command_hypernympredictor = {"train" : 2, "export_tables" : 2, "score" : 1, "predict" : 2}
command_hypernymtrainingsetcreator = {"export_test_set" : 3, "export_training_set" : 3}

# Choose the commands for one tool

while(exit):

    command = input(">>: ")
    command = [i.strip() for i in command.split("-")]

    commands = command_blockremover if tool == "1" else (command_hypernympredictor if tool == "2" else command_hypernymtrainingsetcreator)

    if command[0] in commands:
        try:
            parameter = (str(["command[" + str(i) + "]" for i in range(1, commands[command[0]] + 1)]).strip("[]")).replace("'", "")
            exec(("print(blockremover." if tool == "1" else("print(hypernympredictor." if tool == "2" else "print(hypernymtrainingsetcreator.")) + command[0] + "(" + parameter + "))")
        except:
            print("Error: Wrong number of parameters")
    elif(command[0] == "exit"):
        exit = 0
    else:
        print("Unknown Command")

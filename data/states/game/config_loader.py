"""
making dict by splitting options with each [option]
"""

"""
REWRITE IT
"""
def option_load(path: str, loadnotes: False):
    options = {}
    note_counter = 0
    with open(path, "r") as f:
        for line in f.readlines():
            if line.strip():
                line = line.replace("\n", "")
                if line in ("[General]", "[Difficulty]", "[TimingOptions]", "[NoteTimings]"):
                    options[line] = {}
                    last_title = line
                else:
                    # here line without any spaces
                    line = line.replace(" ", "")
                    if "=" in line:
                        options[last_title][line.split("=")[0]] = line.split("=")[1]
                    elif last_title == "[NoteTimings]" and loadnotes:
                        # here line is the list
                        line = line.split(",")
                        options[last_title][note_counter] = {}
                        # single note
                        if len(line) == 3:
                            options[last_title][note_counter]["type"] = "single"
                            options[last_title][note_counter]["sound_name1"] = line[0]
                            options[last_title][note_counter]["end_timing1"] = line[1]
                            options[last_title][note_counter]["side"] = line[2]
                            note_counter += 1
                        # slider note
                        elif len(line) == 5:
                            options[last_title][note_counter]["type"] = "slider"
                            options[last_title][note_counter]["sound_name1"] = line[0]
                            options[last_title][note_counter]["sound_name2"] = line[1]
                            options[last_title][note_counter]["end_timing1"] = line[2]
                            options[last_title][note_counter]["end_timing2"] = line[3]
                            options[last_title][note_counter]["side"] = line[4]
                            note_counter += 1
    if options:
        return options
    else:
        return None

if __name__ == "__main__":
    pass
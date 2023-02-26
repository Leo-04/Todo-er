def data_to_string(items, tab=0):
        out_string = ""

        tabs = tab * "    "
        
        for i in range(0, len(items), 3):
            out_string += tabs + ("/" if items[i] else "#")
            out_string += items[i+1] + "\n"
            if len(items[i+2]):
                out_string += tabs + "{\n"
                out_string += data_to_string(items[i+2], tab+1)
                out_string += tabs + "}\n"

        return out_string

def string_to_data(string):
    items = [[]]

    i = 0
    while i < len(string):
        while i < len(string) and string[i] in " \t\n":
            i += 1
        if i >= len(string):break
        
        if string[i] == "#":
            if type(items[-1]) != list:
                items.append([])
            items.append(False)
            i += 1
        elif string[i] == "/":
            if type(items[-1]) != list:
                items.append([])
            items.append(True)
            i += 1
        elif string[i] == "{":
            i += 1
            ext_string = ""
            tab = 1
            while tab > 0 and i < len(string):
                while i < len(string) and string[i] != "\n":
                    ext_string += string[i]
                    i += 1
                ext_string += "\n"
                while string[i] in " \t\n":
                    i += 1
                if string[i] == "}":
                    tab -= 1
                elif string[i] == "{":
                    tab += 1
            items.append(string_to_data(ext_string))

            i += 1
            continue
        else:
            showerror("Error", "unexpected: " + string[i])
            return None

        name = ""
        
        while string[i] != "\n" and i < len(string):
            name += string[i]
            i += 1
        i += 1

        items.append(name)
        
    items.pop(0)
    if type(items[-1]) != list:
        items.append([])
    
    return items

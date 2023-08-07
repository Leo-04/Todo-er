from pprint import pprint

def data_to_string(items, tab=0):
        out_string = ""

        tabs = tab * "    "
        
        for i in range(0, len(items), 3):
            out_string += tabs + ("✓" if items[i] else "X") + " "
            out_string += items[i+1] + "\n"
            if len(items[i+2]):
                out_string += data_to_string(items[i+2], tab+1)

        return out_string


def nodes_to_tree(nodes, level=0):
    result = []
    for i in range(len(nodes)):
        current_node = nodes[i]
        if i + 1 < len(nodes):
            next_node  = nodes[i+1]
        else:
            next_node = [0, False, ""]

        # Edge cases
        if current_node[0] > level:
            continue
        if current_node[0] < level:
            return result

        # Recursion
        if next_node[0] == level:
            result.append([current_node[1], current_node[2], []])
        elif next_node[0] > level:
            next_result = nodes_to_tree(nodes[i+1:], level=next_node[0])
            result.append([current_node[1], current_node[2], next_result])
        else:
            result.append([current_node[1], current_node[2], []])
            return result
    return result

def string_to_data(string):
    string = string.replace("\r", "\n")
    while "\n\n" in string:
        string = string.replace("\n\n", "\n")

    lines = string.split("\n")
    i = 0
    while i < len(lines):
        if lines[i].strip() == "":
            lines.pop(i)
        else:
            i += 1

    nodes = []

    tab_size = 0
    
    line = 0
    while line < len(lines):
        i = 0
        string = lines[line]
        
        tab_size = 0
        while i < len(string) and string[i] in " \t\n":
            i += 1
            if string[i] == '\n':
                tab_size = 0
            else:
                tab_size += 1
        if i >= len(string):break
        string = string[i:]

        nodes.append([tab_size, string[0].lower() != "x", string[2:]])

        line += 1
    
    return nodes_to_tree(nodes, 0)

def printd(data, t=0):
    for d in data:
        print("   "*t, d[0], d[1])
        if d[-1]:
            printd(d[-1], t+1)
        

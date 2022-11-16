import re
def getTag(line):
    tags = re.findall(r"(?<=\")[\w\s]+(?=\s*\"\s*:)", line)
    if len(tags) == 1:
        tag = "<" + tags[0] + ">"
        return tag
    else:
        raise ValueError("Ошибка значения")

def getCloseTag(tag):
    return tag[:1] + "/" + tag[1:]


def getContains(line):

    line = re.split(r":\s*\"", line)
    lengthContains = len(line)
    if lengthContains < 2:
        if lengthContains == 1:
            if line[0].find("true") == -1 and line[0].find("null") == -1:
                try:
                    int(line[0])
                    return line[0].strip()
                except:
                    return ""
            else:
                return line[0].strip()
        else:
            return ""
    elif lengthContains > 2:
        raise ValueError("Ошибка значения")
    line = line[1]
    contains = re.findall(r'[\w\s\-:,/.()]+(?=\s*\"\s*)', line)
    if len(contains) > 0:
        contain = contains[0]
        return contain
    else:
        return ""


def parseToXML(fileJSON, fileXML):
    with open(fileJSON, encoding='utf-8') as contentJSON, open(fileXML, 'w', encoding='utf-8') as contentXML:
        contentXML.write('''<?xml version="1.0" encoding="UTF-8" ?>''' + '\n')
        indentationLevel = 0
        indent = "    "
        currentTags = []
        squareBracketFlag = False
        linesJSON = contentJSON.readlines()[1: -1]
        for line in linesJSON:
            # удаляем переносы строки
            line = line.replace("\n", "")
            if len(re.findall(r'\{', line)) > 0:
                if len(line.replace(" ", "")) > 1:
                    contain = getContains(line)
                    # обрабатываем из строки вида {"tag": "content"}
                    if len(re.findall(r':.*{.*', line)) == 0:
                        tag = getTag(line)
                        closeTag = getCloseTag(tag)
                        contentXML.write(indentationLevel * indent + tag + contain + closeTag + '\n')
                    # обрабатываем строки вида "tag"{
                    #                           }
                    else:
                        tag = getTag(line)
                        currentTags.append(tag)
                        contentXML.write(indentationLevel * indent + tag + '\n')
                        indentationLevel += 1
                else:
                    # обрабатываем еденичную {
                    tag = currentTags[indentationLevel]
                    contentXML.write(indentationLevel * indent + tag + '\n')
                    indentationLevel += 1
            # обрабатываем еденичную }
            elif len(re.findall(r'}', line)) > 0:
                indentationLevel -= 1
                closeTag = getCloseTag(currentTags[indentationLevel])
                contentXML.write(indentationLevel * indent + closeTag + '\n')
            # обрабатываем еденичную ]
            elif len(re.findall(r']', line)) > 0:
                squareBracketFlag = False
            # обрабатываем строки вида "tag"[
            #                           "content1",
            #                           "content1"
            #                      ]
            elif squareBracketFlag and len(re.findall(r':', line)) == 0:
                tag = currentTags[indentationLevel]
                contain = getContains(line)
                closeTag = getCloseTag(tag)
                contentXML.write((indentationLevel + 1) * indent + tag + contain + closeTag + '\n')
            else:
                contain = getContains(line)
                # обрабатываем строки вида "tag": "content"
                if contain != '':
                    tag = getTag(line)
                    closeTag = getCloseTag(tag)
                    contentXML.write(indentationLevel * indent + tag + contain + closeTag + '\n')
                # обрабатываем строки вида "tag"[
                else:
                    if len(re.findall(r'\[', line)) > 0:
                        tag = getTag(line)
                        currentTags.append(tag)
                        squareBracketFlag = True
parseToXML('scheduleJSON.json', 'regexScheduleXML.xml')
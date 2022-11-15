# получаем открывающий тег
def getTag(line):
    searchLine = line[line.find('"') + 1:]
    tag = "<" + searchLine[:searchLine.find('"')] + ">"
    return tag


# получаем закрывающий тег
def getCloseTag(tag):
    return tag[:1] + "/" + tag[1:]


# получаем содержимое
def getContains(line):
    searchLine = line[line.find(':') + 1:]
    searchLine = searchLine[searchLine.find('"') + 1:]
    pos = searchLine.find('"')
    if pos != -1:
        return searchLine[:pos]
    else:
        return ""


def parseToXML(fileJSON, fileXML):
    with open(fileJSON, encoding='utf-8') as contentJSON, open(fileXML, 'w', encoding='utf-8') as contentXML:
        contentXML.write('''<?xml version="1.0" encoding="UTF-8" ?>''' + '\n')
        indentationLevel = 0
        indent = "    "
        currentTags = []
        squareBracketFlag = False
        linesJSON = contentJSON.readlines()
        if linesJSON.pop(0).find('{') == - 1 or linesJSON.pop(-1).find('}') == - 1:
            raise ValueError("Ошибка значения")
        for line in linesJSON:
            # удаляем переносы строки
            line = line.replace("\n", "")
            if line.find('{') != -1:
                if len(line.replace(" ", "")) > 1:
                    contain = getContains(line)
                    # из строки вида {"tag": "content"} формируем <tag>content</tag>
                    if line[line.find(':'):].find('{') == -1:
                        tag = getTag(line)
                        closeTag = getCloseTag(tag)
                        contentXML.write(indentationLevel * indent + currentTags[indentationLevel] + '\n')
                        contentXML.write((indentationLevel + 1) * indent + tag + contain + closeTag + '\n')
                        contentXML.write(indentationLevel * indent + getCloseTag(currentTags[indentationLevel]) + '\n')
                    # обрабатываем строки вида "tag"{
                    #                      }
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
            elif line.find('}') != -1:
                indentationLevel -= 1
                closeTag = getCloseTag(currentTags[indentationLevel])
                contentXML.write(indentationLevel * indent + closeTag + '\n')
            # обрабатываем еденичную ]
            elif line.find(']') != -1:
                squareBracketFlag = False
            # обрабатываем строки вида "tag"[
            #                           "content1",
            #                           "content1"
            #                      ]
            elif squareBracketFlag and line.find(":") == -1:
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
                    if line.find('[') != -1:
                        tag = getTag(line)
                        currentTags.append(tag)
                        squareBracketFlag = True


def getHeader(line):
    searchLine = line[line.find('"') + 1:]
    header = searchLine[:searchLine.find('"')]
    return header +','
def getContent(line):
    searchLine = line[line.find(':') + 1:]
    searchLine = searchLine[searchLine.find('"') + 1:]
    pos = searchLine.find('"')
    if pos != -1:
        return searchLine[:pos]
    else:
        return ""

parseToXML('scheduleJSON.json', 'myScheduleXML.xml')

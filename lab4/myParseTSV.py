# получаем содержимое
def getContent(line):
    searchLine = line[line.find(':') + 1:]
    searchLine = searchLine[searchLine.find('"') + 1:]
    pos = searchLine.find('"')
    if pos != -1:
        return searchLine[:pos]
    else:
        return ""


def parseToTSV(fileJSON, fileTSV):
    with open(fileJSON, encoding='utf-8') as contentJSON, open(fileTSV, 'w', encoding='utf-8') as contentTSV:
        content = ''
        blockFlag = False
        linesJSON = contentJSON.readlines()
        if linesJSON.pop(0).find('{') == - 1 or linesJSON.pop(-1).find('}') == - 1:
            raise ValueError("Ошибка значения")
        indentLenght = len(linesJSON[0]) - len(linesJSON[0].lstrip())
        for line in linesJSON:
            # удаляем переносы строки
            line = line.replace("\n", "")
            indent = (len(line) - len(line.lstrip())) // indentLenght - 1
            # окончание ряда
            if indent == 3:
                if line.find(("}")) != -1:
                    content += "\n"
            elif indent == 5:
                # начало блока
                if line.find(("{")) != -1:
                    blockFlag = True
                # конец блока
                elif line.find(("}")) != -1:
                    blockFlag = False
                    content = content[:-2]
                    content += '\t'
            # сбор содержимого
            elif indent == 6:
                if blockFlag:
                    content += getContent(line) + '\\n'
        contentTSV.write(content)


parseToTSV('scheduleJSON.json', "scheduleTSV.tsv")

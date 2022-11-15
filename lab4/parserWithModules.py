from json2xml import json2xml
from json2xml.utils import readfromjson

def parseToXML(fileJSON, fileXML):
    data = readfromjson(fileJSON)
    with open(fileXML, 'w', encoding='utf-8') as contentXML:
        contentXML.write(json2xml.Json2xml(data).to_xml())
parseToXML('scheduleJSON.json', "modulesScheduleXML.xml")
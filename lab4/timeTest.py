import regexParser, parserWithModules, myParser
import time
curTime = time.time()
for i in range(100):
    myParser.parseToXML('scheduleJSON.json', 'myScheduleXML.xml')
workTime = time.time() - curTime
print("res for program with no modules and regexps =", workTime)
time.sleep(1)
curTime = time.time()
for i in range(100):
    parserWithModules.parseToXML('scheduleJSON.json', "modulesScheduleXML.xml")
workTime = time.time() - curTime
print("res for program with modules =", workTime)
time.sleep(1)
curTime = time.time()
for i in range(100):
    regexParser.parseToXML('scheduleJSON.json', 'regexScheduleXML.xml')
workTime = time.time() - curTime
print("res for program with regexps =", workTime)

import datetime as dt
import time

def readFile(path):
    with open(path, 'rt', encoding='utf-8-sig') as f:
        return f.read()

def writeFile(path, contents):
    with open(path, 'wt', encoding='utf-8-sig') as f:
        f.write(contents)

# each row is a semicolon-separated list of each illust's tags. The first element is the illust id
def generateTagFile(api, userId, dest, earlyId=None, lateId=None, delay=1, illustType="illust"):
    result = []
    offset = 0

    while True:
        print("calling user_illusts with offset " + str(offset) + "...", end="")
        json_result = api.user_illusts(userId, offset=offset, type=illustType)
        print("done")

        for illust in json_result.illusts:
            if (earlyId != None) and (illust.id < earlyId): continue
            if (lateId != None) and (illust.id > lateId):
                writeFile(dest, '\n'.join(result))
                return

            row = [str(illust.id)]
            for tag in illust.tags:
                if tag.translated_name != None: row.append(tag.translated_name)
                else: row.append(tag.name)
            result.append(';'.join(row))
        
        if len(json_result.illusts) < 30:
            break
        else:
            offset += 30
        time.sleep(delay)
    
    writeFile(dest, '\n'.join(result))

# takes a file with CSV rows and keeps the first two elements of each row
# the first two elements should be illustId,description
def generateDescriptionFile(tagFile, dest):
    result = []
    tagRows = readFile(tagFile).split('\n')
    for tagRow in tagRows:
        # ignore empty lines that make the edited tag file more readable
        if tagRow == '': continue
        elements = tagRow.split(';')
        result.append(elements[0] + ';' + elements[1])
    
    writeFile(dest, '\n'.join(result))

def parseDescriptionFile(src):
    idToDescriptionMap = {}
    rows = readFile(src).split('\n')
    for row in rows:
        (illustId, description) = row.split(';')
        idToDescriptionMap[illustId] = description
    return idToDescriptionMap

def getListOfIdsFromFile(src):
    idList = []
    rows = readFile(src).split('\n')
    for row in rows:
        illustId = row.split(';')[0]
        idList.append(int(illustId))
    return idList
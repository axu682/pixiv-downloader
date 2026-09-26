def readFile(path):
    with open(path, 'rt', encoding='utf-8-sig') as f:
        return f.read()

def writeFile(path, contents):
    with open(path, 'wt', encoding='utf-8-sig') as f:
        f.write(contents)

referenceFile = "tags, artist name, user12345678, illust, 2025.02.01"
fileToEdit = "tags, artist name, user12345678, illust, 2026.06.28, edited"

if "edited" not in fileToEdit:
    print("fileToEdit should have \"edited\" in its name")
    assert(False)

def removeImageIdsFromFile(referenceFile, fileToEdit):
    outputLines = []

    imageIdsInReferenceFiles = []
    for line in readFile(referenceFile).split('\n'):
        imageIdsInReferenceFiles.append(line.split(';')[0])
    
    for line in readFile(fileToEdit).split('\n'):
        if line.split(';')[0] not in imageIdsInReferenceFiles:
            outputLines.append(line)
    
    writeFile(fileToEdit, '\n'.join(outputLines))

removeImageIdsFromFile(referenceFile + '.txt', fileToEdit + '.txt')


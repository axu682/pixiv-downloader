import os

def setDescriptions(folder, description, illustIds=None, pages=None):
    successes = 0
    failures = []

    for file in os.listdir(folder):
        filepath = folder + '/' + file
        if os.path.isdir(filepath): continue

        tokens = file.split(', ')
        artist = tokens[0]
        date = tokens[1]
        if (len(tokens) == 3): # file does not have an existing description
            (imageId, extension) = tokens[2].split('.')
        else:
            imageId = tokens[2]
            extension = tokens[-1].split('.')[-1]

        illustId = int(imageId.split('_')[0])
        page = int(imageId.split('p')[-1])
        
        if (illustIds==None or illustId in illustIds) and (pages==None or page in pages):
            if description=='' or description==None:
                newName = folder + '/' + artist + ', ' + date + ', ' + imageId + '.' + extension
            newName = folder + '/' + artist + ', ' + date + ', ' + imageId + ', ' + description + '.' + extension
            if os.path.exists(newName):
                print("cannot rename " + filepath + " to " + newName + ". File with that name already exists.")
                failures.append(file)
            else:
                os.rename(filepath, newName)
                successes += 1
    print("total of " + str(successes) + " successes")
    return failures

def setArtistName(folder, artistName, illustIds=None, pages=None):
    successes = 0
    failures = []

    for file in os.listdir(folder):
        filepath = folder + '/' + file
        if os.path.isdir(filepath): continue

        indexOfFirstComma = file.index(',')
        restOfFile = file[indexOfFirstComma:]

        tokens = file.split(', ')
        if (len(tokens) == 3): # file does not have an existing description
            imageId = tokens[2].split('.')[0]
        else:
            imageId = tokens[2]

        illustId = int(imageId.split('_')[0])
        page = int(imageId.split('p')[-1])
        
        if (illustIds==None or illustId in illustIds) and (pages==None or page in pages):
            newName = folder + '/' + artistName + restOfFile
            if os.path.exists(newName):
                print("cannot rename " + filepath + " to " + newName + ". File with that name already exists.")
                failures.append(file)
            else:
                os.rename(filepath, newName)
                successes += 1
    print("total of " + str(successes) + " successes")
    return failures

def interval(a,b):
    return list(range(a,b+1))

failures = setDescriptions('artist name, user12345678/2022.09.04 large post', 'Mallow (Pokemon)', None, interval(110,133))
# failures = setArtistName('test download', 'userwhack', None, [2,3])

print("total of " + str(len(failures)) + " failure(s):")
for failure in failures:
    print("\t" + failure)

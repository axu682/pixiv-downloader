from pixivpy3 import AppPixivAPI
import datetime as dt
import time
import tagFileGenerator

def readFile(path):
    with open(path, 'rt', encoding='utf-8-sig') as f:
        return f.read()

def writeFile(path, contents):
    with open(path, 'wt', encoding='utf-8-sig') as f:
        f.write(contents)

def isSingleImage(illust):
    if (illust.meta_single_page != {}) and (illust.meta_pages == []): return True
    if (illust.meta_single_page == {}) and (illust.meta_pages != []): return False

    if type(illust.id) != int: 
        raise Exception("illust has no id")
    raise Exception("unclear whether illust with id " + str(illust.id) + " is a single or multi-image post")

def constructFileName(savePath, artist, date, url, description):
    idWithExtension = url.split('/')[-1]
    (imageId, extension) = idWithExtension.split('.')
    if description=='' or description==None:
        return savePath + '/' + artist + ', ' + date + ', ' + imageId + '.' + extension
    return savePath + '/' + artist + ', ' + date + ', ' + imageId + ', ' + description + '.' + extension

def downloadIllust(illust, api, savePath, artist=None, description=None, quality="original", delay=1):
    if artist==None:
        artist = 'user' + str(illust.user.id)
    artistDatetime = dt.datetime.fromisoformat(illust.create_date)
    utcDatetime = artistDatetime.astimezone(dt.timezone.utc)
    utcDate = utcDatetime.strftime("%Y.%m.%d")

    isSingle = isSingleImage(illust)
    if isSingle:
        if quality=="original":
            url = illust.meta_single_page.original_image_url
        elif quality=="master":
            url = illust.meta_single_page.original_image_url
            url = url.replace("original", "master")
            tokens = url.split('.')
            url = '.'.join(tokens[:-1]) + "_master1200.jpg"
        else:
            url = illust.image_urls[quality]
        fileName = constructFileName(savePath, artist, utcDate, url, description)
        api.download(url, name=fileName)
        time.sleep(delay)
    else:
        for i in range(illust.page_count):
            if quality=="master":
                url = illust.meta_pages[i].image_urls["original"]
                url = url.replace("original", "master")
                tokens = url.split('.')
                url = '.'.join(tokens[:-1]) + "_master1200.jpg"
            else:
                url = illust.meta_pages[i].image_urls[quality]
            fileName = constructFileName(savePath, artist, utcDate, url, description)
            print("\n\tdownloading " + str(i) + " of " + str(illust.page_count) + "...", end='')
            api.download(url, name=fileName)
            print("done", end='')
            time.sleep(delay)

def downloadFromUserFilter(api, userId, savePath, filter, descriptionFile=None, artistName=None, quality="original", delay=1, earlyTermination=False, initialOffset=0, illustType="illust"):
    offset = initialOffset
    downloadedSoFar = False

    while True:
        print("calling user_illusts with offset " + str(offset) + "...", end="")
        json_result = api.user_illusts(userId, offset=offset, type=illustType)
        print("done\n")

        descriptions = None
        illustsWithDescriptions = set()
        if descriptionFile != None:
            descriptions = tagFileGenerator.parseDescriptionFile(descriptionFile)
            illustsWithDescriptions = descriptions.keys()
        
        for illust in json_result.illusts:
            if filter(illust):
                description = None
                if str(illust.id) in illustsWithDescriptions:
                    description = descriptions[str(illust.id)]
                
                print("downloading illust " + str(illust.id) + "...", end='')
                downloadIllust(illust, api, savePath, artistName, description, quality, delay)
                downloadedSoFar = True
                print("DONE")
            elif earlyTermination and downloadedSoFar:
                # used when all images you want to download will be consecutive in the json_result
                return 

        if len(json_result.illusts) < 30:
            break
        else:
            offset += 30
        time.sleep(delay)

def downloadFromUserDateRange(api, userId, savePath, descriptionFile=None, artistName=None, earlyDatetime=None, lateDatetime=None, quality="original", delay=1, initialOffset=0, illustType="illust"):
    def filter(illust):
        illustDatetime = dt.datetime.fromisoformat(illust.create_date)
        if (earlyDatetime != None) and (illustDatetime < earlyDatetime): return False
        if (lateDatetime != None) and (illustDatetime > lateDatetime): return False
        return True
    downloadFromUserFilter(api, userId, savePath, filter, descriptionFile=descriptionFile, artistName=artistName, quality=quality, delay=delay, earlyTermination=True, initialOffset=initialOffset, illustType=illustType)

def downloadFromUserIdRange(api, userId, savePath, descriptionFile=None, artistName=None, earlyId=None, lateId=None, quality="original", delay=1, initialOffset=0, illustType="illust"):
    def filter(illust):
        if (earlyId != None) and (illust.id < earlyId): return False
        if (lateId != None) and (illust.id > lateId): return False
        return True
    downloadFromUserFilter(api, userId, savePath, filter, descriptionFile=descriptionFile, artistName=artistName, quality=quality, delay=delay, earlyTermination=True, initialOffset=initialOffset, illustType=illustType)

def downloadFromUserIllustList(api, userId, savePath, descriptionFile=None, artistName=None, illustIds=[], quality="original", delay=1, initialOffset=0, illustType="illust"):
    def filter(illust):
        return illust.id in illustIds
    downloadFromUserFilter(api, userId, savePath, filter, descriptionFile=descriptionFile, artistName=artistName, quality=quality, delay=delay, initialOffset=initialOffset, illustType=illustType)

# useful for massive downloads since pixiv might close the connection
def downloadFromUserIllustListIdRange(api, userId, savePath, descriptionFile=None, artistName=None, illustIds=[], quality="original", delay=1, initialOffset=0, illustType="illust", earlyId=None, lateId=None):
    def filter(illust):
        if (earlyId != None) and (illust.id < earlyId): return False
        if (lateId != None) and (illust.id > lateId): return False
        return illust.id in illustIds
    downloadFromUserFilter(api, userId, savePath, filter, descriptionFile=descriptionFile, artistName=artistName, quality=quality, delay=delay, initialOffset=initialOffset, illustType=illustType)


access_token = readFile('tokens/access_token.txt')
refresh_token = readFile('tokens/refresh_token.txt')

api = AppPixivAPI()
# api.set_auth(access_token, refresh_token)
api.auth(refresh_token=refresh_token)

userId = 12345678
artistName = "artist name"
fileTimestamp = "2026.06.28"

# must be illust or manga
illustType = "illust"
downloadFolder = artistName + ', ' + str(userId)

# should be original, master, larger, medium, square_medium
# master refers to the display size in pixiv when you are viewing the post but haven't zoomed in on the image
# I had to inspect element to figure out what the "master" url looks like because it isn't returned in the json_results. It is always a jpg, even if the original image is a png
quality = "original"
qualityText = "" if (quality == "original") else (", " + quality)

# json_result = api.user_illusts(userId, offset=57)
# print(json_result)

tagFile = "tags, " + artistName + ", user" + str(userId) + ", " + illustType + ", " + fileTimestamp + ".txt"
tagFileEdited = "tags, " + artistName + ", user" + str(userId) + ", " + illustType + qualityText + ", " + fileTimestamp + ", edited" + ".txt"
descriptionFile = 'descriptions, ' + artistName + ', user' + str(userId) + ", " + illustType + qualityText + ", " + fileTimestamp + '.txt'

# tagFileGenerator.generateTagFile(api, userId, tagFile, illustType=illustType)

# tagFileGenerator.generateDescriptionFile(tagFileEdited, descriptionFile)

downloadFromUserIllustListIdRange(
    api,
    userId,
    downloadFolder,
    descriptionFile=descriptionFile,
    artistName=artistName,
    illustIds = tagFileGenerator.getListOfIdsFromFile(descriptionFile),
    quality=quality,
    delay=2,
    initialOffset=0,
    illustType=illustType,
    earlyId=None,
    lateId=None
)
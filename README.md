# pixiv-downloader
downloads a given user's pixiv images and manga

pixiv_auth.py is obtained from
https://gist.github.com/ZipFile/c9ebedb224406f4f11845ab700124362#file-pixiv_auth-py
This is how to get the access token and refresh token

pixivpy3 is used for downloading. Documentation can be found here: https://pypi.org/project/pixivpy3/

Currently, the process for downloading large amounts of pics should be:
1. determine the userId of the artist and date range
2. call generateTagFile
3. copy the tag file, and add ', edited' to the file name.
  If you intend to download the pics at any resolution besides original, you neext to append this size to the editedTag file along with a comma
4. modify the tag file so that the second semicolon-separated entry in each row is a short description (like a character name) associated with the image
  (a limitation here is that different images within the same post (illust) must have the same description)
  (you only have to modify the rows that you plan on downloading)
  If you want it to look cleaner, you can delete rows corresponding to files you don't want, and then use downloadFromUserIllustList eventually
  A fileTimestamp in the file names. This represents the day the tag data was fetched and the tag file was generated. This is useful in the future if you want to update the pics downloaded in to include recent posts
5. call generateDescriptionFile on the tag file to clean everything besides the first two elements of each row
  (you can call generateDescriptionFile multiple times as you gradually update generateTagFile)
  (you can also generate this file once and then edit it directly instead of editing the tag file and then editing this)
6. pass the description file into downloadFromUserDateRange (or downloadFromUserIdRange or downloadFromUserIllustList)
  If you want to only download one image, you can use the IdRange and have the earlyId and lateId be identical
7. If you are run this script on one date and then run it at a later date to get recent images
  (or because you changed the location, changing which posts are visible to you)
  Then you can use the old tag file(s) on the new tag (edited) file to exclude any image ids found in previous tag files
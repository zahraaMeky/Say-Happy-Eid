import os
import random
import string
import cv2
from django.http import HttpResponse
from rest_framework.decorators import api_view
from project.settings import BASE_DIR
from . models import *
from datetime import datetime
import arabic_reshaper
from bidi.algorithm import get_display
from PIL import Image, ImageFont, ImageDraw

""" Generate random string consist of numbers and charachters
and use this string to rename the  new image
to ensure that there will no duplication in images name 
No two  image have the same name   """


def get_random_string():
    # choose from all lowercase letter
    letters = string.ascii_letters + string.digits
    result_str = ''.join(random.choice(letters) for i in range(14))
    # print("Random string ", result_str)
    return result_str


""" this is function recieve random string consist of numbers and charachters
from ef get_random_string() """


@api_view(['POST'])
def write_Name_Image(request):
    # getting random string consist of numbers and charachters by call get_random_string function
    randomCode = get_random_string()
    print('randomCode', randomCode)
    # store path of project in variable
    basePath = str(BASE_DIR)
    print('basePath', basePath)
    # get the path of the original image before write on it
    originalImagePath = basePath + '\static\Original\originalImage.jpg'
    print('originalImagePath', originalImagePath)
   # this path of the new image generated after write on it
   # the new image will save here
    NewImagePath = basePath + '\media\\'
    if request.method == 'POST':
        # get arabic Name from user
        arname = request.data['ArName']
        # force app write arabic characters by using arabic_reshaper & bidi.algorithm Libraries
        # use pip to istall both of them
        # Reconstruct Arabic sentences to be used in applications that don't support Arabic script
        # recieve (path) arabic name to library
        reshaped_text = arabic_reshaper.reshape(arname)
        # Bi-directional (BiDi) layout implementation in pure python
        # support rtl and ltr languages
        bidi_text = get_display(reshaped_text)  # path reshap text to library
        # get path of Sahel.ttf font that support arabic
        # arabic name will witten with this is font
        arabicFontPath = basePath + '\static\\fonts\sahel.ttf'
        print('arabicFontPath', arabicFontPath)
        # The ImageFont module in PIL library and it take
        # two parameter the path of font we use and the size of font
        ARfont = ImageFont.truetype(arabicFontPath, size=39)
        # recieve English name from user
        enname = request.data['EnName']
        # get path of Helvetica.ttf font that support English
        # English name will witten with this is font
        EnglishFontPath = basePath + '\static\\fonts\Helvetica.ttf'
        """ # The ImageFont module in PIL library and it take 
        # two parameter the path of font we use and the size of font
        This function loads a font object from the given file, 
        and creates a font object for a font of the given size. """
        ENfont = ImageFont.truetype(EnglishFontPath, size=39)
        print('arname', arname, 'enname', enname)
        # Rename image after generate
        RenameImage = "happyEid" + randomCode + ".jpg"
        # read Image by pillow pi library
        ReadImage = Image.open(originalImagePath)
        # image cordinate
        (x, y) = ReadImage.size
        print(x, y)
        """ this module to create new images, annotate or 
        retouch existing images, and to generate graphics on the fly for web use """
        # take the image anfter read it to be ready to draw on it
        drawImage = ImageDraw.Draw(ReadImage)
        # Draws  string at the given position
        """ it takes Parameters
        xy  Top left corner of the text.
        text  Text to be drawn. If it contains any newline characters, the text is passed on to multiline_text()
        fill  Color to use for the text.
        font  An ImageFont instance.
        spacing  If the text is passed on to multiline_text(), the number of pixels between lines.
        align  If the text is passed on to multiline_text(), “left”, “center” or “right”. """
        # write arabic name
        drawImage.text(
            (410, 1100), bidi_text, font=ARfont, fill=(3, 94, 147), spacing=10, align="right")
        # write English name
        drawImage.text(
            (410, 1160), enname, font=ENfont, fill=(3, 94, 147), spacing=10, align="left")
        # save the new image Image in media path with the new name
        ReadImage.save(NewImagePath+RenameImage)
        # the  path which will send to react app
        sendImagePath = '/media/' + RenameImage
        print('finalImagePath', sendImagePath)
        # Save path of new image and creation date time  in User Table (database)
        Store_in_SaveImagePath = models.SaveImagePath(
            path=sendImagePath, saveDate=datetime.now())
        Store_in_SaveImagePath.save()
        # call function
        sweepImages()
    # send path to react app to display it to user
    return HttpResponse(sendImagePath)


""" this is function fetch datetime of today and calculate the difference 
between this date and the creation date if the image complete one hour delete it 
from media  folder and database """


def sweepImages():
    # fetch date time today
    now = datetime.now()
    print('now', now, type(now))
    # fetch all data from database
    findimages = SaveImagePath.objects.all()
    # loop on fetched data to fetch creation datetime  of
    # each image to compare if image complete one hour or not
    for img in findimages:
        imageID = img.ID
        imageTimeSave = img.saveDate
        imagepath = img.path
        print('imagpath', imagepath)
        print('imagTimeSave', imageTimeSave, type(imageTimeSave))
        # subtract today datetime from image creation date
        duration = now - imageTimeSave
        print('duration', duration)
        # calculate how many days in duration
        days = duration.days
        # calculate how many days in seconds
        seconds = duration.seconds
        print('seconds', seconds)
        # calculate hours
        hours = days * 24 + seconds // 3600
        print('hours', hours)
        # if image complete one hour from creation datetime delete it
        if hours > 1:
            try:
                # delete from database
                getImageID = models.SaveImagePath.objects.get(ID=imageID)
                getImageID.delete()
                # delete from media folder
                # note the path of image fetched from database
                # os.remove must take path
                os.remove(imagepath)
            except:
                pass

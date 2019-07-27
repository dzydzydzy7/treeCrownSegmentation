from PIL import Image
from PIL.ExifTags import TAGS
 
def get_exif_data(fname):
    """Get embedded EXIF data from image file."""
    ret = {}
    try:
        img = Image.open(fname)
        if hasattr( img, '_getexif' ):
            exifinfo = img._getexif()
            if exifinfo != None:
                for tag, value in exifinfo.items():
                    decoded = TAGS.get(tag, tag)
                    ret[decoded] = value
    except IOError:
        print 'IOERROR ' + fname
    return ret
 
if __name__ == '__main__':
    str1 = 'E:/kejian/dy/data/UAV PHOTO/DJI_0'
    num = 323
    str2 = '.JPG'
    #fileName = 'E:/kejian/dy/data/UAV PHOTO/DJI_0323.JPG'
    file=open('out.txt','w+')
    for num in range(323, 843):
        fileName = str1 + str(num) + str2
        Tn = 'DJI_0' + str(num) + str2
        exif = get_exif_data(fileName)
        j1 = exif.values()[7].values()[2][0][0]
        j2 = exif.values()[7].values()[2][1][0]
        j3 = exif.values()[7].values()[2][2][0]/10000.0
        j4 = exif.values()[7].values()[2][2][1]
        w1 = exif.values()[7].values()[4][0][0]
        w2 = exif.values()[7].values()[4][1][0]
        w3 = exif.values()[7].values()[4][2][0]/10000.0
        w4 = exif.values()[7].values()[4][2][1]
        g1 = exif.values()[7].values()[6][0]/1000.0
        g2 = exif.values()[7].values()[6][1]
        print >> file , Tn + "\t" + str(j1) + "#" + str(j2) +  "\'" + str(j3) + str(j4) + "\"\t" + str(w1) + "#" + str(w2) +  "\'" + str(w3) + str(w4) + "\"\t" + str(g1) + str(g2)


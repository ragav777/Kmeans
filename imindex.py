_author__ = 'rrajago1'
from PIL import Image
import random
import sys
import os

#uses a lot of python list comprehension

def preprocess(imname,numpalette) :
    centroid_initial = []
    imarray= []
    im = Image.open(imname)
    imsize = im.size
    imarray = list(im.getdata())
    m = len(imarray)
    print(m)
    centroid_initial= [imarray[random.randint(0,m-1)] for p in range(numpalette)]
    print(len(centroid_initial))
    return imarray,imsize, centroid_initial

#This function returns an index with centroid index for every pixel
def createindex(imarray,centroid) :
    return [ minindex([(cost(i,j)) for i in centroid]) for j in imarray ]

#Given an index list and an image this function calculates the new centroid
def createcentroid(imarray, index,numpalette) :
    return [avgpixels([ imarray[i] for i,j in enumerate(index) if j ==k ]) for k in range(numpalette)]
    ##>>> [  [ a[i] for i,j in enumerate(b) if j ==k ] for k in range(3) ]
    ##[[(1, 2, 3), (4, 5, 6)], [], [(7, 8, 9), (10, 11, 12)]]

def avgpixels(tuplelist) :
    if not tuplelist :
        return tuple([ random.randint(0, 255) for i in range(3)])
    else :
        return tuple([round(sum([i[j] for i in tuplelist])/len(tuplelist)) for j in range(3) ])

#Calculates the distance between a pixel and a centroid
def cost(rgbtuple, centroidtuple):
    return sum([ (rgbtuple[p]-centroidtuple[p])**2 for p in range(len(rgbtuple)) ])

#Calculates the index of the minimum value from a list
def minindex(mylist) :
    mymin = min(mylist)
    ilist = [ i for i,j in enumerate(mylist) if j == mymin ] #returns the list of indices containing the minimums
    return ilist[0]

def createimage(tmpindex, tmpcentroid, size, n) :
    tmpimarray = []
    imname = os.path.join('C:\\Users\\rrajago1\\Desktop\\temp\\imgindex', "index_"+ str(n) + ".bmp")
    #imname =  os.path.join('C:\\Users\\ragav777\\Desktop\\imgindex_dump', "index_"+ str(n) + ".bmp")
    tmpimarray = [ tmpcentroid[i] for i in tmpindex]
    imgtemp = Image.new('RGB', size)
    imgtemp.putdata(tmpimarray)
    imgtemp.save(imname)
    return

def main() :
    #imname = os.path.join('C:\\Users\\ragav777\\Desktop\\imgindex_dump', 'baboon_face.bmp')
    imname = os.path.join('C:\\Users\\rrajago1\\Desktop\\temp\\imgindex', 'tiffany.bmp')
    numpalette = 4
    numiter = 25
    index = []
    imarray = []
    centroid_initial = []
    tmpcentroid = []
    tmpimarray = []
    imarray, imsize, centroid_initial = preprocess(imname,numpalette)
    for i in range(numiter) :
        print( "starting iteration " + str(i) + "...")
        if i == 0 :
            tmpindex = createindex(imarray,centroid_initial)
        else :
            tmpindex = createindex(imarray,tmpcentroid)
        tmpcentroid = createcentroid(imarray, tmpindex,numpalette)
        createimage(tmpindex, tmpcentroid, imsize, i)


if __name__ == '__main__' :
    main()
else :
    print ("Didn't Work")

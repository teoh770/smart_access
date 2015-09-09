import  sys
from string import split
from os.path import basename
from smart_access import eigenfaces


class PyFaces:
    def face_recognition(self,thrsh,imgsdir,egfnum, testimg):
        self.testimg=testimg
        self.imgsdir=imgsdir
        self.threshold=thrsh
        self.egfnum=egfnum
        parts = split(basename(self.testimg),'.')
        extn=parts[len(parts) - 1]
        print "to match:",self.testimg," to all ",extn," images in directory:",imgsdir
        self.facet= eigenfaces.FaceRec()

        self.egfnum=self.set_selected_eigenfaces_count(self.egfnum,extn)
        print "number of eigenfaces used:",self.egfnum
        #to check for the cache file
        #if the cache file is not exists or not the latest one
        #system will train the new cache
        self.facet.checkCache(self.imgsdir,extn,self.imgnamelist,self.egfnum,self.threshold)
        mindist,matchfile=self.facet.findmatchingimage(self.testimg,self.egfnum,self.threshold)
        if mindist < 1e-10:
            mindist=0
        if not matchfile:
            print "NOMATCH! try higher threshold"
            return False
        else:
            print "matches :"+matchfile+" dist :"+str(mindist)
            #since the image naming is using the userId
            #it will be splitted out the userId and return the id
            return matchfile.split("/")[3].split(".")[0].split("_")[0]


    def set_selected_eigenfaces_count(self,selected_eigenfaces_count,ext):
        #call eigenfaces.parsefolder() and get imagenamelist
        self.imgnamelist=self.facet.parsefolder(self.imgsdir,ext)
        numimgs=len(self.imgnamelist)
        if(selected_eigenfaces_count >= numimgs  or selected_eigenfaces_count == 0):
            selected_eigenfaces_count=numimgs/2
        return selected_eigenfaces_count

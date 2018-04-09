import json
from pprint import pprint

import numpy as np

import os

#load file as a string

image_names = os.listdir('./images/')
image_names = [f for f in image_names if not f.startswith('.')]
image_names.sort()


for im_name in image_names:
    print "Working on: "+im_name
    annotation_name = im_name.split(".svs")[0]+".json"

    with open ("annotations/"+annotation_name, "r") as myfile:
        data=myfile.readlines()

        #clean the weird json file that HistomicsTK produces
        data = data[0].replace("&nbsp;","")
        data = data.replace("<br />","")
        data = data.replace("<div style=\"font-family:monospace;\">","")
        data = data.replace("</div>","")

        text_file = open("modified.json", "w")
        text_file.write(data)
        text_file.close()

        #load the cleaned json file
        data = json.load(open("modified.json"))

        number_annotations = data["_elementQuery"]["count"]

        for i in range(number_annotations):
            print "     Extracting patch "+str(i+1)+" of "+str(number_annotations)
            center = data["annotation"]["elements"][i]["center"]
            height = data["annotation"]["elements"][i]["height"]
            width = data["annotation"]["elements"][i]["width"]

            #perapre values for box
            v1 = int(center[0]-width/2)
            v2 = int(center[1]-height/2)
            v3 = int(width)
            v4 = int(height)

            #prepare here string to be executed
            #------------------------------------
            #explanation for the command
            #"echo yes" is for automatically overwrite the patches in case the file already exists
            #info about the bfconvert can be found https://docs.openmicroscopy.org/bio-formats/5.8.1/users/comlinetools/conversion.html
            #">/dev/null" suppress the output of bfconvert, remove this part if something is not working with bfconver and you want to understand why
            exec_string = "echo y | ./bfconvert/./bfconvert images/"+im_name+" -crop "+str(v1)+","+str(v2)+","+str(v3)+","+str(v4)+" rois/"+annotation_name+"_"+str(i)+".jpg >/dev/null"
            os.system(exec_string)

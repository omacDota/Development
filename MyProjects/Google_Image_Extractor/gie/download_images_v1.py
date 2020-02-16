# USAGE
# python download_images.py --urls urls.txt --output images/santa

# import the necessary packages
from imutils import paths
import argparse
import requests
import cv2
import os
import glob

l_url_dir = 'urls'
l_output_dir = "images"

# grab the list of URLs from the input file, then initialize the

#print(os.listdir(l_url_dir))
#print(os.listdir(l_output_dir+"/burgers"))


for file in os.listdir(l_url_dir):
    if file.endswith(".txt"):
        l_inputfile = l_url_dir+"/"+file
        rows = open(l_inputfile).read().strip().split("\n")
        # total number of images downloaded thus far for current Dir
        total = 0

        # loop the URLs      
        for url in rows:
            if(total >= 100):
                break
            try:
                # try to download the image
                r = requests.get(url, timeout=60)

                # save the image to disk
                outfile = os.path.splitext(l_output_dir+"/"+file)[0]
                
                if not os.path.exists(outfile):
                    os.makedirs(outfile) 
                p = os.path.sep.join([outfile, "{}.jpg".format(
                    str(total).zfill(8))])
                f = open(p, "wb")
                f.write(r.content)
                f.close()

                # update the counter
                print("[INFO] downloaded: {}".format(p))
                total += 1

            # handle if any exceptions are thrown during the download process
            except:
                print("[INFO] error downloading {}...skipping".format(p))

        # loop over the image paths we just downloaded
        for imagePath in paths.list_images(outfile):
            # initialize if the image should be deleted or not
            delete = False

            # try to load the image
            try:
                image = cv2.imread(imagePath)

                # if the image is `None` then we could not properly load it
                # from disk, so delete it
                if image is None:
                    print("None")
                    delete = True

            # if OpenCV cannot load the image then the image is likely
            # corrupt so we should delete it
            except:
                print("Except")
                delete = True

            # check to see if the image should be deleted
            if delete:
                print("[INFO] deleting {}".format(imagePath))
                os.remove(imagePath)
    else:
        print("File "+file+" dosent not end with .txt format")
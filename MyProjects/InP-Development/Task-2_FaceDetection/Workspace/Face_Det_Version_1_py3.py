import cv2
import sys

# Gloabls
g_path_imageSrc = 'Imagec-Face\sourceImage-Test_2.jpg'
g_path_casc = 'haarcascade_frontalface_default.xml'



def main():
    # Convert Image to Gray Scale
    l_image = cv2.imread(g_path_imageSrc)
    l_grayScale_img = cv2.cvtColor(l_image, cv2.COLOR_BGR2GRAY)


    # Get Cascade in Memory
    l_cascade_faceCascade = cv2.CascadeClassifier(g_path_casc)

    faces = l_cascade_faceCascade.detectMultiScale(l_grayScale_img, 
                                                    scaleFactor=1.1,
                                                    minNeighbors=5,
                                                    minSize=(30,30),
                                                    flags = cv2.CASCADE_SCALE_IMAGE)
                                    
    print("Found {0} faces!".format(len(faces)))
    
    for (x, y, w, h) in faces:
        cv2.rectangle(l_image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    cv2.imshow(""+g_path_imageSrc+"",l_image)
    cv2.waitKey(0)

if __name__ == '__main__':
    main()
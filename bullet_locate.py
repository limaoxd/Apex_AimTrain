import sys
import cv2
import numpy as np

class a:
    img = cv2.imread('./guns/car.png')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    rows = gray.shape[0]
    circles = cv2.HoughCircles(image=gray, 
                           method=cv2.HOUGH_GRADIENT, 
                           dp=1, 
                           minDist=2,
                           param1=3,
                           param2=3,
                           minRadius=2,
                           maxRadius=4                        
                        )

    # ensure at least some circles were found
    if circles is not None:
        circles = np.uint16(np.around(circles))
        print(len(circles[0]))
        
        for i in circles[0, :]:
            center = (i[0], i[1])
            print(center)
            # circle center
            cv2.circle(img, center, 1, (0, 255, 0), 1)
            # circle outline
            radius = i[2]
            cv2.circle(img, center, radius, (255, 255, 255), 1)

    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
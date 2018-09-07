import cv2
import datetime
#import pandas as pd
import csv
from openalpr import Alpr

def rotate_image(image):
    (h, w) = image.shape[:2]
    center = (w / 2, h / 2)

    # rotate the image by 180 degrees
    M = cv2.getRotationMatrix2D(center, 180, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h))
    #cv2.imshow("rotated", rotated)
    cv2.waitKey(0)
    return rotated


def pred_alpr(image1): #### SHould add the region

    alpr = Alpr("us", "C:\\Users\\shobeir.mazinani\\Desktop\\BasharsALPR\\OpenALPR-Python\\openalpr_64\\openalpr.conf", "C:\\Users\\shobeir.mazinani\\Desktop\\BasharsALPR\\OpenALPR-Python\\openalpr_64\\runtime_data")
    if not alpr.is_loaded():
        print("Error loading OpenALPR")
        sys.exit(1)
    else:
        print("OpenALPR was loaded correctly")

    
    alpr.set_top_n(1)
    alpr.set_default_region("ca")
    results = alpr.recognize_file(image1)
    #print(results)
    

    i = 0
    for plate in results['results']:
        i += 1
        print("Plate #%d" % i)
        print("   %12s %12s" % ("Plate", "Confidence"))
        for candidate in plate['candidates']:
            prefix = "-"
            if candidate['matches_template']:
                prefix = "*"
            #print("  %s %12s%12f" % (prefix, candidate['plate'], candidate['confidence']))

    # Call when completely done to release memory
    # alpr.unload()
    
    #print("Sleep for some time")
    #time.sleep(5)
    #print("I am done")

    return candidate['plate'], candidate['confidence']

    

    
def compare_prediction(pred1,confidence1,pred2,confidence2):
    
    if confidence1 >= confidence2:
        print("Plate: %12s%12f" % (pred1, confidence1))
        return pred1, confidence1
        
    else:
        print("Plate: %12s%12f" % (pred2, confidence2))
        return pred2, confidence2

    
def save_prediction(sql_connection,image1,pred1,confidence1,image2,pred2,confidence2,ground_truth):
    
    return None
    
def save_final_prediction():
    return None

# def recognize():
    # alpr = Alpr("us", "C:\\Users\\shobeir.mazinani\\Desktop\\BasharsALPR\\OpenALPR-Python\\openalpr_64\\openalpr.conf", "C:\\Users\\shobeir.mazinani\\Desktop\\BasharsALPR\\OpenALPR-Python\\openalpr_64\\runtime_data")
    # if not alpr.is_loaded():
        # print("Error loading OpenALPR")
        # sys.exit(1)
    # else:
        # print("OpenALPR was loaded correctly")

    
    # alpr.set_top_n(20)
    # alpr.set_default_region("md")
    # results = alpr.recognize_file("SampleImage.jpg")

    # i = 0
    # for plate in results['results']:
        # i += 1
        # print("Plate #%d" % i)
        # print("   %12s %12s" % ("Plate", "Confidence"))
        # for candidate in plate['candidates']:
            # prefix = "-"
            # if candidate['matches_template']:
                # prefix = "*"
            # print("  %s %12s%12f" % (prefix, candidate['plate'], candidate['confidence']))

    #Call when completely done to release memory
    #alpr.unload()
    
    #print("Sleep for some time")
    #time.sleep(5)
    #print("I am done")
    
    
        
    
    

# Main Function: 
def main(argv=None):  
    todaydate = str(datetime.date.today()).replace("-","")
    
    #with open(f"./{todaydate}Predictions.csv","w",newline='') as fpred:
    #    with open(f"./{todaydate}PredPlateManagement.csv","w",newline='') as f2pm: # The output to be used by plate management
            
            #fieldnames_fpred = []
            #fieldnames_fpredPM = []
            #writer_f = csv.DictWriter(fpred, fieldnames=fieldnames_fpred)
            #writer_f.writeheader()

            #writer_fPM = csv.DictWriter(f2pm, fieldnames=fieldnames_fpredPM)
            #writer_fPM.writeheader()

    print("Press the Esc key to close the program.")
    print("Press the Space key to capture the plate image.")


    cam1 = cv2.VideoCapture(1)
    #cam2 = cv2.VideoCapture(1)

    cv2.namedWindow("TNR_ALPR")

    img_counter = 0

    while True:
        ret, frame = cam1.read()

        cv2.imshow("test", frame)
        if not ret:
            break
        k = cv2.waitKey(1)

        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k%256 == 32:
            # SPACE pressed

            img_name = "{}plateID_{}.png".format(todaydate,img_counter)
            img_name_Rot = "{}RotatedplateID_{}.png".format(todaydate,img_counter)

            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            rotated_frame = rotate_image(frame)
            cv2.imwrite(img_name_Rot, rotated_frame)
            print("{} written!".format(img_name_Rot))

            img_counter += 1

            pred1,conf1 = pred_alpr(img_name)
            predRot1,confRot1 = pred_alpr(img_name_Rot)

            #pred2,conf2 = pred_alpr(frame2)
            #predRot2,confRot2 = pred_alpr(rotated_frame2)


            final_pred1, final_confidence1 = compare_prediction(pred1,conf1,predRot1,confRot1)

            #final_pred2, final_confidence2 = compare_prediction(pred2,conf2,predRot2,confRot2)

            #final_pred, final_confidence = compare_prediction(final_pred1, final_confidence1,final_pred2, final_confidence2)






    cam1.release()

    cv2.destroyAllWindows()
   
# The main function is the entrance:
if __name__ == '__main__':
    main()
























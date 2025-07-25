import cv2 as cv

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

def preprocess_image(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (25,25), 1)
    thresh = cv.adaptiveThreshold(blur, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 11, 2)
    
    contours, _ = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_TC89_KCOS)
    
    for c in contours: 
        x, y, w, h = cv.boundingRect(c)
        area = cv.contourArea(c)
        if area > 1000:  # Adjust threshold as needed
            cv.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)
            #cv.putText(thresh, "Rectangle", (x, y-10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
    
    return img

while True:
    # Capture frame-by-frame
    print("on loop")
    ret, frame = cap.read()
    if not ret: # If frame is not captured correctly, break the loop
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Preprocess the frame
    image = preprocess_image(frame)
    # Display the resulting frame
    cv.imshow('frame', image)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
 
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
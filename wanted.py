from email.mime.image import MIMEImage

import cv2
import datetime
import face_recognition
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_mail(TEXT, ImgFileName):
    img_data = open(ImgFileName, 'rb').read()
    msg = MIMEMultipart()
    msg['Subject'] = 'Python test'
    msg['From'] = "<Sender's email>"
    msg['To'] = "<Receiver's email>"
    text = MIMEText(TEXT)
    msg.attach(text)
    image = MIMEImage(img_data, name='test1.png')
    msg.attach(image)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login("<Sender's email>", "<Sender's password>")
    s.sendmail("<Sender's email>", "<Receiver's email>", msg.as_string())
    s.quit()


# ---------------------- Prepare the known faces ------------------------------

ghassen = face_recognition.load_image_file('ghassen.jpg')             # Load the image as numpy array
ghassen_face_encoding = face_recognition.face_encodings(ghassen)[0]   # Get the facial features to compare them


# Create an array of encodings
known_face_encodings = [
    ghassen_face_encoding
]

# Create an array of names
known_face_names = [
    "Ghassen Chaabouni"
]
# -----------------------------------------------------------------------

cap = cv2.VideoCapture(0)    # Open the webcam
ret, frame = cap.read()      # Read a frame

k = 500
while (cap.isOpened()):
    # Find the faces
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    k = k + 1
    # Loop through the faces
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        name = "Unknown Person"
        datet = str(datetime.datetime.now())  # Get the date

        # If there is a match
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.putText(frame, '{}'.format(name), (left, top-3), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)        # Name
            cv2.putText(frame, '{}'.format(datet), (left, top - 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)    # Time
            cv2.putText(frame, '{}'.format('WANTED'), (left, top - 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
            message = 'WANTED: ' + name + ' ' + datet
            if (k >= 7):    # Add a delay between the emails
                cv2.imwrite('WANTED.png', frame)
                send_mail(message, 'WANTED.png')    # Send a WANTED email
                k = 0

        else:  # Unknown person
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, '{}'.format('Safe'), (left, top-3), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)    # Unknown
            cv2.putText(frame, '{}'.format(datet), (left, top - 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)  # Time

    cv2.imshow("inter", frame)    # Show the camera
    ret, frame = cap.read()       # Read the next frame

    if (cv2.waitKey(40) == 27):   # Press 'ESC' to exit the camera
        break


cv2.destroyAllWindows()
cap.release()


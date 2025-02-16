import cv2
import csv
from cvzone.HandTrackingModule import HandDetector
import cvzone
import time
import streamlit as st

# Setup Streamlit and webcam
st.write('<span class="heading2 quiz-heading">Cyber Quiz 📝</span>',
         unsafe_allow_html=True)
st.write('<span class="smaller-text">Ready to ace your cybersecurity knowledge? Answer questions with your hands in our interactive, hand-detecting quiz!</span>', unsafe_allow_html=True)

# Setup video capture
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Initialize the hand detector
detector = HandDetector(detectionCon=0.8)

# Define MCQ class


class MCQ:
    def __init__(self, data):
        self.question = data[0]
        self.choice1 = data[1]
        self.choice2 = data[2]
        self.choice3 = data[3]
        self.choice4 = data[4]
        self.answer = int(data[5])
        self.userAns = None

    def update(self, cursor, bboxs):
        for x, bbox in enumerate(bboxs):
            x1, y1, x2, y2 = bbox
            if x1 < cursor[0] < x2 and y1 < cursor[1] < y2:
                self.userAns = x + 1
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), cv2.FILLED)


# Import CSV file data for MCQs
pathCSV = "Mcqs.csv"
with open(pathCSV, newline='\n') as f:
    reader = csv.reader(f)
    dataAll = list(reader)[1:]

# Create MCQ objects
mcqList = [MCQ(q) for q in dataAll]

qNo = 0
qTotal = len(dataAll)

# Setup a Streamlit placeholder for webcam feed
frame_placeholder = st.empty()

stop_button_pressed = st.button("Stop Quiz")

# Main loop
while cap.isOpened() and not stop_button_pressed:
    success, img = cap.read()
    if not success:
        st.write("Failed to grab frame!")
        break

    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    # Display the MCQ quiz questions and choices
    if qNo < qTotal:
        mcq = mcqList[qNo]

        img, bbox = cvzone.putTextRect(
            img, mcq.question, [100, 100], 2, 2, offset=50, border=5)
        img, bbox1 = cvzone.putTextRect(
            img, mcq.choice1, [100, 250], 2, 2, offset=50, border=5)
        img, bbox2 = cvzone.putTextRect(
            img, mcq.choice2, [400, 250], 2, 2, offset=50, border=5)
        img, bbox3 = cvzone.putTextRect(
            img, mcq.choice3, [100, 400], 2, 2, offset=50, border=5)
        img, bbox4 = cvzone.putTextRect(
            img, mcq.choice4, [400, 400], 2, 2, offset=50, border=5)

        if hands:
            lmList = hands[0]['lmList']
            cursor = lmList[8]
            length, _, img = detector.findDistance(
                lmList[8][0:2], lmList[12][0:2], img)
            print(length)

            if length < 35:
                mcq.update(cursor, [bbox1, bbox2, bbox3, bbox4])
                if mcq.userAns is not None:
                    time.sleep(0.3)
                    qNo += 1

    # Once all questions are answered
    else:
        score = sum(1 for mcq in mcqList if mcq.answer == mcq.userAns)
        score = round((score / qTotal) * 100, 2)
        img, _ = cvzone.putTextRect(img, "Quiz Completed", [
                                    250, 300], 2, 2, offset=50, border=5)
        img, _ = cvzone.putTextRect(img, f'Your Score: {score}%', [
                                    700, 300], 2, 2, offset=50, border=5)

    # Draw progress bar
    barValue = 150 + (950 // qTotal) * qNo
    cv2.rectangle(img, (150, 600), (barValue, 650), (0, 255, 0), cv2.FILLED)
    cv2.rectangle(img, (150, 600), (1100, 650), (255, 0, 255), 5)
    img, _ = cvzone.putTextRect(
        img, f'{round((qNo / qTotal) * 100)}%', [1130, 635], 2, 2, offset=16)

    # Convert the frame from BGR to RGB for Streamlit
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Display the webcam feed in the Streamlit app
    frame_placeholder.image(img_rgb, channels="RGB")

    # Break condition
    if stop_button_pressed:
        break

# Release resources
cap.release()
cv2.destroyAllWindows()

st.write("Quiz Stopped!")

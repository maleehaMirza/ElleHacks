import cv2
import csv
import av
import time
import streamlit as st
from cvzone.HandTrackingModule import HandDetector
import cvzone
from streamlit_webrtc import webrtc_streamer

# Streamlit UI
st.write('<span class="heading2 quiz-heading">Cyber Quiz 📝</span>',
         unsafe_allow_html=True)
st.write('<span class="smaller-text">Ready to ace your cybersecurity knowledge? Answer questions with your hands in our interactive, hand-detecting quiz!</span>', unsafe_allow_html=True)

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

# Load MCQs from CSV
pathCSV = "Mcqs.csv"
with open(pathCSV, newline='\n') as f:
    reader = csv.reader(f)
    dataAll = list(reader)[1:]

# Create MCQ objects
mcqList = [MCQ(q) for q in dataAll]
qNo = 0
qTotal = len(dataAll)

# Define a callback function to process video frames
def video_frame_callback(frame):
    global qNo

    img = frame.to_ndarray(format="bgr24")  # Convert frame to BGR
    img = cv2.flip(img, 1)  # Flip horizontally
    hands, img = detector.findHands(img, flipType=False)

    # Display the MCQ quiz questions and choices
    if qNo < qTotal:
        mcq = mcqList[qNo]

        img, bbox = cvzone.putTextRect(img, mcq.question, [100, 100], 2, 2, offset=50, border=5)
        img, bbox1 = cvzone.putTextRect(img, mcq.choice1, [100, 250], 2, 2, offset=50, border=5)
        img, bbox2 = cvzone.putTextRect(img, mcq.choice2, [400, 250], 2, 2, offset=50, border=5)
        img, bbox3 = cvzone.putTextRect(img, mcq.choice3, [100, 400], 2, 2, offset=50, border=5)
        img, bbox4 = cvzone.putTextRect(img, mcq.choice4, [400, 400], 2, 2, offset=50, border=5)

        if hands:
            lmList = hands[0]['lmList']
            cursor = lmList[8]
            length, _, img = detector.findDistance(lmList[8][0:2], lmList[12][0:2], img)

            if length < 35:
                mcq.update(cursor, [bbox1, bbox2, bbox3, bbox4])
                if mcq.userAns is not None:
                    time.sleep(0.3)
                    qNo += 1

    # Once all questions are answered
    else:
        score = sum(1 for mcq in mcqList if mcq.answer == mcq.userAns)
        score = round((score / qTotal) * 100, 2)
        img, _ = cvzone.putTextRect(img, "Quiz Completed", [250, 300], 2, 2, offset=50, border=5)
        img, _ = cvzone.putTextRect(img, f'Your Score: {score}%', [700, 300], 2, 2, offset=50, border=5)

    # Draw progress bar
    barValue = 150 + (950 // qTotal) * qNo
    cv2.rectangle(img, (150, 600), (barValue, 650), (0, 255, 0), cv2.FILLED)
    cv2.rectangle(img, (150, 600), (1100, 650), (255, 0, 255), 5)
    img, _ = cvzone.putTextRect(img, f'{round((qNo / qTotal) * 100)}%', [1130, 635], 2, 2, offset=16)

    return av.VideoFrame.from_ndarray(img, format="bgr24")  # Convert back to VideoFrame

# Start webcam stream
webrtc_streamer(
    key="quiz-stream",
    video_frame_callback=video_frame_callback,
    media_stream_constraints={"video": True, "audio": False},
)

# Stop quiz button
if st.button("Stop Quiz"):
    st.write("Quiz Stopped!")

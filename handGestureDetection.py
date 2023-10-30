import cv2
import numpy as np
import mediapipe as mp
import time
import handTrackingModule as hmt
import boto3
import sagemaker
import json
import io
import pandas as pd

def get_prediction(input_data):
    # Set your AWS region and SageMaker endpoint name

    aws_region = 'us-east-2'
    endpoint_name = 'Custom-sklearn-model-2023-10-30-17-28-33'

    # Initialize a SageMaker runtime client
    sagemaker_runtime = boto3.client('sagemaker-runtime', region_name=aws_region)

    payload = io.StringIO()
    data2 = np.array(input_data).reshape(1, -1)
    # input_data = input_data
    input_data = pd.DataFrame(data2)
    input_data.to_csv(payload, header=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20], index=None)

    try:
        # Send a request to the SageMaker endpoint for prediction
        response = sagemaker_runtime.invoke_endpoint(
            EndpointName=endpoint_name,
            ContentType='text/csv',
            Body=payload.getvalue(),
        )

        # Parse the response
        result = response['Body'].read().decode('utf-8')
        result = json.loads(result)

        # Print or use the prediction result
        print("Prediction:", result[1])
        return result[1]

    except Exception as e:
        print("Error:", e)


# Gesture Detection in Realtime
cTime = 0
pTime = 0
cap = cv2.VideoCapture(0)
detector = hmt.HandDetector()
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    className = ""
    lmList = detector.findPosition(img,draw=False)
    lmDist = []
    lmDist.append(0)
    if len(lmList) != 0:
        #Calculating the distance between points
        for i in range(1, len(lmList)):
            lmDist.append(((lmList[i][0] - lmList[0][0])**2 + (lmList[i][1] - lmList[0][1])**2)**0.5)
        # Predict gesture
        prediction = get_prediction([lmDist])

            # print(prediction)
#             classID = np.argmax(prediction)
        if prediction:
            className = prediction
#         print(lmList[4])

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, className, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
    cv2.imshow("Image", img)
    if cv2.waitKey(1) == ord('q'):
        break
# release the webcam and destroy all active windows
cap.release()
cv2.destroyAllWindows()

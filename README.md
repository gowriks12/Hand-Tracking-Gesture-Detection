# Hand Tracking and Gesture Detection
Real-time hand tracking and identifying the gesture on the frame is the goal of the project.

# Hand Tracking
Hand tracking is carried out using mediapipe open source library for hand tracking. A hand tracker module is implemented using the object oriented concept. This module has functions to track hand and return land marks of the hand. The module returns 21 points as landmarks, each landmark has information of the points' X and Y coordinate in the frame. 

![image](https://user-images.githubusercontent.com/82420256/150011948-414c8f52-e937-432d-bcc5-64abf99163ac.png)

Source: https://google.github.io/mediapipe/solutions/hands.html

Using this information, further processing is done with point 0 as the reference. With point 0 as reference, euclidean distance between point 0 and all other points are calculated. The distance data for each geature is collected. Around 30 samples for each geature is collected by running the handDetImplement.py script. This data is stored in handlandmarks.csv file. It is further used for the classification and identification.

# Classification
The data collected is first read into a dataframe and the dataframe is split into train and test datasets. 80% train data and 20% test data.The data is then classififed using two different methods, K nearest neighbours and Support Vector Machines. Since there is less data, an algorithm that performs well even with lesser data had to be picked. Among all the classifiers, decided to go with KNN and SVM as both perform well even with less data.

KNN classifier with k = 3 was used for the project as it seemed like the optimal k value in terms of size of data.
For SVM, different kernels were tested for the classification task. Linear, Radial basis function, sigmoid and polynomial. 

Linear accuracy = 1.0

RBF = 0.08333

Sigmoid = 0.08333

Polynomial = 0.979

Although linear kernel showed 100% accuracy, there is a chance of overfitting. Hence, Polynomial kernel was chones as the best of the four and used for the classification task.

KNN Classifier accuracy :0.958333

SVM(poly kernel) Classifier accuracy :0.979

The classifier models were saved into a pickle file using the pickle package. The saved models are then loaded and used with the handtracking implementation.
The predicted class/gesture is then displayed on the frame in real time.

# Future works and Improvements
1. The gesture detection/identification can be improved by including many more gestures. This project involves recognizing 8 gestures, many more gestures can be classified by collecting relevant data.
2. This project focuses on single hand gesture detection, this can be extended to multiple hand tracking project
3. KNN mis classifies "STOP" and "LIVELONG" gestures but classifies correctly if both are present at different distances from camera. This issue has to be addressed.
4. SVM mis classifies when the hand is far away from camera but classifies all gestures correctly when kept at an optimal distance from camera. This issue also has to be addressed.

# Conclusion
In conclusion, a real-time hand tracking and gesture detection project is completed. Libraries such as Mediapipe, openCv, scikit-learn, pickle and pandas were used. A comparitive study between KNN and SVM classifier for the task is carried out and it is concluded that SVM performs better than KNN for this task.

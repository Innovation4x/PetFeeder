import serial
import cv2
import numpy as np
import time


def main():
    print("Pet Detected!")
    net = cv2.dnn.readNet('yolov3.weights', 'yolov3.cfg')
    classes = []
    with open('coco.names.txt', 'r') as f:
        classes = f.read().splitlines()

    cap = cv2.VideoCapture(0)

    while True:
        initial_time = time.time()
        final_val = "No pet Reconginzed!! Turn off camera"
        pet = "OFF"

        while True:
            final_time = time.time()
            time_diff = final_time - initial_time

            _, img = cap.read()
            height, width, _ = img.shape

            blob = cv2.dnn.blobFromImage(img, 1 / 255, (416, 416), (0, 0, 0), swapRB=True, crop=False)
            net.setInput(blob)

            output_layers_names = net.getUnconnectedOutLayersNames()
            layerOutputs = net.forward(output_layers_names)

            val = "No"
            boxes = []
            confidences = []
            class_ids = []

            for output in layerOutputs:
                for detection in output:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]

                    if confidence > 0.8:
                        center_x = int(detection[0] * width)
                        center_y = int(detection[0] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)

                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)

                        boxes.append([x, y, w, h])
                        confidences.append((float(confidence)))
                        class_ids.append(class_id)
                        if 15 in class_ids:
                            val = "Yes"
                            final_val = "Pet Recognized !!"
                            pet = "Cat"
                        elif 16 in class_ids:
                            val = "Yes"
                            final_val = "Pet Recognized !!"
                            pet = "Dog"

                    print("Pet Recongnized : ", val)

            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
            font = cv2.FONT_HERSHEY_PLAIN
            colors = np.random.uniform(0, 255, size=(len(boxes), 3))

            for i in indexes:
                if class_ids[i] == 15:
                    x, y, w, h = boxes[i]
                    label = str(classes[class_ids[i]])
                    confidence = str(round(confidences[i], 2))
                    color = colors[i]
                    cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(img, label + " " + confidence, (x, y + 20), font, 2, (255, 255, 255), 2)
                elif class_ids[i] == 16:
                    x, y, w, h = boxes[i]
                    label = str(classes[class_ids[i]])
                    confidence = str(round(confidences[i], 2))
                    color = colors[i]
                    cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(img, label + " " + confidence, (x, y + 20), font, 2, (255, 255, 255), 2)

            # show the detected output in a window
            cv2.imshow('Pet Detection', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            def arduino_write(x):
                arduino.write(bytes(x, 'utf-8'))
                data = arduino.readline()
                return data


            # print the observation details of the last time interval
            if time_diff > 10:
                arduino_write(str(pet))
                print("\nPet recognized: ", final_val)
                print(pet)
                time.sleep(10)
                if pet == "OFF":
                    cap.release()
                    cv2.destroyAllWindows()
                    return None
                break



# execution
while True:
    arduino = serial.Serial(port="COM12", baudrate="115200", timeout=.1)
    line = arduino.readline()
    response = line.decode()

    print("pet", response)
    if response == 'detected':
        main()
    arduino.close()
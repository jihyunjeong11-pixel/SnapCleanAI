from ultralytics import YOLO

model = YOLO("yolov8n.pt")

def analyze_image(image_path):

    results = model(image_path)

    person_count = 0
    objects = []

    for result in results:

        for box in result.boxes:

            cls = int(box.cls[0])

            name = model.names[cls]

            objects.append(name)

            if name == "person":

                person_count += 1

    return person_count, objects
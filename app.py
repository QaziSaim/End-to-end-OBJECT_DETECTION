import streamlit as st
from ultralytics import YOLO
import cv2
import numpy as np
import tempfile
import json

# -------------------------
# Load Model
# -------------------------
@st.cache_resource
def load_model():
    return YOLO("yolov8s.pt")  # or your trained model

model = load_model()

st.title("🚗 Traffic Object Detection System")

# -------------------------
# Mode Selection
# -------------------------
option = st.radio("Choose Input Type:", ["Upload Image", "Real-Time Camera"])

# -------------------------
# IMAGE UPLOAD MODE
# -------------------------
if option == "Upload Image":
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        image = np.array(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(image, 1)

        st.image(image, caption="Uploaded Image", use_container_width=True)

        if st.button("Detect Objects"):
            results = model(image, conf=0.25)

            output = []
            result = results[0]

            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cls = int(box.cls[0])
                conf = float(box.conf[0])

                label = model.names[cls]

                output.append({
                    "label": label,
                    "confidence": round(conf, 2),
                    "bbox": [x1, y1, x2, y2]
                })

            # Draw bounding boxes
            plotted = result.plot()
            plotted = cv2.cvtColor(plotted, cv2.COLOR_BGR2RGB)

            st.image(plotted, caption="Detection Result", use_container_width=True)

            # Show JSON
            st.subheader("📄 JSON Output")
            st.json(output)

# -------------------------
# REAL-TIME CAMERA MODE
# -------------------------
elif option == "Real-Time Camera":
    st.warning("Click START to begin camera")

    run = st.checkbox("Start Camera")

    FRAME_WINDOW = st.image([])

    cap = cv2.VideoCapture(0)

    while run:
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to access camera")
            break

        results = model(frame, conf=0.25)
        result = results[0]

        output = []

        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cls = int(box.cls[0])
            conf = float(box.conf[0])

            label = model.names[cls]

            output.append({
                "label": label,
                "confidence": round(conf, 2),
                "bbox": [x1, y1, x2, y2]
            })

        # Draw boxes
        frame = result.plot()

        FRAME_WINDOW.image(frame, channels="BGR")

        # Show JSON live
        st.json(output)

    cap.release()
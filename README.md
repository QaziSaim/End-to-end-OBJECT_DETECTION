# 🧾 Bone Fracture Detection

<p align="center">
  <img src="https://github.com/QaziSaim/End-to-end-OBJECT_DETECTION/blob/main/dafx.png" alt="banner"/>
</p>

---

## 📌 Problem Statement

Manual invoice processing is time-consuming, error-prone, and inefficient for businesses handling large volumes of bills. Extracting key information such as **date, total amount, and item details** requires significant manual effort and lacks scalability.

---

## 🎯 Objective

To build an automated system that:

* Detects key invoice fields using **Computer Vision**
* Extracts text using **OCR**
* Converts unstructured bill images into structured **JSON format**
* Provides a user-friendly interface for real-time processing

---

## 🚀 Solution Approach

This project integrates **YOLOv8 (Object Detection)** with **Tesseract OCR** to create a complete pipeline for invoice data extraction. The system identifies important regions in the bill and extracts meaningful information, which is then stored in a structured format.

---

## 🖼️ Results & Outputs

### 🔹 Input Image vs Prediction

<p align="center">
  <img src="https://via.placeholder.com/400x300.png?text=Original+Invoice" width="30%"/>
  <img src="https://via.placeholder.com/400x300.png?text=YOLO+Detection+Output" width="30%"/>
  <img src="https://via.placeholder.com/400x300.png?text=Bounding+Box+Visualization" width="30%"/>
</p>

### 🔹 Extracted JSON Output

<p align="center">
  <img src="https://via.placeholder.com/600x300.png?text=JSON+Output" width="60%"/>
</p>

---

## ⚙️ Project Workflow

```text
Download Dataset (Roboflow)
        ↓
Train YOLOv8 Model
        ↓
Detect Invoice Fields (Bounding Boxes)
        ↓
Extract Text using OCR (Tesseract)
        ↓
Convert Extracted Data → JSON
        ↓
Build Streamlit Web App
        ↓
Deploy on Streamlit Cloud
        ↓
CI/CD using GitHub Actions
```

---

## 🔄 Process Breakdown

### 1️⃣ Dataset Collection

* Downloaded and managed dataset using **Roboflow**
* Annotated invoice fields for object detection

### 2️⃣ Model Training

* Trained **YOLOv8 model** for detecting invoice components
* Achieved strong detection performance using optimized parameters

### 3️⃣ Detection

* Generated predictions with **bounding boxes** around key fields
* Visualized results for evaluation

### 4️⃣ OCR Extraction

* Used **Pytesseract** to extract text from detected regions

### 5️⃣ Data Structuring

* Converted extracted information into **JSON format**

### 6️⃣ Deployment

* Built UI using **Streamlit**
* Deployed on **Streamlit Cloud**

### 7️⃣ CI/CD

* Automated pipeline using **GitHub Actions**

---

## 🛠️ Tech Stack

* Python
* YOLOv8 (Ultralytics)
* OpenCV
* Tesseract OCR
* Streamlit
* GitHub Actions

---

## 🎯 Conclusion

This project demonstrates how **Computer Vision and OCR** can be combined to automate invoice processing, significantly reducing manual effort and improving efficiency in real-world business workflows.

---

## 🔮 Future Improvements

* Improve OCR accuracy using advanced models (EasyOCR / Transformer-based models)
* Support multiple invoice formats and layouts
* Integrate LLMs for intelligent data parsing
* Enable real-time invoice scanning via camera

---

## 👤 Author

**Saim Qazi**

* GitHub: *(Add your link)*
* LinkedIn: *(Add your link)*

---

### 🔥 Next Step

👉 Replace placeholder images with:

* Your **original invoice**
* Your **YOLO prediction output**
* Your **bounding box image**
* Your **JSON output screenshot**

👉 Create **actual Streamlit UI code + GitHub Actions YAML**
👉 Help you make this project **stand out for recruiters** 🚀

## Chat with document

## Setup

1. **Create a virtual environment**
```
python -m venv venv
```


2. **Activate the virtual environment**
- On Linux/Mac:
  ```
  source venv/bin/activate
  ```
- On Windows:
  ```
  venv\Scripts\activate
  ```

3. **Install dependencies**
```
pip install -r requirements.txt
```

---

## Running the Applications

### Frontend (Streamlit)
```
streamlit run run.py
```

### Backend (FastAPI/Flask)
```
python app.py
```

---

## Usage

1. Start both **frontend and backend**.
2. Open the frontend in your browser (Streamlit provides a local URL).
3. Click the **Upload** button to upload documents/files.  
   *![UI](screenshots\UI.png)*
4. After uploading, start a **chat about the uploaded topic**.

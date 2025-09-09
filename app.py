import os
import shutil
from fastapi import FastAPI, File, UploadFile, HTTPException, Request

from utilities.index_doc import index_document
from utilities.retriever import retrive_index

app = FastAPI()

@app.post("/query")
async def query_context(request: Request):
    try:
        data = await request.json()
        query = data.get("query")
        print(f"Received query: {query}")
        query_engine = retrive_index()
        response = query_engine.query(query)
        print(response)
        return {"response": str(response)}
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))


@app.post("/upload_document")
async def upload_file(file: UploadFile = File(...)):
    try:
        UPLOAD_DIR = "file_uploaded"
        print(f"Received file: {file.filename}")
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file selected")
        
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        file_path = os.path.join(UPLOAD_DIR,file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Index the document
        index_status = index_document(file_path)
        if not index_status:
            raise HTTPException(status_code=500, detail="Document indexing failed")
        return {"index_status": index_status}
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)




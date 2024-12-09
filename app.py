from fastapi import FastAPI, File, UploadFile
from unstructured.partition.auto import partition

app = FastAPI()

@app.post("/process-file")
async def process_file(file: UploadFile = File(...)):
    # Save the uploaded file
    temp_file_path = f"/tmp/{file.filename}"
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(await file.read())
    
    # Process the file using `partition`
    elements = partition(filename=temp_file_path)
    result = "\n\n".join([str(el) for el in elements])
    
    return {"elements": result}
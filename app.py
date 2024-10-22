from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import features
import os
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def home():
    return JSONResponse(content='API is running')

@app.post("/predictVideo")
async def predict_video(video: UploadFile = File(...)):

    try:
        video_path = "video.mp4"
        content = await video.read()
        with open(video_path, "wb") as video_file:
            video_file.write(content)

        prediction = features.video_classifier(video_path)
        return JSONResponse(content={'result':prediction})
    
    except:
        return JSONResponse(content={"message":"Error in reading Video Data"})
    

# @app.post("/predictImage")
# async def predict_image(image: UploadFile = File(...)):

#     try:
#         image_path = 'image.jpg'
#         content = await image.read()
#         with open(image_path, "wb") as video_file:
#             video_file.write(content)
        
#         prediction = features.image_classifier(image_path)
#         return JSONResponse(content={'result':prediction})

#     except:
#         return JSONResponse(content={"message":"Error in reading Image Data"})


@app.post("/predictImage")
async def predict_image(image: UploadFile = File(...)):
    try:
        # Create a unique filename for each uploaded image
        image_filename = f"{uuid.uuid4()}.jpg"
        image_path = f"./uploaded_images/{image_filename}"

        # Ensure the directory exists
        os.makedirs(os.path.dirname(image_path), exist_ok=True)

        # Save the uploaded image to the unique path
        content = await image.read()
        with open(image_path, "wb") as image_file:
            image_file.write(content)

        # Perform the prediction using your image classifier
        prediction = features.image_classifier(image_path)

        # Optionally delete the image after prediction if not needed
        os.remove(image_path)

        return JSONResponse(content={'result': prediction})

    except Exception as e:
        return JSONResponse(content={"message": f"Error in reading Image Data: {str(e)}"})
    
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=4000)
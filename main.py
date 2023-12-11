import os
import cv2

def convert_videos(input_folder, output_folder):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    output_files = os.listdir(output_folder)
    # Loop through all files in the input folder
    for filename in os.listdir(input_folder):
        
        print(f"starting file:{filename}")
        if filename in output_files:
            print("this file exists already")
            continue
        
        input_path = os.path.join(input_folder, filename)
        
        # Check if the file is a video file
        if os.path.isfile(input_path) and filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
            print(f"Converting {filename}...")

            # Read the video
            cap = cv2.VideoCapture(input_path)
            
            # Get video properties
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)*0.9)
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)*0.9)
            fps = cap.get(cv2.CAP_PROP_FPS)

            # Define the codec and create a VideoWriter object
            fourcc = cv2.VideoWriter_fourcc(*'avc1')
            output_path = os.path.join(output_folder, filename)
            out = cv2.VideoWriter(output_path, fourcc, fps, (640, int(640 * cap.get(cv2.CAP_PROP_FRAME_HEIGHT) / cap.get(cv2.CAP_PROP_FRAME_WIDTH))))

            # Read frames and write to the output video
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                resized_frame = cv2.resize(frame, (640, int(640 * frame.shape[0] / frame.shape[1])))
                out.write(resized_frame)

            # Release video capture and writer objects
            cap.release()
            out.release()

            print(f"{filename} converted and saved to {output_path}")


input_folder = r"D:\New folder (2)"

output_folder = r"D:\New folder"

convert_videos(input_folder, output_folder)



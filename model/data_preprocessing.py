import os
import pandas as pd
import cv2
import shutil
from sklearn.model_selection import train_test_split

# Paths
DATASET_PATH = "model/dataset/images"
ANNOTATIONS_FILE = "model/dataset/annotations.csv"
TRAIN_PATH = "model/dataset/train"
VAL_PATH = "model/dataset/val"

# Ensure directories exist and clean them if needed
for folder in [TRAIN_PATH, VAL_PATH]:
    os.makedirs(folder, exist_ok=True)
    for file in os.listdir(folder):  # Remove old images
        os.remove(os.path.join(folder, file))

# Load annotations
df = pd.read_csv(ANNOTATIONS_FILE)

# Check if the required columns exist
if 'filename' not in df.columns or 'label' not in df.columns:
    raise ValueError("Error: 'filename' or 'label' column missing in annotations.csv!")

# Split dataset (80% train, 20% validation)
train_df, val_df = train_test_split(df, test_size=0.2, random_state=42, stratify=df['label'])

def move_files(df, dest_folder):
    missing_files = 0
    for _, row in df.iterrows():
        img_name = row['filename']
        src_path = os.path.join(DATASET_PATH, img_name)
        dest_path = os.path.join(dest_folder, img_name)
        
        if os.path.exists(src_path):
            shutil.copy(src_path, dest_path)
        else:
            missing_files += 1
            print(f"⚠️ Warning: {img_name} not found in dataset!")

    print(f"✅ Moved {len(df) - missing_files} images to {dest_folder} ({missing_files} missing)")

# Move files to train and validation directories
move_files(train_df, TRAIN_PATH)
move_files(val_df, VAL_PATH)

# Print dataset summary
print("\n📊 Dataset split summary:")
print(f"🔹 Training set: {len(os.listdir(TRAIN_PATH))} images")
print(f"🔹 Validation set: {len(os.listdir(VAL_PATH))} images")
print("\n✅ Dataset split completed! Training and validation sets are ready.")
# 
import os
import json
import shutil
from pathlib import Path 
# this module will be used to clip validation and test dataset

def clip_dataset(src_folder, src_annotations_coco_json, target_folder, num_of_samples_with_obj, num_of_samples_without_obj):
    """
    (Dataset must be in COCO format)
    clip a dataset in the target_folder_path according to given parameters
    """

    src_folder_path = Path(src_folder)
    target_folder_path = Path(target_folder)

    target_folder_path.mkdir(parents=True, exist_ok=True)

    # read coco_json 
    with open(src_annotations_coco_json, 'r', encoding='utf-8') as f:
        coco_json = json.load(f)
    
    images = coco_json.get('images', [])
    annotations = coco_json.get('annotations', [])
    categories = coco_json.get('categories', [])

    # store images with objects in dict {image_id: annotation_of_image} 
    image_annotations = {}
    for annotation in annotations:
        image_id = annotation['image_id']

        # same image may contain multiple objects
        if image_id not in image_annotations:
            image_annotations[image_id] = [annotation]
        else:
            image_annotations[image_id].append(annotation)

    
    images_with_objects = []
    images_without_objects = []

    # seperate images into two list

    for image in images:
        image_id = image['id']

        # Make sure that image path is valid
        image_path = src_folder_path / image['file_name']
        if not image_path.exists():
            continue

        if image_id in image_annotations and len(image_annotations[image_id]) > 0:
            images_with_objects.append(image)
        else:
            images_without_objects.append(image)

    # Slice the list according to num_of_samples_with_obj and num_of_samples_without_obj
    if len(images_with_objects) > num_of_samples_with_obj:
        images_with_objects = images_with_objects[:num_of_samples_with_obj]
    else:
        print(f"Warning source dataset does not contain enought images with objects.\n Number of image with object:{len(images_with_objects)}")

    if len(images_without_objects) > num_of_samples_without_obj:
        images_without_objects = images_without_objects[:num_of_samples_without_obj]
    else:
        print(f"Warning source dataset does not contain enought images without objects.\n Number of image without object:{len(images_without_objects)}")
    
    selected_images = images_with_objects + images_without_objects

    # list the ids for new coco_json
    selected_image_ids = {image['id'] for image in selected_images}

    # list the annotations for new coco_json
    selected_image_annotations = [annotation for annotation in annotations if annotation['image_id'] in selected_image_ids]
    
    #new coco_json annotation file for new cliped dataset  
    target_coco_json = {
        "images": selected_images,
        "annotations": selected_image_annotations,
        "categories": categories
    }

    # copy all images into target folder
    for image in selected_images:
        shutil.copy(src_folder_path / image['file_name'], target_folder_path / image['file_name'])
    
    # create new coco_json annotation file in target folder
    target_coco_json_path = target_folder_path / "_annotations.coco.json"
    with open(target_coco_json_path, 'w', encoding='utf-8') as f:
        json.dump(target_coco_json, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    #create validation dataset
    clip_dataset("valid","valid\\_annotations.coco.json", "new_valid",200,600)
    #create test dataset
    clip_dataset("test","test\\_annotations.coco.json", "new_test",200,600)
import json
import os
import pandas as pd

def read_json(json_path, image_path):
    with open(json_path) as json_file:
        data = json.load(json_file)
    boxes = []
    list_boxes_raw = data['attributes']['_via_img_metadata']['regions']
    for box_raw in list_boxes_raw:
        box_pos = box_raw['shape_attributes']
        x1 = box_pos['x']
        y1 = box_pos['y']
        x2 = box_pos['x'] + box_pos['width']
        y2 = box_pos['y'] + box_pos['height']
        boxes.append([image_path, x1, y1, x2, y2, 'vertical'])
    return boxes

def convert_data_to_csv(image_path, json_path):
    list_images = os.listdir(image_path)
    data = []
    for image_name in list_images:
        name = image_name[:-4]
        image_data = read_json(json_path=os.path.join(json_path, name + '.json'), image_path=os.path.join(image_path, image_name))
        data += image_data
    path = [data[i][0] for i in range(len(data))]
    x1 = [data[i][1] for i in range(len(data))]
    y1 = [data[i][2] for i in range(len(data))]
    x2 = [data[i][3] for i in range(len(data))]
    y2 = [data[i][4] for i in range(len(data))]
    class_name = [data[i][5] for i in range(len(data))]
    df = pd.DataFrame({'path': path, 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'class_name': class_name})
    df.to_csv('train.csv', index=False)
    print('done!')
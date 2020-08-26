import json
import os
import pandas as pd
import cv2

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
    df.to_csv('train.csv', index=False, header=False)
    print('done!')

def intersection(a,b):
    if b[0] >= a[0] and b[2] <= a[2]:
        x = max(a[0], b[0])
        y = max(a[1], b[1])
        w = min(a[2], b[2]) - x
        h = min(a[3], b[3]) - y
        if w<0 or h<50: return False
        return (x, y, x + w, y + h)
    else:
        return False

def image_splitter(data_folder, image_name, w, h, ouput_folder, bbox):
    image = cv2.imread(os.path.join(data_folder, image_name))
    list_image = []
    converted_bbox = {}
    if image.shape[0] < h or image.shape[1] < w:
        list_image.append([0, 0, image.shape[1], image.shape[0]])
    else:
        check_w = True
        check_h = True
        next_point = (0, 0)
        while check_w:
            check_h = True
            x1, y1 = next_point[0], next_point[1]
            x2, y2 = x1 + w, y1 + h

            if x2 >= image.shape[1]:
                check_w = False
                if x2 > image.shape[1]:
                    x2 = image.shape[1]
                    x1 = x2 - w
            next_point = (x1 + int(w/3), y1)
            list_image.append([x1, y1, x2, y2])
            next_slide_w_point = (x1, y1 + int(h/3))
            while check_h:
                x1, y1 = next_slide_w_point
                x2, y2 = x1 + w, y1 + h
                if y2 >= image.shape[0]:
                    check_h = False
                    if y2 > image.shape[0]:
                        y2 = image.shape[0]
                        y1 = y2 - h
                next_slide_w_point = (x1, y1 + int(h/3))
                list_image.append([x1, y1, x2, y2])
    for i, pos in enumerate(list_image):
        image_piece_name = image_name.split('.')[0] + '_' + str(i) + '.png'
        x1, y1, x2, y2 = pos
        image_boxes = []
        for box in bbox:
            intersect = intersection(pos, box)
            if intersect:
                b_x1, b_y1, b_x2, b_y2 = intersect
                b_new_x1 = b_x1 - x1
                b_new_y1 = b_y1 - y1
                b_new_x2 = b_x2 - x1
                b_new_y2 = b_y2 - y1
                image_boxes.append((b_new_x1, b_new_y1, b_new_x2, b_new_y2))
        if len(image_boxes) != 0:
            converted_bbox[image_piece_name] = image_boxes
    cv2.imsave(os.path.join(ouput_folder, image_piece_name), image[y1:y2, x1:x2])
    return converted_bbox
    
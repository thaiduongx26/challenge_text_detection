import cv2  
import json
def draw_rectangle_image(image_path, json_path):
    def read_json(json_path):
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
            boxes.append((x1,y1,x2,y2))
        return boxes

    image = cv2.imread(image_path)
    image_boxes = read_json(json_path)
    for box in image_boxes:
        x1, y1, x2, y2 = box
        color = (255, 0, 0) 
        thickness = 2
        image = cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness) 
    cv2.imwrite('image_output.png', image)
    print('done!')
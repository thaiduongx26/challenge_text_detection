from process.data_generation import image_splitter
import os
import json

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

if __name__ == "__main__":
    imgs_folder = 'data/images'
    labels_folder = 'data/labels'
    output_folder = 'data/splitted_imgs'
    list_imgs = os.listdir(imgs_folder)
    res = {}
    for img in list_imgs:
        label_path = img.split('.')[0] + '.json'
        bbox = read_json(os.path.join(labels_folder, label_path))
        out = image_splitter(imgs_folder, img, output_folder, bbox)
        res.update(out)
    path = []
    x1 = []
    y1 = []
    x2 = []
    y2 = []
    class_name = []
    for img_name in res:
        for b in res[img_name]:
            path.append(os.path.join(output_folder, img_name))
            x1.append(b[0])
            y1.append(b[1])
            x2.append(b[2])
            y2.append(b[3])
            class_name.append('vertical')
    df = pd.DataFrame({'path': path, 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'class_name': class_name})
    df.to_csv('train_splitted.csv', index=False, header=False)
    print('done!')
    
# show.py
import json
import numpy as np
import torch
from PIL import Image, ImageDraw

# 连接关节的骨架列表，参考 BODY_25
POSE_PAIRS = [
    (0,1),(0,15),(0,16),(15,17),(16,18),
    (1,2),(1,5),(1,8),(2,3),(3,4),(5,6),(6,7),
    (8,9),(8,12),(9,10),(10,11),(11,22),(11,24),
    (22,23),(12,13),(13,14),(14,21),(14,19),(19,20)
]

def decode_json_to_batch(json_batch, canvas_size=(512,768)):
    imgs = []
    for rec in json_batch:
        width, height = rec.get('canvas_width',canvas_size[0]), rec.get('canvas_height',canvas_size[1])
        img = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(img)
        for person in rec.get('people', []):
            pts = person.get('pose_keypoints_2d', [])
            coords = [(pts[i], pts[i+1]) for i in range(0, len(pts), 3)]
            # 绘制点
            for x,y in coords:
                draw.ellipse((x-3, y-3, x+3, y+3), fill="red")
            # 绘制骨架
            for a,b in POSE_PAIRS:
                if a < len(coords) and b < len(coords):
                    xa, ya = coords[a]
                    xb, yb = coords[b]
                    draw.line((xa, ya, xb, yb), fill="blue", width=2)
        # 转为 Tensor (H,W,C)->(C,H,W) 并归一化
        arr = np.array(img).astype(np.float32) / 255.0
        t = torch.from_numpy(arr).permute(2,0,1)
        imgs.append(t)
    if not imgs:
        return torch.zeros(1,3,1,1)
    return torch.stack(imgs, dim=0)

if __name__ == "__main__":
    # 示例输入，可替换为文件读取
    sample = [
        # （此处插入你提供的 JSON 对象列表）
    ]
    batch = decode_json_to_batch(sample)
    print("Batch shape:", batch.shape)  # 比如 (5,3,768,512)
    # 可将每张图保存为 PNG
    for i, im in enumerate(batch):
        np_img = (im.permute(1,2,0).numpy()*255).astype(np.uint8)
        Image.fromarray(np_img).save(f"out_{i:03}.png")

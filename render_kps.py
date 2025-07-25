import json
import math
import cv2
import numpy as np
import torch
from collections import namedtuple
from typing import List, Union, NamedTuple
from .dwpose import *

def numpy2torch(np_image: np.ndarray) -> torch.Tensor:
    """ [H, W, C] => [B=1, H, W, C]"""
    return torch.from_numpy(np_image.astype(np.float32) / 255).unsqueeze(0)

class RenderKps:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "kps": ("POSE_KEYPOINT",),
                "render_body": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES   = ("IMAGE",)
    FUNCTION = "render"
    CATEGORY = "Snap Processing"

    def render(self, kps, render_body):
        frames = kps if isinstance(kps, list) else [kps]

        imgs = []
        for data in frames:
            if isinstance(data, list):
                data = data[0]
            if isinstance(data, str):
                try:
                    data = json.loads(data)
                except json.JSONDecodeError:
                    continue
            if not isinstance(data, dict):
                continue

            poses, _, H, W = decode_json_as_poses(data)
            np_img = draw_poses(poses, H, W, render_body)
            imgs.append(torch.from_numpy(np_img.astype(np.float32) / 255.0))  # [H,W,3]

        if not imgs:
            imgs = [torch.zeros((1, 1, 3), dtype=torch.float32)]


        batch = torch.stack(imgs, dim=0)  
        print("batch shape:", batch.shape)  

        return (batch,)

NODE_CLASS_MAPPINGS = {
    "RenderKps": RenderKps,
}

from .ratio_cau import CalculatePoseScales
from .frame_cau import ApplyPoseScalesToFrames
from .convertPoseToStandardFormat import ConvertPoseToStandardFormat
from .render_kps import RenderKps
# 把下面一行指向同目录下的 show.py


NODE_CLASS_MAPPINGS = {
    "CalculatePoseScales": CalculatePoseScales,
    "ApplyPoseScalesToFrames": ApplyPoseScalesToFrames,
    "ConvertPoseToStandardFormat": ConvertPoseToStandardFormat,
    "RenderKps": RenderKps,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CalculatePoseScales": "C&scales🧮",
    "ApplyPoseScalesToFrames" : "A&scales🔧",
    "ConvertPoseToStandardFormat" : "ConvertPose ✂️",
    "RenderKps" : "RenderKps 📹"
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]

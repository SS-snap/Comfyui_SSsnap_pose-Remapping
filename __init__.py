from .apply_diss_pose import ApplyPoseDiff
from .cha import PoseDiffCalculator

NODE_CLASS_MAPPINGS = {
    "ApplyPoseDiff": ApplyPoseDiff,
    "PoseDiffCalculator" : PoseDiffCalculator
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ApplyPoseDiff": "SSsnap Apply Pose Diff ✂️",
    "PoseDiffCalculator" : "SSsnap Pose Diff Calculator 🛠️"
}
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
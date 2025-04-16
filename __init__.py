from .apply_diss_pose import ApplyPoseDiff
from .DiffCalculator import PoseDiffCalculator
from .scaled_diff import CalcScaledPoseDiff

NODE_CLASS_MAPPINGS = {
    "ApplyPoseDiff": ApplyPoseDiff,
    "PoseDiffCalculator" : PoseDiffCalculator,
    "CalcScaledPoseDiff" : CalcScaledPoseDiff
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ApplyPoseDiff": "SSsnap Apply Pose Diff ✂️",
    "PoseDiffCalculator" : "SSsnap Pose Diff Calculator 🛠️",
    "CalcScaledPoseDiff" : "SSsnap Calc 🪛"
}
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
import json
import numpy as np

class PoseDiffCalculator:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "original_frame_pose": ("POSE_KEYPOINT", {}),
                "adjusted_frame_pose": ("POSE_KEYPOINT", {})
            }
        }

    RETURN_TYPES = ("POSE_KEYPOINT",)
    RETURN_NAMES = ("pose_diff",)
    FUNCTION = "calculate_diff"
    CATEGORY = "Snap Processing"

    def extract_pose(self, data):
        if isinstance(data, list):
            data = data[0]
        try:
            return np.array(data['people'][0]['pose_keypoints_2d'])
        except (IndexError, KeyError, TypeError):
            raise ValueError("Input pose data is invalid or malformed.")

    def calculate_diff(self, original_frame_pose, adjusted_frame_pose):
        original_pose = self.extract_pose(original_frame_pose)
        adjusted_pose = self.extract_pose(adjusted_frame_pose)

        # 检查数据有效性
        if original_pose.size == 0 or adjusted_pose.size == 0 or original_pose.size != adjusted_pose.size:
            raise ValueError("Input pose data is invalid or keypoints are mismatched.")

        # 计算差值
        pose_diff = (adjusted_pose - original_pose).tolist()

        # 构建差值数据
        diff_result = [{
            "people": [
                {
                    "pose_keypoints_2d": pose_diff
                }
            ]
        }]

        return (diff_result,)

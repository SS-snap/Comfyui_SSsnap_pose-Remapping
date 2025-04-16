import numpy as np

class CalcScaledPoseDiff:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "adjusted_pose": ("POSE_KEYPOINT", {}),
                "scaled_pose": ("POSE_KEYPOINT", {}),
            }
        }

    RETURN_TYPES = ("POSE_KEYPOINT",)
    RETURN_NAMES = ("scaled_pose_diff",)
    FUNCTION = "calc_diff"
    CATEGORY = "Snap Processing"

    def _extract_pose(self, data):
        if isinstance(data, list):
            data = data[0]
        return np.array(data["people"][0]["pose_keypoints_2d"]).reshape(-1, 3)

    def calc_diff(self, adjusted_pose, scaled_pose):
        adj_pose = self._extract_pose(adjusted_pose)
        scl_pose = self._extract_pose(scaled_pose)
        if adj_pose.shape != scl_pose.shape:
            raise ValueError("Pose shapes mismatch.")
        diff = scl_pose - adj_pose
        diff_list = diff.reshape(-1).tolist()
        result = [{
            "people": [{
                "pose_keypoints_2d": diff_list,
                "face_keypoints_2d": [],
                "hand_left_keypoints_2d": [],
                "hand_right_keypoints_2d": []
            }],
            "canvas_width": 0,
            "canvas_height": 0
        }]
        return (result,)

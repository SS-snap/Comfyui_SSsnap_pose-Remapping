import json
import numpy as np

class ApplyPoseDiff:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "pose_diff": ("POSE_KEYPOINT", {}),          # 差值数据
                "original_frame_pose": ("POSE_KEYPOINT", {}),# 原始关键帧数据
                "canvas_width": ("INT", {"default": 1440}),   # 画布宽度
                "canvas_height": ("INT", {"default": 1440})   # 画布高度
            }
        }

    # 输出类型为 POSE_KEYPOINT，直接对应 RenderPeopleKps 的输入
    RETURN_TYPES = ("POSE_KEYPOINT",)
    RETURN_NAMES = ("adjusted_frame_pose",)
    FUNCTION = "apply_diff"
    CATEGORY = "Snap Processing"

    def extract_pose_array(self, data):
        """
        安全地提取 people[0].pose_keypoints_2d，返回 numpy 数组。
        data 可能是 [ { ... } ] 或 { ... } 两种情况。
        """
        # 若外层是 list，就取第 0 个
        if isinstance(data, list):
            data = data[0]
        try:
            pose_list = data["people"][0]["pose_keypoints_2d"]
            return np.array(pose_list)
        except (IndexError, KeyError, TypeError):
            raise ValueError("Input pose data is invalid or malformed.")

    def extract_other_keypoints(self, data):
        """
        从原始数据中提取 face、手等信息，用于在输出里保持它们。
        若不需要保留，可注释掉。
        """
        if isinstance(data, list):
            data = data[0]
        # 为防止找不到对应字段，使用 get
        person = data["people"][0]
        return {
            "face_keypoints_2d": person.get("face_keypoints_2d", []),
            "hand_left_keypoints_2d": person.get("hand_left_keypoints_2d", []),
            "hand_right_keypoints_2d": person.get("hand_right_keypoints_2d", [])
        }

    def apply_diff(self, pose_diff, original_frame_pose, canvas_width, canvas_height):
        # 1) 提取原始 pose & 差值 pose
        original_array = self.extract_pose_array(original_frame_pose)
        diff_array = self.extract_pose_array(pose_diff)

        # 2) 检查一致性
        if original_array.size == 0 or diff_array.size == 0 or original_array.size != diff_array.size:
            raise ValueError("Input pose data is invalid or keypoints are mismatched.")

        # 3) 应用差值
        adjusted_array = (original_array + diff_array).tolist()

        # 4) 若想保留原始 hand/face 关键点，提取并合并
        other_kps = self.extract_other_keypoints(original_frame_pose)

        # 5) 构建新的关键帧数据 (Python 对象)
        #    与 RenderPeopleKps 中 decode_json_as_poses(kps) 兼容
        adjusted_frame = [{
            "people": [
                {
                    "pose_keypoints_2d": adjusted_array,
                    "hand_left_keypoints_2d": other_kps["hand_left_keypoints_2d"],
                    "hand_right_keypoints_2d": other_kps["hand_right_keypoints_2d"],
                    "face_keypoints_2d": other_kps["face_keypoints_2d"]
                }
            ],
            "canvas_width": canvas_width,
            "canvas_height": canvas_height
        }]

        # 返回一个 tuple，里面只有一个值，供 ComfyUI 使用
        return (adjusted_frame,)


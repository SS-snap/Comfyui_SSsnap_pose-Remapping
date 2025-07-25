import json
import numpy as np

class CalculatePoseScales:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "ref_json": ("POSE_KEYPOINT",),  # 标准化后 data.json 风格（list of frame dict）
                "raw_json": ("POSE_KEYPOINT",),  # 或者直接是关键点列表（KEY_POINTS）
            }
        }

    RETURN_TYPES = ("SCALES",)
    RETURN_NAMES = ("scales",)
    FUNCTION = "calculate_scales"
    CATEGORY = "Snap Processing"

    BONES = [
        ("neck-lshoulder", 1, 2),
        ("lshoulder-lelbow", 2, 3),
        ("lelbow-lwrist", 3, 4),
        ("neck-rshoulder", 1, 5),
        ("rshoulder-relbow", 5, 6),
        ("relbow-rwrist", 6, 7),
        ("neck-lhip", 1, 8),
        ("lhip-lknee", 8, 9),
        ("lknee-lankle", 9, 10),
        ("neck-rhip", 1, 11),
        ("rhip-rknee", 11, 12),
        ("rknee-rankle", 12, 13),
    ]

    def _to_kps_array(self, data):
        """
        将各种可能的输入:
          - JSON 字符串 (dict 或 list of dict)
          - Python dict
          - list of frame-dicts
          - list of floats 或 list of [x,y,c]
        统一转成 (N,3) 的 NumPy array。
        """
        # 如果是 JSON 字符串，先加载
        if isinstance(data, str):
            data = json.loads(data)

        # 如果是 dict，则当成单帧包装到 list
        if isinstance(data, dict):
            data = [data]

        # 如果是 list 且首元素是 dict → 标准化帧格式
        if isinstance(data, list) and data and isinstance(data[0], dict):
            frame = data[0]
            people = frame.get("people")
            if not isinstance(people, list) or not people:
                raise ValueError("frame 中找不到 people 列表")
            kp_list = people[0].get("pose_keypoints_2d")
            if not isinstance(kp_list, list):
                raise ValueError("people[0] 中找不到 pose_keypoints_2d")
            arr = np.array(kp_list, dtype=np.float32)

        # 如果是 list 且元素是数字序列 → 直接当成关键点数组
        elif isinstance(data, list) and data and isinstance(data[0], (int, float)):
            arr = np.array(data, dtype=np.float32)

        # 如果是嵌套 list ([[x,y,c],…])
        elif isinstance(data, list) and data and isinstance(data[0], list):
            arr = np.array(data, dtype=np.float32).reshape(-1, 3)

        else:
            raise ValueError(f"无法识别的 keypoints 输入格式: {type(data)}")

        # 最终统一 shape 成 (N,3)
        if arr.ndim == 1:
            arr = arr.reshape(-1, 3)
        if arr.shape[1] != 3:
            raise ValueError(f"关键点格式错误，应为 N×3，但得到 shape={arr.shape}")
        return arr

    def _segment_length(self, kps, i, j):
        a, b = kps[i, :2], kps[j, :2]
        # 置信度为 0 或者坐标全 0 时视为无效
        if np.any(a == 0) or np.any(b == 0):
            return np.nan
        return float(np.linalg.norm(a - b))

    def calculate_scales(self, ref_json, raw_json):
        # 把 ref_json 和 raw_json 都转成 (N,3) 数组
        kps_ref = self._to_kps_array(ref_json)
        kps_raw = self._to_kps_array(raw_json)

        scales = {}
        for name, i, j in self.BONES:
            len_ref = self._segment_length(kps_ref, i, j)
            len_raw = self._segment_length(kps_raw, i, j)
            if np.isnan(len_ref) or np.isnan(len_raw) or len_raw == 0:
                scales[name] = 1.0
            else:
                scales[name] = len_ref / len_raw
        return (scales,)


NODE_CLASS_MAPPINGS = {
    "CalculatePoseScales": CalculatePoseScales,
}

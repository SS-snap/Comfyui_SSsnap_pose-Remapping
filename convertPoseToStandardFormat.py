import json

class ConvertPoseToStandardFormat:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "raw_pose_data": ("POSE_KEYPOINT",),  
            }
        }

    RETURN_TYPES = ("POSE_KEYPOINT",)
    RETURN_NAMES = ("standardized_pose_data",)
    FUNCTION = "convert"
    CATEGORY = "Snap Processing"

    def convert(self, raw_pose_data):
       
        frames = []

        if isinstance(raw_pose_data, str):
            try:
                parsed = json.loads(raw_pose_data)
            except json.JSONDecodeError as e:
                raise ValueError(f"[ConvertPoseToStandardFormat] JSON 解析失败: {e}")
            if isinstance(parsed, dict):
                frames = [parsed]
            elif isinstance(parsed, list):
                frames = parsed
            else:
                raise ValueError(f"[ConvertPoseToStandardFormat] 解析后不是 dict/list: {type(parsed)}")

        elif isinstance(raw_pose_data, dict):
            frames = [raw_pose_data]

        elif isinstance(raw_pose_data, list):
            for idx, entry in enumerate(raw_pose_data):
                if isinstance(entry, dict):
                    frames.append(entry)
                elif isinstance(entry, str):
                    try:
                        e = json.loads(entry)
                    except json.JSONDecodeError:
                        raise ValueError(f"[ConvertPoseToStandardFormat] 第 {idx} 项 JSON 解析失败：{entry[:100]}…")
                    if isinstance(e, dict):
                        frames.append(e)
                    else:
                        raise ValueError(f"[ConvertPoseToStandardFormat] 第 {idx} 项解析后不是 dict: {type(e)}")
                else:
                    raise ValueError(f"[ConvertPoseToStandardFormat] 第 {idx} 项类型不支持: {type(entry)}")
        else:
            raise ValueError(f"[ConvertPoseToStandardFormat] 不支持的 raw_pose_data 类型: {type(raw_pose_data)}")

        output = []
        for frame in frames:
            ppl = frame.get("people")
            if not isinstance(ppl, list) or len(ppl) == 0:
                
                print(f"[ConvertPoseToStandardFormat] 跳过无效 frame：{frame}")
                continue

            new_people = []
            for person in ppl:
                new_people.append({
                    "pose_keypoints_2d": person.get("pose_keypoints_2d", []),
                    "face_keypoints_2d": [],
                    "hand_left_keypoints_2d": [],
                    "hand_right_keypoints_2d": [],
                })

            output.append({"people": new_people})

        return (output,)


NODE_CLASS_MAPPINGS = {
    "ConvertPoseToStandardFormat": ConvertPoseToStandardFormat,
}

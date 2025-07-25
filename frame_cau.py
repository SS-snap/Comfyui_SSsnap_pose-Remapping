import json
import numpy as np

class ApplyPoseScalesToFrames:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "frame_list": ("POSE_KEYPOINT",),  
                "scales":     ("SCALES",),         
                "ref_pose":   ("POSE_KEYPOINT",),  
            }
        }

    RETURN_TYPES   = ("POSE_KEYPOINT",)
    RETURN_NAMES   = ("new_frame_list",)
    FUNCTION       = "apply_scales"
    CATEGORY       = "Snap Processing"


    NECK = 1
    L_SHOULDER, L_ELBOW, L_WRIST = 2, 3, 4
    R_SHOULDER, R_ELBOW, R_WRIST = 5, 6, 7
    L_HIP, L_KNEE, L_ANKLE       = 8, 9, 10
    R_HIP, R_KNEE, R_ANKLE       = 11, 12, 13


    BONE_STEPS = [
        ("neck-lshoulder", NECK, L_SHOULDER, [L_SHOULDER, L_ELBOW, L_WRIST]),
        ("lshoulder-lelbow", L_SHOULDER, L_ELBOW, [L_ELBOW, L_WRIST]),
        ("lelbow-lwrist", L_ELBOW, L_WRIST, [L_WRIST]),
        ("neck-rshoulder", NECK, R_SHOULDER, [R_SHOULDER, R_ELBOW, R_WRIST]),
        ("rshoulder-relbow", R_SHOULDER, R_ELBOW, [R_ELBOW, R_WRIST]),
        ("relbow-rwrist", R_ELBOW, R_WRIST, [R_WRIST]),
        ("neck-lhip", NECK, L_HIP, [L_HIP, L_KNEE, L_ANKLE]),
        ("lhip-lknee", L_HIP, L_KNEE, [L_KNEE, L_ANKLE]),
        ("lknee-lankle", L_KNEE, L_ANKLE, [L_ANKLE]),
        ("neck-rhip", NECK, R_HIP, [R_HIP, R_KNEE, R_ANKLE]),
        ("rhip-rknee", R_HIP, R_KNEE, [R_KNEE, R_ANKLE]),
        ("rknee-rankle", R_KNEE, R_ANKLE, [R_ANKLE]),
    ]


    @staticmethod
    def move_branch(kp, parent, child, scale, subtree):
        p = kp[parent, :2].copy()
        c = kp[child,  :2].copy()
        new_c = p + (c - p) * scale
        offset = new_c - c
        kp[child, :2] = new_c
        for idx in subtree[1:]:
            kp[idx, :2] += offset


    def apply_scales(self, frame_list, scales, ref_pose):
        smooth_alpha = 0.2               


        ref_json = ref_pose[0] if isinstance(ref_pose, list) else ref_pose
        if isinstance(ref_json, str):
            ref_json = json.loads(ref_json)
        ref_kp = np.array(
            ref_json["people"][0]["pose_keypoints_2d"], dtype=np.float32
        ).reshape(-1, 3)

        delta_map = None          
        prev_smoothed = None      

        new_frames = []
        for frame_idx, frame in enumerate(frame_list):
            person = frame["people"][0]
            kp = np.array(person["pose_keypoints_2d"], dtype=np.float32).reshape(-1, 3)


            for name, parent, child, subtree in self.BONE_STEPS:
                self.move_branch(
                    kp, parent, child,
                    scales.get(name, 1.0), subtree
                )


            if delta_map is None:
                delta_map = ref_kp[:, :2] - kp[:, :2]   


            kp[:, :2] += delta_map


            if prev_smoothed is not None:
                kp[:, :2] = prev_smoothed[:, :2] + smooth_alpha * (
                    kp[:, :2] - prev_smoothed[:, :2]
                )
            prev_smoothed = kp.copy()


            person["pose_keypoints_2d"]      = kp.reshape(-1).tolist()
            person["face_keypoints_2d"]      = []
            person["hand_left_keypoints_2d"] = []
            person["hand_right_keypoints_2d"] = []
            new_frames.append(frame)

        return (new_frames,)


NODE_CLASS_MAPPINGS = {
    "ApplyPoseScalesToFrames": ApplyPoseScalesToFrames,
}

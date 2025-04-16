import numpy as np
import json

class ApplyPoseDiff:
    @classmethod
    def INPUT_TYPES(cls):
        toggles = {
            "neck": ("BOOLEAN", {"default": False}),
            "right_elbow": ("BOOLEAN", {"default": False}),
            "right_wrist": ("BOOLEAN", {"default": True}),
            "left_elbow": ("BOOLEAN", {"default": False}),
            "left_wrist": ("BOOLEAN", {"default": True}),
            "right_knee": ("BOOLEAN", {"default": False}),
            "right_ankle": ("BOOLEAN", {"default": False}),
            "left_knee": ("BOOLEAN", {"default": False}),
            "left_ankle": ("BOOLEAN", {"default": False})
        }
        required = {
            "pose_diff": ("POSE_KEYPOINT", {}),
            "original_frame_pose": ("POSE_KEYPOINT", {}),
            "prev_original_frame_pose": ("POSE_KEYPOINT", {}),
            "canvas_width": ("INT", {"default": 1440}),
            "canvas_height": ("INT", {"default": 1440}),
            **toggles
        }
        optional = {
            "scaled_pose_diff": ("POSE_KEYPOINT", {}),
            "current_step": ("INT", {}),
            "total_steps": ("INT", {})
        }
        return {"required": required, "optional": optional}

    RETURN_TYPES = ("POSE_KEYPOINT",)
    RETURN_NAMES = ("adjusted_frame_pose",)
    FUNCTION = "apply_diff"
    CATEGORY = "Snap Processing"

    COCO18_MAP = {
        1: "neck", 3: "left_elbow", 4: "left_wrist",
        6: "right_elbow", 7: "right_wrist",
        9: "left_knee", 10: "left_ankle",
        12: "right_knee", 13: "right_ankle",
    }

    BODY25_MAP = {
        1: "neck", 3: "left_elbow", 4: "left_wrist",
        6: "right_elbow", 7: "right_wrist",
        10: "left_knee", 11: "left_ankle",
        13: "right_knee", 14: "right_ankle",
    }

    def _arr(self, d):
        if isinstance(d, list):
            d = d[0]
        return np.array(d["people"][0]["pose_keypoints_2d"]).reshape(-1, 3)

    def _others(self, d):
        if isinstance(d, list):
            d = d[0]
        p = d["people"][0]
        return {
            "face_keypoints_2d": p.get("face_keypoints_2d", []),
            "hand_left_keypoints_2d": p.get("hand_left_keypoints_2d", []),
            "hand_right_keypoints_2d": p.get("hand_right_keypoints_2d", [])
        }

    def apply_diff(
        self,
        pose_diff,
        original_frame_pose,
        prev_original_frame_pose,
        canvas_width,
        canvas_height,
        scaled_pose_diff=None,
        current_step=None,
        total_steps=None,
        **kw
    ):
        cur = self._arr(original_frame_pose)
        prev = self._arr(prev_original_frame_pose)
        delta = self._arr(pose_diff)

        if cur.shape != prev.shape or cur.shape != delta.shape:
            raise ValueError("Pose size mismatch.")
        n_pts = delta.shape[0]
        idx_map = self.BODY25_MAP if n_pts >= 25 else self.COCO18_MAP

        eps = 1e-5
        ratio = np.linalg.norm((cur - prev)[:, :2]) / max(np.linalg.norm(delta[:, :2]), eps)

        mask = np.zeros((n_pts, 1), dtype=bool)
        for idx, name in idx_map.items():
            if idx < n_pts and kw.get(name, False):
                mask[idx] = True

        final_delta = np.where(mask, delta * ratio, delta)
        adj = cur + final_delta

        # ---------- 缓动应用 scaled_pose_diff ---------- #
        if (
            scaled_pose_diff is not None
            and current_step is not None
            and total_steps is not None
        ):
            spd = self._arr(scaled_pose_diff)
            if spd.shape == adj.shape:
                if total_steps <= 1 or current_step <= 1:
                    t = 0.0
                elif current_step >= total_steps:
                    t = 1.0
                else:
                    t = current_step / total_steps
                adj += spd * t

        out = adj.reshape(-1).tolist()
        others = self._others(original_frame_pose)
        return ([{
            "people": [{
                "pose_keypoints_2d": out,
                "hand_left_keypoints_2d": others["hand_left_keypoints_2d"],
                "hand_right_keypoints_2d": others["hand_right_keypoints_2d"],
                "face_keypoints_2d": others["face_keypoints_2d"]
            }],
            "canvas_width": canvas_width,
            "canvas_height": canvas_height
        }],)

        return (adjusted_frame,)

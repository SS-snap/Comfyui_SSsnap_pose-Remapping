# OpenPose_Remapping for ComfyUI(骨骼重映射节点)

> ✨ A pose remapping node with support for joint locking, motion-aware scaling, and optional easing – perfect for animation refinement and mech rig control.

一个用于 **骨骼重映射（Skeleton Remapping）** 的 ComfyUI 节点，支持锁定躯干、末端关键点比例调节、帧间缓动过渡等功能，可用于高质量的人体姿态变换、动画平滑处理与机甲刚体控制。

---

🧠 Features | 功能特点
---

✅ Skeleton Remapping – Automatically remap pose differences from the first frame to the entire animation

✅ 骨骼重映射：基于第一帧姿态差异，自动映射全帧姿态

✅ Motion-Aware Scaling – Dynamically scale movement on end-effectors (hands, feet) based on motion magnitude

✅ 支持比例缩放：末端关键点（手、脚）动作幅度可自适应

✅ Joint Locking – Keep shoulders and hips fixed to preserve torso stability

✅ 关节锁定：肩膀与髋部始终固定，保持身体稳定性

✅ Easing to Target Poses – Supports optional scaled_pose_diff + t to smoothly blend into global targets

✅ 动作缓动过渡：支持 optional scaled_pose_diff + t，实现向任意姿态过渡

✅ COCO‑18 & BODY‑25 Compatible – Auto-detects keypoint format

✅ 兼容 COCO‑18 与 BODY‑25：自动判断关键点格式

✅ Native ComfyUI Integration – Seamlessly works with ControlNet-style pose pipelines

✅ ComfyUI 原生节点，支持与 ControlNet pose pipeline 无缝集成

🚀 Use Cases | 应用场景
---
🔄 Smooth animation retargeting for pose keypoints

姿态动画过渡平滑化

🤖 Mecha / Robot control with rigid torso preservation

机器人 / 机甲 动作调整（保持躯干刚性）


---

## 🔧 Node Inputs | 节点输入说明

| 输入名                | 类型              | 描述 |
|---------------------|------------------|------|
| `pose_diff`         | `POSE_KEYPOINT`  | 初始差值（调整后 - 原始） |
| `original_frame_pose` | `POSE_KEYPOINT` | 当前帧原始姿态 |
| `prev_original_frame_pose` | `POSE_KEYPOINT` | 上一帧原始姿态，用于动作幅度计算 |
| `scaled_pose_diff` *(可选)* | `POSE_KEYPOINT` | 全局目标位置差值（最终 - 当前），用于缓动过渡 |
| `current_step` *(可选)*     | `INT`          | 当前帧序号（用于插值） |
| `total_steps` *(可选)*      | `INT`          | 总帧数（用于插值） |
| `canvas_width`       | `INT`           | 输出图像宽度 |
| `canvas_height`      | `INT`           | 输出图像高度 |


## display

Skeletal Remapping +  3D Composition 🦴
https://github.com/user-attachments/assets/b6460591-ad93-46fb-b4f5-864b4b4cceac

Multi-Camera AI Cinematography 📹
https://github.com/user-attachments/assets/a90f4005-d8f7-46fa-a9cf-e05332fcb654









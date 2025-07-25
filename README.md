# OpenPose_Remapping for ComfyUI(骨骼重映射节点)

> ✨ A pose remapping node with support for joint locking, motion-aware scaling, and optional easing – perfect for animation refinement and mech rig control.

一个用于 **骨骼重映射（Skeleton Remapping）** 的 ComfyUI 节点，支持锁定躯干、末端关键点比例调节、帧间缓动过渡等功能，可用于高质量的人体姿态变换、动画平滑处理与机甲刚体控制。

---

# Pose Remapping 节点更新声明（7.25）

我们对以下节点进行了功能增强与优化，适配更灵活的人体姿态重建需求：

## ✅ 更新节点列表与说明

### 1. `ApplyPoseScalesToFrames`
- 支持按骨骼段进行 **比例缩放**
- 支持以参考帧为锚点进行 **全局位置对齐**
- 内置 **帧间平滑（EMA）**，减少动画抖动

### 2. `RenderKps`
- 支持批量渲染 **多帧姿态图像**
- 输出为 ComfyUI 兼容图像列表，可用于后续处理或预览

### 3. `ApplyPoseDiff`
- 应用两帧姿态间的 **差值位移**
- 可选择性缩放末端关节（腕、踝等）
- 支持缓动过渡，适合生成流畅的骨骼动画序列

---

这些节点可协同使用，完成从关键点解析、比例适配、动态迁移到图像渲染的完整流程。

更新时间：2025-07-25  
作者：SSsnap

---
## 🔗 相关资源

- 🧠 **模型下载地址**：  
  [Wan2.1-Fun-14B-Control（Hugging Face）](https://huggingface.co/alibaba-pai/Wan2.1-Fun-14B-Control/tree/main)

- 🧩 **ComfyUI 配套节点**：  
  [ComfyUI OpenPose editor（GitHub）](https://github.com/huchenlei/ComfyUI-openpose-editor)

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

| 输入名          | 类型              | 描述                             |
| ------------ | --------------- | ------------------------------ |
| `frame_list` | `POSE_KEYPOINT` | 多帧姿态数据（待缩放与对齐）                 |
| `scales`     | `SCALES`        | 每条骨骼的缩放比例（如左臂、右腿）              |
| `ref_pose`   | `POSE_KEYPOINT` | 用于初始对齐的参考姿态帧（例如原始 OpenPose 输出） |
| 输入名           | 类型              | 描述              |
| ------------- | --------------- | --------------- |
| `kps`         | `POSE_KEYPOINT` | 多帧关键点数据         |
| `render_body` | `BOOLEAN`       | 是否绘制身体主骨架（默认启用） |



## display

Skeletal Remapping +  3D Composition 🦴



https://github.com/user-attachments/assets/2134ba60-9526-40a6-a653-072945422101




Multi-Camera AI Cinematography 📹






https://github.com/user-attachments/assets/24875b91-3c67-46d1-898a-2f374f9b94da









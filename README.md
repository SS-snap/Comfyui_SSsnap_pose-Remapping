# ApplyPoseDiff – 姿态缓动调整节点 for ComfyUI

A smooth pose transformation node for OpenPose keypoints in ComfyUI, supporting easing-based motion, joint locking, and dynamic action scaling.

一个适用于 ComfyUI 的 OpenPose 姿态平滑过渡节点，支持线性缓动、比例缩放和关节锁定，帮助你生成自然连贯的动画动作。

---

## 🧠 Features | 功能特点

- ✅ 支持 COCO‑18 与 BODY‑25 两种姿态格式  
- ✅ 锁定肩膀与髋部关键点，避免躯干漂移  
- ✅ 手动开启末端关键点（腕、肘、膝、踝、颈部）是否参与比例计算  
- ✅ 使用线性缓动，t ∈ [0,1] 实现平滑过渡  
- ✅ 自动根据前后帧动作幅度，动态调整差值比例  
- ✅ 可选的 `scaled_pose_diff` 实现全局过渡到指定目标姿态  
- ✅ 可用于任何支持 `POSE_KEYPOINT` 的渲染节点，如 `RenderPeopleKps`

---

## 🚀 Use Cases | 应用场景

- 姿态动画过渡平滑化  
- 机器人 / 机甲 动作调整（保持躯干刚性）  
- 手工编辑后的关键帧修复  
- OpenPose 驱动的动作补间与矫正  
- 多段姿态插值动画构建

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
| *末端关节开关*         | `BOOLEAN`       | 是否启用该关键点的比例变换（如 left_wrist、right_ankle 等） |

---

## ⚙️ Internal Logic | 节点核心逻辑

### 1. 应用姿态差值

使用 `pose_diff`（初始调整差）对每帧姿态进行叠加，肩部和髋部始终应用，不做比例调整。

### 2. 动作幅度比例控制

动态计算当前帧动作与初始差值的比例：

```python
ratio = ||cur - prev|| / (||pose_diff|| + ε)

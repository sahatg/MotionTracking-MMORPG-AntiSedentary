# MotionTracking-MMORPG-AntiSedentary
Image Processing Project Group 6 - Telecommunications Engineering ITERA

# MOTION TRACKING-BASED GAME INTERACTION SYSTEM FOR SEDENTARY LIFESTYLE MITIGATION IN MMORPG PLAYERS

This project was developed to fulfill the requirements of the **Image Processing (Pengolahan Citra)** course at **Institut Teknologi Sumatera (ITERA)**. The system utilizes a standard webcam as a visual input to track the player's physical movements in real-time, converting them into keyboard controls for an MMORPG game (specifically simulated for the *Mage* class) to mitigate the adverse effects of a sedentary lifestyle.

---

## 👥 Team Members (Group 6)
* **Sahat Juniver Danny Tredo Gultom** (122400106)
* **Maya Lestari** (122400010)
* **Dhiya Maharanni** (122400019)

**Telecommunications Engineering Study Program | Faculty of Industrial Technology** **Institut Teknologi Sumatera** **2026**

---

## 🛠️ Core Technologies & Frameworks
The system is built entirely within the Python ecosystem using the following core libraries:
* **OpenCV (`cv2`)**: Used for real-time video stream acquisition from the webcam, image manipulation (mirroring for natural feedback), and On-Screen Display (OSD) visualizations.
* **MediaPipe Pose (`BlazePose`)**: Utilized to extract 33 skeletal body landmark coordinates instantly with a minimum detection and tracking confidence threshold of `0.5`.
* **PyDirectInput**: Used to simulate direct low-level OS keyboard inputs (`press`, `keyDown`, `keyUp`) that are fully compatible with modern 3D MMORPG rendering engines.

---

## ⚙️ Movement Detection Logic & In-Game Mapping (Mage Class)
The system processes normalized landmark coordinates and translates them via a robust rule-based method using the following control mapping:

| No | Physical Movement | Sensor Logic / Threshold | Simulated Keyboard Action |
|----|-------------------|--------------------------|---------------------------|
| 1  | **Physical Jump** | Detects sudden vertical shoulder acceleration (`oldest_y - avg_shoulder_y > 0.05`) with a 1-second cooldown. | `SPACE` (Character Jumps) |
| 2  | **Outstretched Arms (T-Pose)** | Wrist-to-shoulder width ratio `> 2.5` kept strictly within the chest area level. | `5` (Cast Mount / Summon Mount) |
| 3  | **Clapping Hands** | Horizontal distance between wrists `< 0.08` while positioned below the shoulders. | `TAB` (Cycle Enemy Targets) |
| 4  | **Leaning Left** | Average horizontal shoulder coordinate moves beyond the hip threshold (`-0.04`). | Holds `A` (Strafe Left) |
| 5  | **Leaning Right** | Average horizontal shoulder coordinate moves beyond the hip threshold (`+0.04`). | Holds `D` (Strafe Right) |
| 6  | **Raising Right Hand** | Right wrist rises above the right shoulder level. | `1` (Cast Spell: *Fireball*) |
| 7  | **Raising Left Hand** | Left wrist rises above the left shoulder level. | `2` (Cast Spell: *Frostbolt*) |
| 8  | **Raising Both Hands** | Both wrists rise above their respective shoulders simultaneously. | `4` (Cast AoE Spell: *Frost Nova*) |
| 9  | **Hand-to-Nose (Drinking)** | Distance from either wrist to the nose landmark falls `< 0.1`. | `3` (Use Consumable: *Drink Mana*) |
| 10 | **High Knees / Jogging in Place** | Vertical knee coordinate rises closer to the hip level (`threshold 0.15`). | Holds `W` (Character Moves Forward) |

*Note: The script features built-in state debouncing, a walk timeout buffer, and an emergency failsafe that automatically releases all held keys (`w`, `a`, `d`) when exiting the application with the 'ESC' key to prevent operating system key-binding lockups.*

---

## 📂 Repository Layout
* **`src/`**: Contains `main.py` which holds the fully implemented OpenCV, MediaPipe, and PyDirectInput integration.
* **`docs/`**: Holds the formal academic Progress Report (`Laporan Kemajuan 2`) document.

---

## 🔒 Privacy & Data Safety Statement
All video frame processing, landmark extraction, and control conversions take place locally on the user's host machine (*edge computing*). This software **does not record, store, or transmit any visual video data** to external cloud servers, guaranteeing absolute privacy for the player.

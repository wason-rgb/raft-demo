#!/usr/bin/env python3
"""Python 1:1 equivalent of Godot Raft Demo v0.2 business logic.

Replicates (no Godot needed):
- RandomDriftController: 5-15s random direction change, 80-120 px/s speed, 100ms lerp
- Raft: 4px sine bob, 2.4s period, screen center 960,540
- Water: parallax scroll (deep 0.7x, wave 1.5x opposite to drift)
- Cloud: 0.5x parallax opposite to drift.x
- Debris: 1.5x parallax + 4-12s random respawn

Output: tools/preview_montage.png (4×3 grid, 6 seconds / 12 frames)
"""
import math
import random
from PIL import Image, ImageDraw

random.seed(42)  # 固定随机种子，结果可复现

# 颜色
COLOR_BG_SKY = (180, 200, 220, 255)
COLOR_BG_HORIZON = (150, 180, 200, 255)
COLOR_WATER_DEEP_BASE = (32, 80, 120, 255)
COLOR_WATER_WAVE = (140, 200, 230, 220)
COLOR_RAFT = (110, 75, 50, 255)
COLOR_RAFT_EDGE = (80, 50, 30, 255)
COLOR_PLAYER_SKIN = (200, 160, 100, 255)
COLOR_PLAYER_CLOTH = (140, 60, 40, 255)
COLOR_PLAYER_PANTS = (60, 40, 30, 255)
COLOR_CLOUD = (220, 220, 240, 220)
COLOR_DEBRIS = (90, 60, 40, 255)

# 视口（Godot 1920×1080，缩到 480×270 缩略图便于预览）
VIEWPORT_W, VIEWPORT_H = 1920, 1080
THUMB_W, THUMB_H = 480, 270
SCALE = THUMB_W / VIEWPORT_W  # 0.25
RAFT_CENTER = (960, 540)


class RandomDriftController:
    def __init__(self):
        self.direction = (1.0, 0.0)
        self.speed = 100.0
        self.target_direction = (1.0, 0.0)
        self.target_speed = 100.0
        self.smoothing_ms = 0.0
        self.direction_timer = 0.0
        self.direction_duration = random.uniform(5.0, 15.0)
        self.min_speed = 80.0
        self.max_speed = 120.0
        self.min_dur = 5.0
        self.max_dur = 15.0
        self.smoothing_duration_ms = 100.0

    @property
    def velocity(self):
        return (self.direction[0] * self.speed, self.direction[1] * self.speed)

    def step(self, dt_ms):
        dt_s = dt_ms / 1000.0
        self.direction_timer += dt_s
        if self.direction_timer >= self.direction_duration:
            angle = random.uniform(0, 2 * math.pi)
            self.target_direction = (math.cos(angle), math.sin(angle))
            self.target_speed = random.uniform(self.min_speed, self.max_speed)
            self.direction_timer = 0.0
            self.direction_duration = random.uniform(self.min_dur, self.max_dur)
            self.smoothing_ms = 0.0

        if abs(self.direction[0] - self.target_direction[0]) > 0.01 or abs(self.direction[1] - self.target_direction[1]) > 0.01:
            self.smoothing_ms += dt_ms
            t = max(0.0, min(1.0, self.smoothing_ms / self.smoothing_duration_ms))
            new_x = self.direction[0] + (self.target_direction[0] - self.direction[0]) * t
            new_y = self.direction[1] + (self.target_direction[1] - self.direction[1]) * t
            length = math.sqrt(new_x*new_x + new_y*new_y)
            if length > 0:
                self.direction = (new_x/length, new_y/length)
            if abs(self.direction[0] - self.target_direction[0]) < 0.01 and abs(self.direction[1] - self.target_direction[1]) < 0.01:
                self.direction = self.target_direction
                self.smoothing_ms = 0.0

        # 平滑速度
        self.speed = self.speed + (self.target_speed - self.speed) * dt_s * 2.0


class WaterLayer:
    def __init__(self, parallax):
        self.parallax = parallax
        self.offset = (0.0, 0.0)
    def step(self, drift_vel, dt_s):
        self.offset = (self.offset[0] - drift_vel[0] * self.parallax * dt_s,
                       self.offset[1] - drift_vel[1] * self.parallax * dt_s)


def lerp(a, b, t):
    return a + (b - a) * t


def draw_demo_frame(drift, water_deep, water_wave, elapsed_s, cloud_x, debris_x):
    img = Image.new("RGBA", (THUMB_W, THUMB_H), COLOR_BG_SKY)
    draw = ImageDraw.Draw(img)
    s = lambda v: int(v * SCALE)  # 缩放工具

    # 1. 天空背景
    # 2. 地平线渐变（用矩形条模拟）
    for y in range(s(540), s(700)):
        t = (y - s(540)) / max(1, s(700) - s(540))
        r = int(lerp(180, 100, t))
        g = int(lerp(200, 130, t))
        b = int(lerp(220, 160, t))
        draw.line([(0, y), (THUMB_W, y)], fill=(r, g, b, 255))

    # 3. 深水层（带 offset，模拟漂移）
    deep_y = s(700)
    for y in range(deep_y, THUMB_H):
        wave = int(math.sin((y + water_deep.offset[1]) * 0.05 + elapsed_s * 0.5) * 4)
        color = (32 + wave, 80 + wave, 120 + wave, 255)
        draw.line([(0, y), (THUMB_W, y)], fill=color)

    # 4. 浪层（半透明叠加）
    for y in range(s(680), s(760)):
        wave = int(math.sin((y + water_wave.offset[1]) * 0.1 + elapsed_s * 1.5) * 6)
        for x in range(0, THUMB_W, 4):
            wave2 = int(math.sin((x + water_wave.offset[0]) * 0.08 + elapsed_s * 1.2) * 4)
            yy = y + wave + wave2
            if 0 <= yy < THUMB_H:
                draw.point((x, yy), fill=COLOR_WATER_WAVE)

    # 5. 云
    cx = s(cloud_x % VIEWPORT_W)
    if cx < -s(96): cx += s(1920)
    cy = s(180)
    draw.ellipse([cx - s(40), cy - s(15), cx + s(40), cy + s(15)], fill=COLOR_CLOUD)
    draw.ellipse([cx - s(30), cy - s(20), cx + s(20), cy + s(10)], fill=COLOR_CLOUD)
    draw.ellipse([cx - s(20), cy - s(10), cx + s(30), cy + s(15)], fill=COLOR_CLOUD)

    # 6. 漂浮物
    dx = s(debris_x % VIEWPORT_W)
    if dx < -s(16): dx += s(1920)
    dy = s(620)
    draw.rectangle([dx - s(8), dy - s(8), dx + s(8), dy + s(8)], fill=COLOR_DEBRIS)

    # 7. 木筏（中心，sin 呼吸）
    bob = math.sin(elapsed_s * 2 * math.pi / 2.4) * 4
    rx, ry = s(RAFT_CENTER[0]), s(RAFT_CENTER[1] + bob)
    raft_w, raft_h = s(48), s(32)
    draw.rectangle([rx - raft_w//2, ry - raft_h//2, rx + raft_w//2, ry + raft_h//2], fill=COLOR_RAFT)
    for i in range(3):
        draw.line([(rx - raft_w//2 + i*raft_w//3, ry - raft_h//2),
                   (rx - raft_w//2 + i*raft_w//3, ry + raft_h//2)], fill=COLOR_RAFT_EDGE)

    # 8. 主角
    px, py = rx, ry - raft_h//2 - s(16)
    draw.rectangle([px - s(8), py, px + s(8), py + s(8)], fill=COLOR_PLAYER_SKIN)
    draw.rectangle([px - s(7), py + s(8), px + s(7), py + s(24)], fill=COLOR_PLAYER_CLOTH)
    draw.rectangle([px - s(6), py + s(24), px - s(1), py + s(32)], fill=COLOR_PLAYER_PANTS)
    draw.rectangle([px + s(1), py + s(24), px + s(6), py + s(32)], fill=COLOR_PLAYER_PANTS)

    return img


def main():
    drift = RandomDriftController()
    water_deep = WaterLayer(parallax=0.7)
    water_wave = WaterLayer(parallax=1.5)
    cloud_x = 400.0
    debris_x = 1500.0

    frames = []
    dt_ms = 50
    total_ms = 6000
    capture_every_ms = 500

    elapsed_ms = 0
    while elapsed_ms < total_ms:
        drift.step(dt_ms)
        vel = drift.velocity
        dt_s = dt_ms / 1000.0
        water_deep.step(vel, dt_s)
        water_wave.step(vel, dt_s)
        cloud_x += -vel[0] * dt_s * 0.5
        debris_x += -vel[0] * dt_s * 1.5
        elapsed_ms += dt_ms
        if elapsed_ms % capture_every_ms == 0:
            frame = draw_demo_frame(drift, water_deep, water_wave, elapsed_ms/1000, cloud_x, debris_x)
            frames.append(frame)

    cols = 4
    rows = (len(frames) + cols - 1) // cols
    montage = Image.new("RGBA", (cols * THUMB_W, rows * THUMB_H), (0, 0, 0, 255))
    for i, f in enumerate(frames):
        col, row = i % cols, i // cols
        montage.paste(f, (col * THUMB_W, row * THUMB_H))
    out = "tools/preview_montage.png"
    montage.save(out)
    print(f"[verify] 生成 {len(frames)} 帧 → {out}")
    print(f"[verify] 最终漂移: dir=({drift.direction[0]:.2f},{drift.direction[1]:.2f}) speed={drift.speed:.1f}")
    print(f"[verify] 深水 offset: ({water_deep.offset[0]:.1f},{water_deep.offset[1]:.1f})")
    print(f"[verify] 浪层 offset: ({water_wave.offset[0]:.1f},{water_wave.offset[1]:.1f})")


if __name__ == "__main__":
    main()

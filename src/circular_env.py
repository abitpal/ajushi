import gymnasium as gym
from gymnasium.envs.box2d.car_racing import CarRacing, BORDER, TRACK_WIDTH
import numpy as np
import math

class CircularCarRacing(CarRacing):
    def _create_track(self):
        """
        Generates a geometrically perfect oval track composed of two straights
        and two semicircles, ensuring a clean and reliable loop.
        """
        self.road = []
        self.road_poly = []

        # ==========================================================================
        # === THE DEFINITIVE FIX: Build the track from geometric primitives    ======
        # === (straights and semicircles) for 100% predictable results.      ======
        # ==========================================================================
        
        centerline = []
        STRAIGHT_LENGTH = 300
        TURN_RADIUS = 100
        TRACK_DETAIL = 40  # Points per turn/straight

        # Helper to create a straight line
        def create_straight(start, end, num_points):
            for i in range(num_points):
                t = i / (num_points - 1)
                x = start[0] * (1 - t) + end[0] * t
                y = start[1] * (1 - t) + end[1] * t
                centerline.append((x, y))

        # Helper to create a semicircle turn
        def create_turn(center, radius, start_angle, end_angle, num_points):
            for i in range(num_points):
                t = i / (num_points - 1)
                angle = start_angle * (1 - t) + end_angle * t
                x = center[0] + radius * math.cos(angle)
                y = center[1] + radius * math.sin(angle)
                centerline.append((x, y))

        # 1. Front Straight (going up)
        create_straight(start=(0, 0), end=(0, STRAIGHT_LENGTH), num_points=TRACK_DETAIL)

        # 2. Top Semicircle (180 degrees)
        create_turn(center=(TURN_RADIUS, STRAIGHT_LENGTH), radius=TURN_RADIUS, start_angle=math.pi, end_angle=0, num_points=TRACK_DETAIL * 2)

        # 3. Back Straight (going down)
        create_straight(start=(TURN_RADIUS * 2, STRAIGHT_LENGTH), end=(TURN_RADIUS * 2, 0), num_points=TRACK_DETAIL)

        # 4. Bottom Semicircle (180 degrees, closing the loop)
        create_turn(center=(TURN_RADIUS, 0), radius=TURN_RADIUS, start_angle=0, end_angle=-math.pi, num_points=TRACK_DETAIL * 2)


        track = []
        for i, (x, y) in enumerate(centerline):
            look_ahead = 5
            x_next, y_next = centerline[(i + look_ahead) % len(centerline)]
            dx, dy = x_next - x, y_next - y
            beta = math.atan2(dy, dx)
            alpha = 2 * math.pi * i / len(centerline)
            track.append((alpha, beta, x, y))

        # Re-center the track so the start is exactly at (0,0)
        x_offset, y_offset = track[0][2], track[0][3]
        final_track = []
        for i in range(len(track)):
            alpha, beta, x, y = track[i]
            final_track.append((alpha, beta, x - x_offset, y - y_offset))
        self.track = final_track
        
        # GUARANTEE the car spawns facing perfectly UP
        if len(self.track) > 0:
            alpha0, _, x0, y0 = self.track[0]
            self.track[0] = (alpha0, 0, x0, y0)
        
        self.start_alpha = 0

        # Detect borders
        border = [False] * len(self.track)
        BORDER_MIN_COUNT = 4
        # A simple way to add borders on turns for this geometric track
        for i in range(len(self.track)):
            # The turns are the second and fourth quarters of the track array
            is_on_turn1 = TRACK_DETAIL < i < TRACK_DETAIL * 3
            is_on_turn2 = TRACK_DETAIL * 4 < i < TRACK_DETAIL * 6
            if is_on_turn1 or is_on_turn2:
                border[i] = True

        for i in range(len(self.track)):
            alpha1, beta1, x1, y1 = self.track[i]
            alpha2, beta2, x2, y2 = self.track[(i - 1) % len(self.track)]

            if math.sqrt((x1-x2)**2 + (y1-y2)**2) < 0.1: continue

            perp1, perp2 = beta1 + math.pi / 2, beta2 + math.pi / 2
            road1_l = (x1 + TRACK_WIDTH * math.cos(perp1), y1 + TRACK_WIDTH * math.sin(perp1))
            road1_r = (x1 - TRACK_WIDTH * math.cos(perp1), y1 - TRACK_WIDTH * math.sin(perp1))
            road2_l = (x2 + TRACK_WIDTH * math.cos(perp2), y2 + TRACK_WIDTH * math.sin(perp2))
            road2_r = (x2 - TRACK_WIDTH * math.cos(perp2), y2 - TRACK_WIDTH * math.sin(perp2))
            
            self.fd_tile.shape.vertices = [road1_l, road1_r, road2_r, road2_l]
            t = self.world.CreateStaticBody(fixtures=self.fd_tile)
            t.userData = t
            t.color = self.road_color + 0.01 * (i % 3) * 255
            t.road_visited, t.road_friction, t.idx = False, 1.0, i
            t.fixtures[0].sensor = True
            self.road_poly.append(([road1_l, road1_r, road2_r, road2_l], t.color))
            self.road.append(t)

            if border[i]:
                side = 1
                b1_l = (x1 + side * TRACK_WIDTH * math.cos(perp1), y1 + side * TRACK_WIDTH * math.sin(perp1))
                b1_r = (x1 + side * (TRACK_WIDTH + BORDER) * math.cos(perp1), y1 + side * (TRACK_WIDTH + BORDER) * math.sin(perp1))
                b2_l = (x2 + side * TRACK_WIDTH * math.cos(perp2), y2 + side * TRACK_WIDTH * math.sin(perp2))
                b2_r = (x2 + side * (TRACK_WIDTH + BORDER) * math.cos(perp2), y2 + side * (TRACK_WIDTH + BORDER) * math.sin(perp2))
                self.road_poly.append(( [b1_l, b1_r, b2_r, b2_l], (255, 255, 255) if i % 2 == 0 else (255, 0, 0)))

        return True

try:
    gym.envs.registration.register(
        id='CircularCarRacing-v0',
        entry_point=__name__ + ':CircularCarRacing',
        max_episode_steps=2000,
    )
except gym.error.Error:
    pass


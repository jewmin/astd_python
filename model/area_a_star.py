# -*- coding: utf-8 -*-
# A*算法
from astar import AStar
import math


class AreaAStar(AStar):
    def __init__(self, area_map):
        self.m_listMap = area_map
        self.m_nWidth = len(area_map[0])
        self.m_nHeight = len(area_map)
        self.m_bIgnoreBarrier = False

    def set_map(self, area_map):
        self.m_listMap = area_map
        self.m_nWidth = len(area_map[0])
        self.m_nHeight = len(area_map)
        self.m_bIgnoreBarrier = False

    def ignore_barrier(self, ignore):
        self.m_bIgnoreBarrier = ignore

    def heuristic_cost_estimate(self, current, goal):
        (y1, x1) = current
        (y2, x2) = goal
        distance = math.hypot(x2 - x1, y2 - y1)
        return distance

    def distance_between(self, n1, n2):
        return 1

    def neighbors(self, node):
        y, x = node
        return [(ny, nx) for ny, nx in [(y, x - 1), (y, x + 1), (y - 1, x), (y + 1, x)] if 0 <= nx < self.m_nWidth and 0 <= ny < self.m_nHeight and (self.m_bIgnoreBarrier or self.m_listMap[ny][nx] == 1)]

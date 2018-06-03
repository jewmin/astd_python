# -*- coding: utf-8 -*-
# 世界任务
from logic.base_task import BaseTask
from logic.config import config


class WorldTask(BaseTask):
    def __init__(self):
        super(WorldTask, self).__init__()
        self.m_szName = "world"
        self.m_szReadable = "世界"

    def run(self):
        world_mgr = self.m_objServiceFactory.get_world_mgr()

        # 领取攻击令
        apply_att_token_config = config["world"]["apply_att_token"]
        if apply_att_token_config["enable"] and float(self.m_objUser.m_nAttToken) / float(self.m_objUser.m_nMaxAttToken) <= apply_att_token_config["proportion"]:
            world_mgr.get_transfer_info()

        # 屠城嘉奖
        tu_city_config = config["world"]["tu_city"]
        if tu_city_config["enable"]:
            world_mgr.get_tu_city_info()

        # 战绩
        score_config = config["world"]["score"]
        if score_config["enable"]:
            world_mgr.get_battle_ranking_info()
            # 上轮战绩排名奖励
            if world_mgr.m_bLastRankingReward and not world_mgr.m_bGetLast:
                world_mgr.get_battle_rank_reward()
            # 战绩宝箱
            while world_mgr.m_nBox > 0:
                world_mgr.open_score_box()
                world_mgr.m_nBox -= 1
            # 战绩奖励
            for rinfo in world_mgr.m_listScoreRewardInfo:
                if rinfo["canget"] == "1" and rinfo["get"] == "0":
                    world_mgr.get_battle_score_reward(rinfo)

        # 攻坚战
        nation_task_config = config["world"]["nation_task"]
        if nation_task_config["enable"]:
            world_mgr.get_nation_task_new_info()
            if world_mgr.m_nNationTaskStatus == 3:
                world_mgr.get_nation_task_new_reward()

        # 逃跑
        if self.m_objUser.m_nArrestState == 100:
            cd = self.m_objServiceFactory.get_city_mgr().escape()
            if cd is not None:
                return cd

        world_mgr.get_new_area()
        world_mgr.get_new_area_token()

        # 封地
        fengdi_config = config["world"]["fengdi"]
        if fengdi_config["enable"]:
            # 封地奖励
            if world_mgr.m_dictFengDi["完成"]:
                world_mgr.recv_fengdi_reward()
            # 封地生产
            if world_mgr.m_dictFengDi["剩余封地生产次数"] > 0 and len(world_mgr.m_setFengDi) > 0:
                for area in world_mgr.m_setFengDi:
                    if area["areaid"] == world_mgr.m_nSelfAreaId:
                        world_mgr.generate_big_g(area)
                        break

        # 城防恢复
        if world_mgr.m_nCityHpRecoverCd > 0:
            return world_mgr.m_nCityHpRecoverCd

        # 个人令
        use_token_config = config["world"]["use_token"]
        if use_token_config["enable"]:
            for token in world_mgr.m_listTokens:
                if token["tokenid"] in use_token_config["list"]:
                    world_mgr.use_token(token)

        # 间谍
        if world_mgr.m_nSpyAreaId == world_mgr.m_nSelfAreaId:
            world_mgr.look_area_city(world_mgr.m_dictAreas[world_mgr.m_nSpyAreaId])

        # 悬赏
        city_event_config = config["world"]["city_event"]
        if city_event_config["enable"]:
            # 悬赏星数奖励
            world_mgr.get_new_city_event_info()
            for pos, star_reward in enumerate(world_mgr.m_dictTarget["悬赏星数奖励"], 1):
                if star_reward["state"] == "1":
                    world_mgr.recv_new_city_event_star_reward(pos)

            # 悬赏目标
            if world_mgr.m_dictTarget["悬赏目标"] != 0:
                return self.attack_city_event_player(world_mgr.m_dictTarget["悬赏目标城池"], world_mgr.m_dictTarget["悬赏目标城区"], world_mgr.m_dictTarget["悬赏目标"])
            elif world_mgr.m_dictTarget["悬赏已完成"]:
                if world_mgr.m_dictTarget["悬赏剩余时间"] == 0:
                    world_mgr.deliver_new_city_event()
            elif world_mgr.m_dictTarget["悬赏剩余次数"] > 0 and len(world_mgr.m_dictTarget["悬赏任务列表"]) > 0:
                for task in world_mgr.m_dictTarget["悬赏任务列表"]:
                    if task["星级"] <= city_event_config["star"]:
                        world_mgr.accept_new_city_event(task)
                        break
                return self.immediate()

        return self.next_half_hour()

    def attack_city_event_player(self, area_id, scope_id, player_id):
        world_mgr = self.m_objServiceFactory.get_world_mgr()
        city_list = world_mgr.get_all_city(area_id, scope_id)
        for city in city_list:
            if int(city["playerid"]) == player_id:
                target_city = city
                break
        if target_city is None:
            return self.immediate()
        elif int(target_city["protectcd"]) > 0:
            return int(target_city["protectcd"])
        else:
            if world_mgr.attack_other_area_city(area_id, scope_id, target_city["cityid"]):
                return self.immediate()
            else:
                return self.one_minute()

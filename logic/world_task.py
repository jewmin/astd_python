# -*- coding: utf-8 -*-
# 世界任务
from logic.base_task import BaseTask
from logic.config import config


class WorldTask(BaseTask):
    def __init__(self):
        super(WorldTask, self).__init__()
        self.m_szName = "world"
        self.m_szReadable = "世界"
        self.m_dictTime = dict()
        self.m_WorldMgr = None
        self.m_CityMgr = None
        self.m_nTransferFailNum = 0

    def init(self):
        self.m_WorldMgr = self.m_objServiceFactory.get_world_mgr()
        self.m_CityMgr = self.m_objServiceFactory.get_city_mgr()

    def run(self):
        # 领取攻击令
        apply_att_token_config = config["world"]["apply_att_token"]
        if apply_att_token_config["enable"] and float(self.m_objUser.m_nAttToken) / float(self.m_objUser.m_nMaxAttToken) <= apply_att_token_config["proportion"]:
            self.m_WorldMgr.get_transfer_info()

        # 国家宝箱
        treasure_config = config["world"]["treasure"]
        if treasure_config["enable"] and float(self.m_objUser.m_nAttToken) / float(self.m_objUser.m_nMaxAttToken) <= treasure_config["proportion"]:
            self.m_WorldMgr.get_new_area_treasure_info()
            while self.m_WorldMgr.m_nTreasureNum > treasure_config["reserve"]:
                self.m_WorldMgr.draw_5_new_area_treasure()
                self.m_WorldMgr.m_nTreasureNum -= 5

        # 屠城嘉奖
        tu_city_config = config["world"]["tu_city"]
        if tu_city_config["enable"]:
            self.m_WorldMgr.get_tu_city_info()

        # 战绩
        score_config = config["world"]["score"]
        if score_config["enable"]:
            self.m_WorldMgr.get_battle_ranking_info()
            # 上轮战绩排名奖励
            if self.m_WorldMgr.m_bLastRankingReward and not self.m_WorldMgr.m_bGetLast:
                self.m_WorldMgr.get_battle_rank_reward()
            # 战绩宝箱
            while self.m_WorldMgr.m_nBox > 0:
                self.m_WorldMgr.open_score_box()
                self.m_WorldMgr.m_nBox -= 1
            # 战绩奖励
            for rinfo in self.m_WorldMgr.m_listScoreRewardInfo:
                if rinfo["canget"] == "1" and rinfo["get"] == "0":
                    self.m_WorldMgr.get_battle_score_reward(rinfo)

        # 攻坚战
        nation_task_config = config["world"]["nation_task"]
        if nation_task_config["enable"]:
            self.m_WorldMgr.get_nation_task_new_info()
            if self.m_WorldMgr.m_nNationTaskStatus == 3:
                self.m_WorldMgr.get_nation_task_new_reward()

        # 悬赏
        city_event_config = config["world"]["city_event"]
        if city_event_config["enable"]:
            self.m_WorldMgr.get_new_city_event_info()
            # 悬赏星数奖励
            for pos, star_reward in enumerate(self.m_WorldMgr.m_dictTarget["悬赏星数奖励"], 1):
                if star_reward["state"] == "1":
                    self.m_WorldMgr.recv_new_city_event_star_reward(pos)
            # 悬赏任务奖励
            if self.m_WorldMgr.m_dictTarget["悬赏已完成"] and self.m_WorldMgr.m_dictTarget["悬赏剩余时间"] == 0:
                self.m_WorldMgr.deliver_new_city_event()

        # 逃跑
        if self.m_objUser.m_nArrestState == 100:
            cd = self.m_CityMgr.escape()
            if cd is not None:
                self.m_WorldMgr.info("等待逃跑冷却时间：{}".format(
                    self.m_objServiceFactory.get_time_mgr().get_datetime_string(cd)))
                return cd

        self.m_WorldMgr.get_new_area()
        self.m_WorldMgr.get_new_area_token()

        # 封地奖励
        fengdi_config = config["world"]["fengdi"]
        if fengdi_config["enable"]:
            if self.m_WorldMgr.m_dictFengDi["完成"]:
                self.m_WorldMgr.recv_fengdi_reward()
            elif self.m_WorldMgr.m_dictFengDi["生产时间"] == 0 and self.m_WorldMgr.m_dictFengDi["剩余封地生产次数"] > 0:
                area = self.m_WorldMgr.m_dictId2Areas[self.m_WorldMgr.m_nSelfAreaId]
                if area.get("fengdiflag", "") != "" and area["nation"] == self.m_objUser.m_nNation:
                    self.m_WorldMgr.generate_big_g(area, fengdi_config["big"])

        # 城防恢复
        if self.m_WorldMgr.m_nCityHpRecoverCd > 0:
            self.m_WorldMgr.info("等待城防恢复时间：{}".format(
                self.m_objServiceFactory.get_time_mgr().get_datetime_string(self.m_WorldMgr.m_nCityHpRecoverCd)))
            return self.m_WorldMgr.m_nCityHpRecoverCd

        # 决斗
        self.do_duel()

        # 冷却时间
        if self.m_objUser.m_bTokenCdFlag and self.m_objUser.m_nTokenCd > 0:
            self.m_WorldMgr.info("等待军令冷却时间：{}".format(self.m_objServiceFactory.get_time_mgr().get_datetime_string(self.m_objUser.m_nTokenCd)))
            return self.m_objUser.m_nTokenCd

        # 攻击令
        attack_config = config["world"]["attack"]
        if self.m_objUser.m_nAttToken > 0:
            # 个人令
            use_token_config = config["world"]["use_token"]
            if use_token_config["enable"]:
                for token in self.m_WorldMgr.m_listTokens:
                    if token["tokenid"] in use_token_config["list"]:
                        self.m_WorldMgr.use_token(token)

            # 不在都城
            if attack_config["main_city"][self.m_objUser.m_nNation] != self.m_WorldMgr.m_nSelfAreaId:
                # 间谍
                if self.m_WorldMgr.m_nSpyAreaId > 0:
                    self.attack_spy(self.m_WorldMgr.m_nSpyAreaId)

                # 悬赏
                if city_event_config["enable"]:
                    self.m_WorldMgr.get_new_city_event_info()
                    # 悬赏目标
                    if self.m_WorldMgr.m_dictTarget["悬赏目标"] != 0:
                        self.attack_city_event_player(self.m_WorldMgr.m_dictTarget["悬赏目标城池"], self.m_WorldMgr.m_dictTarget["悬赏目标城区"], self.m_WorldMgr.m_dictTarget["悬赏目标"])

                # 搜索敌人
                if attack_config["enable"] and attack_config["main_city"][self.m_objUser.m_nNation] != self.m_WorldMgr.m_nSelfAreaId:
                    can_attack_area_list = self.attack_player(self.m_WorldMgr.m_nSelfAreaId)
                    for area in can_attack_area_list:
                        # 屠城
                        attack_num = 0
                        total_num = len(area["玩家列表"]) + len(area["NPC列表"]) + len(area["已被抓的玩家列表"]) + len(area["已被抓的NPC列表"])
                        attack_arrest = False
                        if tu_city_config["enable"] and area["屠城"] and self.m_WorldMgr.m_dictTuCity["冷却时间"] == 0 and self.m_WorldMgr.m_dictTuCity["剩余次数"] > 0:
                            if total_num <= tu_city_config["people_num"]:
                                self.m_WorldMgr.tu_city(area["城池"])
                                attack_arrest = True
                        attack_list = []
                        attack_list.extend(area["玩家列表"])
                        attack_list.extend(area["NPC列表"])
                        if attack_arrest:
                            attack_list.extend(area["已被抓的玩家列表"])
                            attack_list.extend(area["已被抓的NPC列表"])
                        for city in attack_list:
                            lost_times = 0
                            while True:
                                result, error, arrest_state, attack_back = self.attack_other_area_city(city["areaid"], city["scopeid"], city["cityid"])
                                if result is False:
                                    if error == "没有足够的攻击令":
                                        if attack_arrest:
                                            self.m_WorldMgr.get_transfer_info()
                                            while self.m_WorldMgr.m_nTreasureNum > treasure_config["arrest_reserve"]:
                                                self.m_WorldMgr.draw_5_new_area_treasure()
                                                self.m_WorldMgr.m_nTreasureNum -= 5
                                        if self.m_objUser.m_nAttToken <= 0:
                                            return self.immediate()
                                    elif error == "军令还没有冷却，请等待":
                                        return self.immediate()
                                    elif error == "你已被抓，请先逃跑":
                                        return self.immediate()
                                    elif error == "您当前正在组队征战中，不可以进行其他操作":
                                        return self.ten_minute()
                                    elif error == "该位置玩家发生了变动":
                                        attack_num += 1
                                        break
                                    elif error == "打不过敌人":
                                        lost_times += 1
                                        if lost_times >= attack_config["lost_times"]:
                                            break
                                    else:
                                        break
                                else:
                                    if self.m_WorldMgr.m_nSpyAreaId > 0:
                                        self.attack_spy(self.m_WorldMgr.m_nSpyAreaId)
                                    if attack_back:
                                        attack_num += 1
                                        break
                                    elif arrest_state and not attack_arrest:
                                        break
                        if attack_arrest and attack_num == total_num:
                            self.m_WorldMgr.info("完成屠城")
                            next_area = self.get_next_move_area(area["城池"])
                            if next_area is not None:
                                self.m_WorldMgr.cd_move_recover_confirm()
                                self.m_WorldMgr.transfer_in_new_area(next_area)
                                return self.immediate()

        # 悬赏
        if city_event_config["enable"]:
            self.m_WorldMgr.get_new_city_event_info()
            # 领取悬赏任务
            if not self.m_WorldMgr.m_dictTarget["悬赏已完成"] and self.m_WorldMgr.m_dictTarget["悬赏剩余次数"] > city_event_config["reserve"] and len(self.m_WorldMgr.m_dictTarget["悬赏任务列表"]) > 0:
                for task in self.m_WorldMgr.m_dictTarget["悬赏任务列表"]:
                    if task["星级"] <= city_event_config["star"]:
                        self.m_WorldMgr.accept_new_city_event(task)
                        break

        # 决斗
        area_list = self.m_WorldMgr.get_neighbors_area(self.m_WorldMgr.m_nSelfAreaId)
        for area in area_list:
            if area["areaname"] in attack_config["exculde"] and area["areaid"] != attack_config["main_city"][self.m_objUser.m_nNation]:
                self.duel(area, attack_config["diff_level"], attack_config["duel_city_hp_limit"])
                break

        # 移动cd
        if self.m_WorldMgr.m_nTransferCd > 0:
            if self.m_WorldMgr.m_nFreeClearMoveTime > attack_config["reserve_transfer_cd_clear_num"]:
                self.m_WorldMgr.cd_move_recover_confirm()
            else:
                return self.m_WorldMgr.m_nTransferCd

        # 集结
        if self.m_WorldMgr.m_szNationTaskAreaName != "":
            self.m_WorldMgr.info("发现集结城池[{}]".format(self.m_WorldMgr.m_szNationTaskAreaName))
            next_area = self.get_next_move_area(self.m_WorldMgr.m_szNationTaskAreaName)
            if next_area is not None:
                self.m_WorldMgr.transfer_in_new_area(next_area)
                return self.immediate()

        # 封地生产
        if fengdi_config["enable"]:
            if self.m_WorldMgr.m_dictFengDi["生产时间"] == 0 and self.m_WorldMgr.m_dictFengDi["剩余封地生产次数"] > 0:
                if len(self.m_WorldMgr.m_dictFengDiAreas) > 0:
                    for area in self.m_WorldMgr.m_dictFengDiAreas.itervalues():
                        if int(area["fengdicd"]) >= fengdi_config["cd"]:
                            next_area = self.get_next_move_area(area["areaname"])
                            if next_area is not None:
                                self.m_WorldMgr.transfer_in_new_area(next_area)
                                return self.immediate()
            elif self.m_WorldMgr.m_dictFengDi["生产时间"] > 0:
                return self.one_minute()

        # 间谍
        if self.m_WorldMgr.m_nSpyAreaId > 0:
            next_area = self.get_next_move_area(self.m_WorldMgr.m_nSpyAreaId)
            if next_area is not None:
                self.m_WorldMgr.transfer_in_new_area(next_area)
                return self.immediate()

        # 敌方都城附近
        near_main_city_area_id_list = attack_config["near_main_city"][self.m_objUser.m_nNation]
        for area_id in near_main_city_area_id_list:
            if area_id == self.m_WorldMgr.m_nSelfAreaId:
                if self.m_objUser.m_nAttToken == 0 and not self.can_duel(attack_config["duel_city_hp_limit"]):
                    return self.next_half_hour()
                return self.immediate()
        for area_id in near_main_city_area_id_list:
            next_area = self.get_next_move_area(area_id)
            if next_area is not None:
                self.m_WorldMgr.transfer_in_new_area(next_area)
                return self.immediate()

        # 取一个方向前进
        self.m_WorldMgr.m_AStar.ignore_barrier(True)
        for area_id in near_main_city_area_id_list:
            next_area = self.get_next_move_area(area_id)
            if next_area is not None:
                if self.m_WorldMgr.transfer_in_new_area(next_area):
                    return self.immediate()
                else:
                    self.m_nTransferFailNum += 1
                if self.m_nTransferFailNum >= attack_config["transfer_fail_num"]:
                    self.m_nTransferFailNum = 0
                    return self.next_hour()
                return self.one_minute()

        return self.one_minute()

    def attack_city_event_player(self, area_id, scope_id, player_id):
        city_list = self.m_WorldMgr.get_all_city(area_id, scope_id)
        if city_list is None:
            return
        for city in city_list:
            if city["playerid"] == str(player_id):
                if city["protectcd"] == "0":
                    self.attack_other_area_city(area_id, scope_id, city["cityid"])
                break

    def attack_spy(self, area_id):
        area_list = self.m_WorldMgr.get_neighbors_area(area_id, True)
        for area in area_list:
            if area_id == area["areaid"]:
                self.m_WorldMgr.m_nSpyAreaId = 0
                for i in xrange(1, 100):
                    city_list = self.m_WorldMgr.get_all_city(area_id, i)
                    if city_list is None:
                        break
                    for city in city_list:
                        if city["myspy"] == "0":
                            continue
                        self.attack_other_area_city(area_id, i, city["cityid"])
                break

    # cityid areaid scopeid playerid playername citytype citylevel myspy protectcd arreststate nation inpk
    def attack_player(self, area_id):
        area_list = self.m_WorldMgr.get_neighbors_area(area_id, True, config["world"]["attack"]["exculde"])
        can_attack_area_list = []
        for area in area_list:
            if area["nation"] == self.m_objUser.m_nNation:
                can_tu_city = False
            else:
                can_tu_city = True
            can_attack_player = []
            can_attack_npc = []
            arrest_player = []
            arrest_npc = []
            for i in xrange(1, 100):
                city_list = self.m_WorldMgr.get_all_city(area["areaid"], i)
                if city_list is None:
                    break
                for city in city_list:
                    if int(city["nation"]) == self.m_objUser.m_nNation:
                        continue
                    if city["protectcd"] != "0":
                        can_tu_city = False
                        continue
                    if city["citytype"] == "1":
                        if int(city["citylevel"]) > self.m_objUser.m_nLevel:
                            can_tu_city = False
                        elif city["inpk"] != "0":
                            can_tu_city = False
                        elif city["arreststate"] == "0":
                            can_attack_player.append(city)
                        else:
                            arrest_player.append(city)
                    elif city["arreststate"] == "0":
                        can_attack_npc.append(city)
                    else:
                        arrest_npc.append(city)
            can_attack_area_list.append({"城池": area["areaid"], "屠城": can_tu_city, "玩家列表": can_attack_player, "NPC列表": can_attack_npc, "已被抓的玩家列表": arrest_player, "已被抓的NPC列表": arrest_npc})
        return can_attack_area_list

    def can_duel(self, duel_city_hp_limit):
        return self.m_objUser.m_nCityHp > duel_city_hp_limit and self.m_WorldMgr.m_dictDaoJu["诱敌锦囊"] > 0 and self.m_WorldMgr.m_dictDaoJu["决斗战旗"] > 0

    def duel(self, area, diff_level, duel_city_hp_limit):
        scope_id = 1
        while self.can_duel(duel_city_hp_limit):
            city_list = self.m_WorldMgr.get_all_city(area["areaid"], scope_id)
            if city_list is None:
                break
            for city in city_list:
                if not self.can_duel(duel_city_hp_limit):
                    break
                level = int(city["citylevel"])
                if 0 <= self.m_objUser.m_nLevel - level <= diff_level:
                    result, info, error_code = self.m_WorldMgr.use_world_daoju(city)
                    if result:
                        self.m_WorldMgr.m_dictDaoJu["诱敌锦囊"] -= 1
                        duel_city_list = self.m_WorldMgr.get_all_city(info["城池"], info["区域"])
                        if duel_city_list is None:
                            return
                        for duel_city in duel_city_list:
                            if duel_city["playerid"] == str(info["玩家"]):
                                result, info, error_code = self.m_WorldMgr.use_world_daoju(duel_city, True)
                                if result:
                                    self.m_WorldMgr.m_dictDaoJu["决斗战旗"] -= 1
                                    self.do_duel()
                                    break
                                else:
                                    return
                    elif "当前城池正在补充城防" in error_code or "该玩家今日诱敌次数已满" in error_code:
                        continue
                    else:
                        return
            scope_id += 1

    def do_duel(self):
        while True:
            pk_info = self.m_WorldMgr.get_pk_info()
            if pk_info is not None and pk_info["阶段"] == 1:
                self.m_WorldMgr.info("{}({}/{}) VS {}({}/{})".format(
                    pk_info["攻"]["玩家"], pk_info["攻"]["城防"], pk_info["攻"]["最大城防"],
                    pk_info["防"]["玩家"], pk_info["防"]["城防"], pk_info["防"]["最大城防"]))
                self.attack_other_area_city(pk_info["目标"]["城池"], pk_info["目标"]["区域"], pk_info["目标"]["城市"])
            else:
                break

    def attack_other_area_city(self, area_id, scope_id, city_id):
        self.m_CityMgr.draught(0.3)
        return self.m_WorldMgr.attack_other_area_city(area_id, scope_id, city_id)

    def get_next_move_area(self, area):
        current_area = self.m_WorldMgr.m_dictId2Areas[self.m_WorldMgr.m_nSelfAreaId]
        goal_area = None

        if isinstance(area, str):
            goal_area = self.m_WorldMgr.m_dictName2Areas[area]
        elif isinstance(area, int):
            goal_area = self.m_WorldMgr.m_dictId2Areas[area]
        elif isinstance(area, tuple):
            goal_area = self.m_WorldMgr.m_dictXY2Areas[area[0]][area[1]]

        if goal_area is None or current_area is None:
            self.m_WorldMgr.info("area type is {}, not str or int or tuple".format(type(area)))
            return None

        if current_area["areaid"] == goal_area["areaid"]:
            self.m_WorldMgr.info("已在城池[{}]".format(current_area["areaname"]))
            return None

        coordinate = map(int, current_area["coordinate"].split(","))
        current_y, current_x = coordinate[0] - 1, coordinate[1] - 1
        coordinate = map(int, goal_area["coordinate"].split(","))
        goal_y, goal_x = coordinate[0] - 1, coordinate[1] - 1
        paths = self.m_WorldMgr.m_AStar.astar((current_y, current_x), (goal_y, goal_x))
        if paths is None:
            # self.m_WorldMgr.info("从城池[{}] 无法到达 城池[{}]".format(current_area["areaname"], goal_area["areaname"]))
            return None

        path_list = list(paths)
        path_list.pop(0)
        msg = ""
        if self.m_WorldMgr.m_AStar.m_bIgnoreBarrier:
            msg += "忽略国家限制，"
        msg += "从城池[{}] 到达 城池[{}]，需要经过城池".format(current_area["areaname"], goal_area["areaname"])
        for path in path_list:
            after_area = self.m_WorldMgr.m_dictXY2Areas[path[0]][path[1]]
            msg += " [{}]".format(after_area["areaname"])
        self.m_WorldMgr.info(msg)
        return self.m_WorldMgr.m_dictXY2Areas[path_list[0][0]][path_list[0][1]]

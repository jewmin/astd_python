# -*- coding: utf-8 -*-
# 世界管理
from manager.base_mgr import BaseMgr
from model.reward_info import RewardInfo


class WorldMgr(BaseMgr):
    def __init__(self, time_mgr, service_factory, user, index):
        super(WorldMgr, self).__init__(time_mgr, service_factory, user, index)
        self.m_dictAreas = dict()  # 城池
        self.m_setFengDi = set()  # 封地集合
        self.m_dictFengDi = dict()  # 封地
        self.m_dictDaoJu = dict()  # 道具
        self.m_listTokens = list()  # 个人令 -1:未解锁,0:已使用,1:建造令,2:破坏令,3:,4:鼓舞令,5:诽谤令,6:,7:窃取令,8:战绩令,9:横扫令
        self.m_dictTuCity = dict()  # 屠城
        self.m_listScoreRewardInfo = list()  # 战绩奖励
        self.m_dictTarget = dict()  # 悬赏目标
        self.m_nTreasureNum = 0  # 国家宝箱
        self.m_nCityHpRecoverCd = 0  # 城防恢复冷却时间
        self.m_nFreeClearMoveTime = 0  # 免费清除迁移冷却时间次数
        self.m_nTransferCd = 0  # 迁移冷却时间
        self.m_nBox = 0  # 战绩宝箱
        self.m_bLastRankingReward = False  # 有没有上轮排名奖励
        self.m_bGetLast = False  # 领没领上轮排名奖励
        self.m_nSelfAreaId = 0  # 本人所在城池
        self.m_nSpyAreaId = 0  # 间谍所在城池
        self.m_nNationTaskAreaId = 0  # 攻坚战集结城池
        self.m_nNationTaskStatus = 0  # 攻坚战状态 3:完成

    def set_feng_di(self, feng_di_info):
        self.m_dictFengDi.clear()
        self.m_dictFengDi["剩余封地生产次数"] = int(feng_di_info.get("remainnum", "0"))
        self.m_dictFengDi["免费借兵次数"] = int(feng_di_info["freejiebinnum"])
        self.m_dictFengDi["金币借兵消耗"] = int(feng_di_info["jiebincost"])
        self.m_dictFengDi["完成"] = feng_di_info.get("finish", "0") == "1"

    def set_dao_ju(self, dao_ju_info):
        self.m_dictDaoJu.clear()
        self.m_dictDaoJu["决斗战旗"] = int(dao_ju_info["flagnum"])
        self.m_dictDaoJu["诱敌锦囊"] = int(dao_ju_info["jinnum"])

    def set_tu_city(self, tu_city_info):
        self.m_dictTuCity.clear()
        self.m_dictTuCity["剩余次数"] = int(tu_city_info["remaintutimes"])
        self.m_dictTuCity["冷却时间"] = int(tu_city_info["tucd"])

    def get_new_area(self):
        url = "/root/world!getNewArea.action"
        result = self.get_protocol_mgr().get_xml(url, "世界")
        if result and result.m_bSucceed:
            self.set_feng_di(result.m_objResult["fengdi"])
            self.set_dao_ju(result.m_objResult["daoju"])
            self.m_nTreasureNum = int(result.m_objResult["treasurenum"])
            self.m_nCityHpRecoverCd = int(result.m_objResult["cityhprecovercd"])
            self.m_nFreeClearMoveTime = int(float(result.m_objResult["freeclearmovetime"]))
            self.m_nTransferCd = int(result.m_objResult["tranfercd"])
            self.m_dictTarget["悬赏目标"] = int(result.m_objResult.get("targetid", "0"))
            self.m_dictTarget["悬赏目标城池"] = int(result.m_objResult.get("targetareaid", "0"))
            self.m_dictTarget["悬赏目标城区"] = int(result.m_objResult.get("targetscopeid", "0"))
            self.m_setFengDi.clear()
            self.m_dictAreas.clear()
            for area in result.m_objResult["newarea"]:
                if "areaid" in area:
                    area["areaid"] = int(area["areaid"])
                    area["nation"] = int(area["nation"])
                    area["scopecount"] = int(area["scopecount"])
                    if area.get("isselfarea", "0") == "1":
                        self.m_nSelfAreaId = area["areaid"]
                    if area.get("ziyuan", "0") == "100":
                        self.m_nSpyAreaId = area["areaid"]
                    if area.get("fengdiflag", "0") == "1" and area["nation"] == self.m_objUser.m_nNation:
                        self.m_setFengDi.add(area)
                    self.m_dictAreas[area["areaid"]] = area

    def look_area_city(self, area):
        url = "/root/world!lookAreaCity.action"
        data = {"areaId": area["areaid"]}
        result = self.get_protocol_mgr().post_xml(url, data, "城池")
        if result and result.m_bSucceed:
            spy_num = int(result.m_objResult["area"].get("spynum", "0"))
            if spy_num > 0:
                self.info("搜索间谍，找到{}个间谍".format(spy_num))
                for i in xrange(area["scopecount"]):
                    pass

    def get_transfer_info(self):
        url = "/root/world!getTranferInfo.action"
        result = self.get_protocol_mgr().get_xml(url, "迁移")
        if result and result.m_bSucceed:
            if result.m_objResult["canget"] == "1":
                self.get_transfer_token()

    def get_transfer_token(self):
        url = "/root/world!getTransferToken.action"
        result = self.get_protocol_mgr().get_xml(url, "领取攻击令")
        if result and result.m_bSucceed:
            self.info("领取{}攻击令".format(result.m_objResult["token"]))

    def get_tu_city_info(self):
        url = "/root/world!getTuCityInfo.action"
        result = self.get_protocol_mgr().get_xml(url, "屠城嘉奖")
        if result and result.m_bSucceed:
            maxrecvednum = int(result.m_objResult.get("maxrecvednum", "0"))
            recvednum = int(result.m_objResult.get("recvednum", "0"))
            if recvednum < maxrecvednum and "info" in result.m_objResult:
                for info in result.m_objResult["info"]:
                    self.get_tu_city_reward(info["playerid"], info["areaid"])

    def get_tu_city_reward(self, player_id, area_id):
        url = "/root/world!getTuCityReward.action"
        data = {"playerId": player_id, "areaId": area_id}
        result = self.get_protocol_mgr().post_xml(url, data, "搜刮屠城嘉奖")
        if result and result.m_bSucceed:
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["rewardinfo"])
            self.info("搜刮屠城嘉奖，获得{}".format(reward_info))

    def tu_city(self, area_id):
        url = "/root/world!tuCity.action"
        data = {"areaId": area_id}
        result = self.get_protocol_mgr().post_xml(url, data, "屠城")
        if result and result.m_bSucceed:
            self.info("屠城，获得{}宝石".format(result.m_objResult["baoshi"]))

    def get_new_area_token(self):
        url = "/root/world!getNewAreaToken.action"
        result = self.get_protocol_mgr().get_xml(url, "个人令")
        if result and result.m_bSucceed:
            self.m_listTokens = result.m_objResult["tokenlist"]
            self.set_tu_city(result.m_objResult["tucity"])

    def use_token(self, token):
        if token["tokenid"] == "1":
            self.use_constuct_token(token)
        elif token["tokenid"] == "4":
            self.use_inspire_token(token)
        elif token["tokenid"] == "8":
            self.use_score_token(token)
        else:
            self.warning("未知个人令：{}_{}_{}".format(token["tokenid"], token["name"], token["level"]))

    def use_constuct_token(self, token):
        url = "/root/world!useConstuctToken.action"
        data = {"newTokenId": token["id"]}
        result = self.get_protocol_mgr().post_xml(url, data, "使用建造令")
        if result and result.m_bSucceed:
            self.info("使用建造令lv.{}，城防+{}".format(result.m_objResult["tokenlevel"], result.m_objResult["effect"]))

    def use_score_token(self, token):
        url = "/root/world!useScoreToken.action"
        data = {"newTokenId": token["id"]}
        result = self.get_protocol_mgr().post_xml(url, data, "使用战绩令")
        if result and result.m_bSucceed:
            self.info("使用战绩令lv.{}".format(result.m_objResult["tokenlevel"]))

    def use_inspire_token(self, token):
        url = "/root/world!useInspireToken.action"
        data = {"newTokenId": token["id"]}
        result = self.get_protocol_mgr().post_xml(url, data, "使用鼓舞令")
        if result and result.m_bSucceed:
            self.info("使用鼓舞令lv.{}".format(result.m_objResult["tokenlevel"]))

    def get_battle_ranking_info(self):
        url = "/root/world!getBattleRankingInfo.action"
        result = self.get_protocol_mgr().get_xml(url, "战绩")
        if result and result.m_bSucceed:
            self.m_nBox = int(result.m_objResult["box"])
            self.m_bLastRankingReward = result.m_objResult["lastrankingreward"] != "0"
            self.m_bGetLast = result.m_objResult["getlast"] == "1"
            self.m_listScoreRewardInfo = result.m_objResult["scorerewardinfo"]["rinfo"]

    def get_battle_score_reward(self, rinfo):
        url = "/root/world!getBattleScoreReward.action"
        data = {"pos": rinfo["id"]}
        result = self.get_protocol_mgr().post_xml(url, data, "领取战绩奖励")
        if result and result.m_bSucceed:
            self.info("领取战绩奖励，获得{}宝石，{}宝箱".format(result.m_objResult["baoshi"], result.m_objResult.get("box", "0")))

    def open_score_box(self):
        url = "/root/world!openScoreBox.action"
        result = self.get_protocol_mgr().get_xml(url, "打开战绩宝箱")
        if result and result.m_bSucceed:
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["rewardinfo"])
            self.info("打开战绩宝箱，获得{}".format(reward_info))

    def get_battle_rank_reward(self):
        url = "/root/world!getBattleRankReward.action"
        result = self.get_protocol_mgr().get_xml(url, "领取上轮战绩排名奖励")
        if result and result.m_bSucceed:
            self.info("领取上轮战绩排名奖励，获得{}宝石".format(result.m_objResult["baoshi"]))

    def recv_fengdi_reward(self):
        url = "/root/world!recvFengdiReward.action"
        result = self.get_protocol_mgr().get_xml(url, "领取封地奖励")
        if result and result.m_bSucceed:
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["rewardinfo"])
            self.info("领取封地奖励，获得{}".format(reward_info))
            self.set_feng_di(result.m_objResult["fengdi"])

    def generate_big_g(self, area):
        url = "/root/world!generateBigG.action"
        data = {"areaId": area["areaid"]}
        result = self.get_protocol_mgr().post_xml(url, data, "封地资源列表")
        if result and result.m_bSucceed:
            pass

    def get_nation_task_new_info(self):
        url = "/root/nation!getNationTaskNewInfo.action"
        result = self.get_protocol_mgr().get_xml(url, "攻坚战")
        if result and result.m_bSucceed:
            self.m_nNationTaskStatus = int(result.m_objResult["status"])

    def get_nation_task_new_reward(self):
        url = "/root/nation!getNationTaskNewReward.action"
        result = self.get_protocol_mgr().get_xml(url, "领取攻坚战奖励")
        if result and result.m_bSucceed:
            self.info("领取攻坚战奖励，获得{}个国家宝箱".format(result.m_objResult["box"]))

    def get_new_city_event_info(self):
        url = "/root/world!getNewCityEventInfo.action"
        result = self.get_protocol_mgr().get_xml(url, "悬赏")
        if result and result.m_bSucceed:
            self.m_dictTarget["悬赏任务列表"] = list()
            tasks = result.m_objResult["taskstr"].split(",")
            for pos, task in enumerate(tasks, 1):
                if len(task) > 0:
                    content = map(int, task.split(":"))
                    if content[1] == 0:
                        self.m_dictTarget["悬赏任务列表"].append({"位置": pos, "星级": content[0]})
            self.m_dictTarget["悬赏任务列表"] = sorted(self.m_dictTarget["悬赏任务列表"], key=lambda obj: obj["星级"], reverse=True)
            self.m_dictTarget["悬赏星数奖励"] = result.m_objResult["starreward"]
            self.m_dictTarget["悬赏剩余次数"] = int(result.m_objResult["remaintimes"])
            self.m_dictTarget["悬赏剩余时间"] = int(result.m_objResult.get("taskremaintime", "0"))
            self.m_dictTarget["悬赏已完成"] = result.m_objResult.get("taskstate", "0") == "1"

    def recv_new_city_event_star_reward(self, pos):
        url = "/root/world!recvNewCityEventStarReward.action"
        data = {"pos": pos}
        result = self.get_protocol_mgr().post_xml(url, data, "领取悬赏星数奖励")
        if result and result.m_bSucceed:
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["rewardinfo"])
            self.info("领取悬赏星数奖励，获得{}".format(reward_info))

    def accept_new_city_event(self, task):
        url = "/root/world!acceptNewCityEvent.action"
        data = {"pos": task["位置"]}
        result = self.get_protocol_mgr().post_xml(url, data, "领取悬赏任务")
        if result and result.m_bSucceed:
            self.info("领取{}星悬赏任务".format(task["星级"]))

    def deliver_new_city_event(self):
        url = "/root/world!deliverNewCityEvent.action"
        result = self.get_protocol_mgr().get_xml(url, "领取悬赏奖励")
        if result and result.m_bSucceed:
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["rewardinfo"])
            self.info("领取悬赏奖励，获得{}".format(reward_info))

    def get_all_city(self, area_id, scope_id):
        url = "/root/area!getAllCity.action"
        data = {"areaId": area_id, "scopeId": scope_id}
        result = self.get_protocol_mgr().post_xml(url, data, "查看城区")
        if result and result.m_bSucceed:
            city_list = result.m_objResult["city"]
            return city_list
        else:
            return list()

    def attack_other_area_city(self, area_id, scope_id, city_id):
        url = "/root/world!attackOtherAreaCity.action"
        data = {"areaId": area_id, "scopeId": scope_id, "cityId": city_id}
        result = self.get_protocol_mgr().post_xml(url, data, "攻击敌人")
        if result and result.m_bSucceed:
            if "battlereport" in result.m_objResult:
                de = {"名称": result.m_objResult["defender"]["playername"], "等级": result.m_objResult["defender"]["playerlevel"]}
                report = {
                    "战绩": result.m_objResult["battlereport"]["attscore"],
                    "消息": result.m_objResult["battlereport"]["message"],
                    "城防": [result.m_objResult["battlereport"]["attcityhpchange"], result.m_objResult["battlereport"]["defcityhpchange"]],
                    "胜负": "胜利" if result.m_objResult["battlereport"]["winside"] == "1" else "失败",
                }
            else:
                de = {"名称": "禁卫军", "等级": self.m_objUser.m_nLevel}
                if result.m_objResult["myspy"] != "0":
                    de["名称"] = "间谍"
                elif result.m_objResult["defender"]["playertype"] == "3":
                    de["名称"] = "守备军"
                report = {
                    "战绩": result.m_objResult["attscore"],
                    "消息": "",
                    "城防": [result.m_objResult["attcityhpchange"], result.m_objResult["defcityhpchange"]],
                    "胜负": "胜利",
                }
            self.info("您攻打{}, {}, {}获得战绩{}, 您/敌({}级)城防减少{}/{}".format(de["名称"], report["胜负"], report["消息"], report["战绩"], de["等级"], report["城防"][0], report["城防"][1]))
            return True
        else:
            self.warning("攻击敌人失败：{}".format(result.m_szError))
            return False

# -*- coding: utf-8 -*-
# 城池管理
from manager.base_mgr import BaseMgr
from model.enum.activity_type import ActivityType
from model.reward_info import RewardInfo
from model.general_tower import GeneralTower
from model.global_func import GlobalFunc
from manager.time_mgr import TimeMgr


class CityMgr(BaseMgr):
    def __init__(self, time_mgr, service_factory, user, index):
        super(CityMgr, self).__init__(time_mgr, service_factory, user, index)

    def get_main_city(self):
        url = "/root/mainCity.action"
        result = self.get_protocol_mgr().get_xml(url, "主城信息")
        if result and result.m_bSucceed:
            self.m_objUser.m_nRemainSeniorSlaves = int(result.m_objResult.get("remainseniorslaves", "0"))
            self.m_objUser.m_bCanVisit = result.m_objResult.get("canvisit", "0") == "1"
            self.m_objUser.m_bNewTechnology = result.m_objResult.get("newtechnology", "0") == "1"
            self.m_objUser.m_bWarChariot = result.m_objResult.get("warchariot", "0") == "1"
            self.m_objUser.m_nRightCd = int(result.m_objResult.get("rightcd", "0"))
            self.m_objUser.m_nRightNum = int(result.m_objResult.get("rightnum", "0"))
            self.set_activities(self.m_objUser, result.m_objResult)
            self.m_objUser.set_main_city_dto(result.m_objResult.get("maincitydto", []))
            self.m_objUser.set_constructor_dto(result.m_objResult.get("constructordto", []))
            self.m_objUser.set_mo_zi_building(result.m_objResult.get("mozibuilding", []))

    def upgrade_level(self, main_city_dto):
        url = "/root/mainCity!upgradeLevel.action"
        data = {"player_BuildingId": main_city_dto.id}
        result = self.get_protocol_mgr().post_xml(url, data, "升级建筑")
        if result and result.m_bSucceed:
            self.info("花费{}银币，升级建筑[{}]".format(main_city_dto.nextcopper, main_city_dto.buildname))

    @staticmethod
    def set_activities(user, dict_activities_info):
        if dict_activities_info.get("hasarchevent", "0") == "1":
            user.m_dictActivities[ActivityType.HasArchEvent] = True
        if dict_activities_info.get("weekendgift", "0") == "1":
            user.m_dictActivities[ActivityType.WeekendGift] = True
        if dict_activities_info.get("shenhuo", "0") == "1":
            user.m_dictActivities[ActivityType.ShenHuo] = True
        if dict_activities_info.get("baishen", "0") == "1":
            user.m_dictActivities[ActivityType.BaiShen] = True
        if dict_activities_info.get("yang", "0") == "1":
            user.m_dictActivities[ActivityType.Yang] = True
        if dict_activities_info.get("offlineevent", "0") == "1":
            user.m_dictActivities[ActivityType.OfflineEvent] = True
        if dict_activities_info.get("arrestevent", "0") == "1":
            user.m_dictActivities[ActivityType.ArrestEvent] = True
        if dict_activities_info.get("goldticketevent", "0") == "1":
            user.m_dictActivities[ActivityType.GoldTicketEvent] = True
        if dict_activities_info.get("yuebingevent", "0") == "1":
            user.m_dictActivities[ActivityType.YueBingEvent] = True
        if dict_activities_info.get("boatevent", "0") == "1":
            user.m_dictActivities[ActivityType.BoatEvent] = True
        if dict_activities_info.get("buffevent", "0") == "1":
            user.m_dictActivities[ActivityType.BuffEvent] = True
        if dict_activities_info.get("cuilianevent", "0") == "1":
            user.m_dictActivities[ActivityType.CuiLianEvent] = True
        if dict_activities_info.get("payhongbaoevent", "0") == "1":
            user.m_dictActivities[ActivityType.PayHongBaoEvent] = True
        if dict_activities_info.get("bgevent", "0") == "1":
            user.m_dictActivities[ActivityType.BGEvent] = True
        if dict_activities_info.get("qingmingevent", "0") == "1":
            user.m_dictActivities[ActivityType.QingMingEvent] = True
        if dict_activities_info.get("duanwuevent", "0") == "1":
            user.m_dictActivities[ActivityType.DuanWuEvent] = True
        if dict_activities_info.get("moongeneralevent", "0") == "1":
            user.m_dictActivities[ActivityType.MoonGeneralEvent] = True
        if dict_activities_info.get("trainingevent", "0") == "1":
            user.m_dictActivities[ActivityType.TrainingEvent] = True
        if dict_activities_info.get("snowtradingevent", "0") == "1":
            user.m_dictActivities[ActivityType.SnowTradingEvent] = True
        if dict_activities_info.get("bombnianevent", "0") == "1":
            user.m_dictActivities[ActivityType.BombNianEvent] = True
        if dict_activities_info.get("borrowingarrowsevent", "0") == "1":
            user.m_dictActivities[ActivityType.BorrowingArrowsEvent] = True
        if dict_activities_info.get("paradeevent", "0") == "1":
            user.m_dictActivities[ActivityType.ParadeEvent] = True
        if dict_activities_info.get("towerstage", "0") == "1":
            user.m_dictActivities[ActivityType.TowerStage] = True
        if dict_activities_info.get("moontowerevent", "0") == "1":
            user.m_dictActivities[ActivityType.MoonTowerEvent] = True
        if dict_activities_info.get("goldboxevent", "-1") == "0":
            user.m_dictActivities[ActivityType.GoldBoxEvent] = True
        if dict_activities_info.get("nationdaygoldboxevent", "0") == "1":
            user.m_dictActivities[ActivityType.NationDayGoldBoxEvent] = True
        if dict_activities_info.get("hasdaytreasuregame", "0") == "1":
            user.m_dictActivities[ActivityType.HasDayTreasureGame] = True
        if dict_activities_info.get("hastroopfeedback", "0") == "1":
            user.m_dictActivities[ActivityType.HasTroopFeedback] = True
        if dict_activities_info.get("hascakeevent", "false") == "true":
            user.m_dictActivities[ActivityType.HasCakeEvent] = True
        if dict_activities_info.get("hasnationdayevent", "0") == "1":
            user.m_dictActivities[ActivityType.HasNationDayEvent] = True
        if dict_activities_info.get("hasjailevent", "0") == "1":
            user.m_dictActivities[ActivityType.HasJailEvent] = True
        if dict_activities_info.get("showkfyz", "0") != "0":
            user.m_dictActivities[ActivityType.ShowKfYZ] = True
        if dict_activities_info.get("showkfwd", "0") != "0":
            user.m_dictActivities[ActivityType.ShowKfWD] = True
        if dict_activities_info.get("showkfpvp", "0") != "0":
            user.m_dictActivities[ActivityType.ShowKfPVP] = True
        if dict_activities_info.get("ringevent", "0") == "1":
            user.m_dictActivities[ActivityType.RingEvent] = True
        if dict_activities_info.get("feteevent", "0") == "1":
            user.m_dictActivities[ActivityType.FeteEvent] = True
        if dict_activities_info.get("superfanpai", "0") == "1":
            user.m_dictActivities[ActivityType.SuperFanPai] = True
        if dict_activities_info.get("yuandanqifu", "0") == "1":
            user.m_dictActivities[ActivityType.YuanDanQiFu] = True
        if dict_activities_info.get("doubleelevenevent", "0") == "1":
            user.m_dictActivities[ActivityType.DoubleElevenEvent] = True
        if dict_activities_info.get("goldgifttype", "0") == "2":
            user.m_dictActivities[ActivityType.GoldGiftType] = True
        if dict_activities_info.get("eatmooncaketevent", "0") == "1":
            user.m_dictActivities[ActivityType.EatMoonCakeEvent] = True
        if dict_activities_info.get("springfestivalwishevent", "0") == "1":
            user.m_dictActivities[ActivityType.SpringFestivalWishEvent] = True
        if dict_activities_info.get("memoryevent", "0") == "1":
            user.m_dictActivities[ActivityType.MemoryEvent] = True

    def get_update_reward(self):
        url = "/root/mainCity!getUpdateReward.action"
        result = self.get_protocol_mgr().get_xml(url, "领取版本更新奖励")
        if result and result.m_bSucceed:
            self.m_objUser.m_bHasVersionGift = False

    def get_per_day_reward(self):
        url = "/root/mainCity!getPerDayReward.action"
        result = self.get_protocol_mgr().get_xml(url, "试试手气")
        if result and result.m_bSucceed:
            self.m_objUser.m_bHasPerDayReward = False
            gold = result.m_objResult["gold"]
            goldxs = result.m_objResult["goldxs"]
            token = result.m_objResult["token"]
            tokenxs = result.m_objResult["tokenxs"]
            self.info("试试手气，获得{}金币({}倍暴击)，{}军令({}倍暴击)".format(gold, goldxs, token, tokenxs), True)

    def get_login_reward_info(self):
        url = "/root/mainCity!getLoginRewardInfo.action"
        result = self.get_protocol_mgr().get_xml(url, "登录送礼")
        if result and result.m_bSucceed:
            if result.m_objResult["lastmonth"]["state15"] == "1":
                self.get_reward(1, 1)
            if result.m_objResult["lastmonth"]["statefull"] == "1":
                self.get_reward(1, 2)
            if result.m_objResult["curmonth"]["state15"] == "1":
                self.get_reward(2, 1)
            if result.m_objResult["curmonth"]["statefull"] == "1":
                self.get_reward(2, 2)

    def get_reward(self, cid, opt):
        url = "/root/mainCity!getReward.action"
        data = {"cId": cid, "opt": opt}
        result = self.get_protocol_mgr().post_xml(url, data, "领取登录送礼")
        if result and result.m_bSucceed:
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["rewardinfo"])
            self.info("领取登录送礼，获得{}".format(reward_info))

    def get_champion_info(self):
        url = "/root/mainCity!getChampionInfo.action"
        result = self.get_protocol_mgr().get_xml(url, "争霸风云榜")
        if result and result.m_bSucceed:
            if result.m_objResult["canvisit"] == "1":
                self.visit_champion()

    def visit_champion(self):
        url = "/root/mainCity!visitChampion.action"
        result = self.get_protocol_mgr().get_xml(url, "恭贺")
        if result and result.m_bSucceed:
            self.info("恭贺，获得点券+{}".format(GlobalFunc.get_short_readable((int)(result.m_objResult["tickets"]))))

    def get_general_tower_info(self, build):
        url = "/root/mainCity!getGeneralTowerInfo.action"
        result = self.get_protocol_mgr().get_xml(url, "将军塔")
        if result and result.m_bSucceed:
            tower = GeneralTower()
            tower.handle_info(result.m_objResult["generaltower"])
            self.info("今天获得宝石+{}".format(tower.gemstonenum))
            if build:
                while tower.buildingstone > 0:
                    self.use_building_stone(tower)

    def use_building_stone(self, tower):
        url = "/root/mainCity!useBuildingStone.action"
        result = self.get_protocol_mgr().get_xml(url, "筑造将军塔")
        if result and result.m_bSucceed:
            tower.handle_info(result.m_objResult["generaltower"])
            msg = "筑造将军塔，进度增加{}".format(tower.addprogress)
            if tower.levelup == 1:
                msg += "，升级"
            self.info(msg)
            self.info("{}级将军塔({}/{})，剩余{}筑造石".format(tower.generaltowerlevel, tower.buildingprogress, tower.leveluprequirement, tower.buildingstone))
        else:
            tower.buildingstone = 0

    def right_army(self):
        url = "/root/mainCity!rightArmy.action"
        result = self.get_protocol_mgr().get_xml(url, "征义兵")
        if result and result.m_bSucceed:
            self.m_objUser.m_nRightCd = int(result.m_objResult.get("rightcd", "0"))
            self.m_objUser.m_nRightNum = int(result.m_objResult.get("rightnum", "0"))
            forces = int(result.m_objResult.get("forces", "0"))
            self.info("征义兵，获得兵力+{}，剩余{}次征义兵".format(GlobalFunc.get_short_readable(forces), self.m_objUser.m_nRightNum))

    def draught(self, percent):
        need_forces = self.m_objUser.m_nMaxForces * percent
        if self.m_objUser.m_nForces < need_forces:
            forces = need_forces - self.m_objUser.m_nForces
            need_copper = int(forces / 2)
            copper = need_copper - self.m_objUser.m_nCopper
            if copper > 0:
                import math
                exchange_num = int(math.ceil(float(copper) / 5000000.0))
                misc_mgr = self.get_service_factory().get_misc_mgr()
                while exchange_num > 0:
                    exchange_num -= 1
                    misc_mgr.get_tickets_reward_by_name("银币", 10)
            url = "/root/mainCity!draught.action"
            data = {"forceNum": int(forces)}
            result = self.get_protocol_mgr().post_xml(url, data, "征兵")
            if result and result.m_bSucceed:
                self.info("征兵，兵力+{}".format(GlobalFunc.get_short_readable(int(forces))))

    def per_impose(self):
        impose_num, force_impose_cost = 0, 100
        url = "/root/mainCity!perImpose.action"
        result = self.get_protocol_mgr().get_xml(url, "征收")
        if result and result.m_bSucceed:
            impose_num = int(result.m_objResult["imposedto"]["imposenum"])
            impose_max_num = int(result.m_objResult["imposedto"]["imposemaxnum"])
            force_impose_cost = int(result.m_objResult["imposedto"]["forceimposecost"])
            self.m_objUser.m_bImposeCdFlag = result.m_objResult["imposedto"]["cdflag"] == "1"
            self.m_objUser.m_nImposeCd = int(result.m_objResult["imposedto"]["lastimposetime"])
            self.info("今日可征收次数：{}/{}，强征需要花费{}金币".format(impose_num, impose_max_num, force_impose_cost))

            if "larrydto" in result.m_objResult:
                self.select_le(result.m_objResult["larrydto"]["effect1"], result.m_objResult["larrydto"]["effect2"])

        return impose_num, force_impose_cost

    def select_le(self, effect1, effect2):
        opt = self.get_impose_select_le(effect1, effect2)
        url = "/root/mainCity!selectLE.action"
        data = {"opt": opt}
        result = self.get_protocol_mgr().post_xml(url, data, "回答征收问题")
        if result and result.m_bSucceed:
            dict_reward = dict()
            dict_reward["民忠"] = int(result.m_objResult["ledto"]["l"])
            dict_reward["威望"] = int(result.m_objResult["ledto"]["f"])
            dict_reward["银币"] = int(result.m_objResult["ledto"]["s"])
            dict_reward["金币"] = int(result.m_objResult["ledto"]["g"])
            dict_reward["征收次数"] = int(result.m_objResult["ledto"]["t"])
            dict_reward["征收CD"] = int(result.m_objResult["ledto"]["c"])
            msg = "征收问题[({})，({})]，选择答案[{}]，获得".format(effect1, effect2, opt)
            for k, v in dict_reward.iteritems():
                if v > 0:
                    msg += "{}+{}，".format(k, v)
                elif v < 0:
                    msg += "{}{}，".format(k, v)
            self.info(msg, dict_reward["金币"] > 0)

    def impose(self, force, cost=0):
        url = "/root/mainCity!impose.action"
        desc = "征收"
        if force:
            url = "/root/mainCity!forceImpose.action"
            desc = "花费{}金币强征".format(cost)
        result = self.get_protocol_mgr().get_xml(url, desc)
        if result and result.m_bSucceed:
            use_gold = False
            if force:
                use_gold = True
                self.add_task_finish_num(2, 1)
            self.add_task_finish_num(1, 1)
            msg = "{}，获得银币+{}".format(desc, GlobalFunc.get_short_readable(int(result.m_objResult["cooperdis"])))
            gold_dis = result.m_objResult["golddis"]
            if gold_dis != "0":
                msg += "，金币+{}".format(gold_dis)
                use_gold = True
            self.info(msg, use_gold)

    def get_pick_space(self, proportion):
        url = "/root/outCity!getPickSpace.action"
        result = self.get_protocol_mgr().get_xml(url, "宝石矿洞")
        if result and result.m_bSucceed:
            for v in result.m_objResult["playerpickdto"]:
                if float(v["output"]) / float(v["limit"]) >= proportion:
                    self.end_bao_shi_pick(v)

    def end_bao_shi_pick(self, player_pick_dto):
        url = "/root/outCity!endBaoshiPick.action"
        data = {"pickSpaceId": player_pick_dto["id"]}
        result = self.get_protocol_mgr().post_xml(url, data, "采集宝石")
        if result and result.m_bSucceed:
            msg = "采集宝石"
            if "baoji" in result.m_objResult:
                msg += "，{}倍暴击".format(result.m_objResult["baoji"])
            msg += "，获得{}宝石".format(result.m_objResult["baoshi"])
            self.info(msg)

    def jail(self, available_gold, get_baoshi):
        url = "/root/jail.action"
        result = self.get_protocol_mgr().get_xml(url, "监狱")
        if result and result.m_bSucceed:
            if "remaintime" not in result.m_objResult:
                per_gold = int(result.m_objResult["pergold"])
                if per_gold <= available_gold:
                    self.tech_research()
            for jail_work in result.m_objResult["jailwork"]:
                if jail_work["canget"] != "0":
                    jail_id = int(jail_work["id"]) - 1
                    self.recv_jail_work(1, jail_id)
                    if get_baoshi:
                        self.recv_jail_work(0, jail_id)

    def tech_research(self):
        url = "/root/jail!techResearch.action"
        result = self.get_protocol_mgr().get_xml(url, "技术研究")
        if result and result.m_bSucceed:
            remain_time = int(result.m_objResult["remaintime"])
            self.info("监狱技术研究，剩余时间：{}".format(TimeMgr.get_datetime_string(remain_time)))

    def recv_jail_work(self, jail_type, jail_id):
        url = "/root/jail!recvJailWork.action"
        data = {"type": jail_type, "weizhi": jail_id}
        result = self.get_protocol_mgr().post_xml(url, data, "监狱劳作")
        if result and result.m_bSucceed:
            msg = "监狱劳作"
            if "baoshi" in result.m_objResult:
                msg += "，获得{}宝石".format(result.m_objResult["baoshi"])
            elif "bintie" in result.m_objResult:
                msg += "，获得{}镔铁".format(result.m_objResult["bintie"])
            self.info(msg)

    def escape(self):
        url = "/root/jail!escape.action"
        result = self.get_protocol_mgr().get_xml(url, "从监狱逃跑")
        if result and result.m_bSucceed:
            cd = int(result.m_objResult["cd"])
            self.info("从监狱逃跑，冷却时间：{}秒".format(cd))
            return cd * 1000

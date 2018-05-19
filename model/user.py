# -*- coding: utf-8 -*-
# 角色信息
from model.main_city_dto import MainCityDto
from model.constructor_dto import ConstructorDto
from model.mo_zi_building import MoZiBuilding
from model.task import Task
from model.enum.activity_type import ActivityType
from model.global_func import GlobalFunc


class User(object):
    def __init__(self):
        super(User, self).__init__()
        self.m_nId = 0  # 角色id
        self.m_szUserName = ""  # 角色名
        self.m_nLevel = 0  # 角色等级
        self.m_nYear = 0  # 年份
        self.m_szSeason = ""  # 季节
        self.m_szNation = ""  # 国家
        self.m_bInNewArea = False  # 新区

        self.m_nCopper = 0  # 银币
        self.m_nFood = 0  # 粮草
        self.m_nForces = 0  # 兵力
        self.m_nGold = 0  # 金币
        self.m_nRechargeGold = 0  # 充值金币
        self.m_nJunGong = 0  # 军功
        self.m_nPrestige = 0  # 声望
        self.m_nBowlder = 0  # 原石
        self.m_nToken = 0  # 军令
        self.m_nAttToken = 0  # 攻击令
        self.m_nCityHp = 0  # 城防值
        self.m_nTickets = 0  # 点券

        self.m_nImposeCd = 0  # 征收冷却时间
        self.m_bImposeCdFlag = False  # 征收冷却状态
        self.m_nTokenCd = 0  # 军令冷却时间
        self.m_bTokenCdFlag = False  # 军令冷却状态
        self.m_nTransferCd = 0  # 迁移冷却时间
        self.m_nProtectCd = 0  # 保护冷却时间
        self.m_nInspireCd = 0  # 鼓舞冷却时间
        self.m_nInspireState = 0  # 鼓舞状态
        self.m_nRightCd = 0  # 征义兵冷却时间
        self.m_nRightNum = 0  # 可征义兵次数
        self.m_nCityHpRecoverCd = 0  # 城防恢复冷却时间

        self.m_nMaxBowlder = 0  # 原石上限
        self.m_nMaxToken = 0  # 军令上限
        self.m_nMaxAttToken = 0  # 攻击令上限
        self.m_nMaxCityHp = 0  # 城防值上限
        self.m_nMaxFood = 0  # 粮草上限
        self.m_nMaxCopper = 0  # 银币上限
        self.m_nMaxForces = 0  # 兵力上限
        self.m_nMaxActive = 0  # 行动力上限

        self.m_nJailBaoShi = 0  # 监狱劳作获得宝石
        self.m_nBattleScore = 0  # 战绩
        self.m_nCurActive = 0  # 当前行动力
        self.m_nArrestState = 0  # 劳作状态 0:正常 1:劳作 10:逃跑cd 100:被抓
        self.m_bCanTech = False  # 技术研究
        self.m_bHasPerDayReward = False  # 今日手气
        self.m_bHasVersionGift = False  # 版本更新奖励

        self.m_nRemainSeniorSlaves = 0  # 剩余高级劳工(墨子改造)
        self.m_bCanVisit = False  # 恭贺争霸风云榜
        self.m_bNewTechnology = False  # 科技
        self.m_bWarChariot = False  # 战车

        self.m_nAreaId = 0  # 当前所在城池id
        self.m_szAreaName = ""  # 当前所在城池名称

        self.m_dictActivities = dict()  # 活动列表
        self.m_dictMainCityBuildings = dict()  # 主城建筑
        self.m_listConstructorDto = list()  # 建筑建造队列
        self.m_dictMoZiBuildings = dict()  # 墨子建筑
        self.m_dictTasks = dict()  # 日常任务
        self.m_dictTicketExchange = dict()  # 点券兑换资源

    def __str__(self):
        return "{}({}级，{})，{}年{}，{}金币，{}银币，{}点券，{}行动力，{}军令，{}攻击令，{}城防值，状态：{}".format(
            self.m_szUserName, self.m_nLevel, self.m_szNation,
            self.m_nYear, self.m_szSeason, GlobalFunc.get_short_readable(self.m_nGold),
            GlobalFunc.get_short_readable(self.m_nCopper), self.m_nTickets, self.m_nCurActive,
            self.m_nToken, self.m_nAttToken, self.m_nCityHp, self.m_nArrestState)

    def handle_info(self, dict_info):
        if "playerid" in dict_info:
            self.m_nId = int(dict_info["playerid"])
        if "playername" in dict_info:
            self.m_szUserName = dict_info["playername"]
        if "playerlevel" in dict_info:
            self.m_nLevel = int(dict_info["playerlevel"])
        if "year" in dict_info:
            self.m_nYear = int(dict_info["year"])
        if "season" in dict_info:
            self.set_season(int(dict_info["season"]))
        if "nation" in dict_info:
            self.set_nation(int(dict_info["nation"]))
        if "innewarea" in dict_info:
            self.m_bInNewArea = dict_info["innewarea"] == "1"

        if "copper" in dict_info:
            self.m_nCopper = int(dict_info["copper"])
        if "food" in dict_info:
            self.m_nFood = int(dict_info["food"])
        if "forces" in dict_info:
            self.m_nForces = int(dict_info["forces"])
        if "sys_gold" in dict_info:
            self.m_nGold = int(dict_info["sys_gold"])
        if "user_gold" in dict_info:
            self.m_nRechargeGold = int(dict_info["user_gold"])
        if "jyungong" in dict_info:
            self.m_nJunGong = int(dict_info["jyungong"])
        if "prestige" in dict_info:
            self.m_nPrestige = int(dict_info["prestige"])
        if "bowlder" in dict_info:
            self.m_nBowlder = int(dict_info["bowlder"])
        if "token" in dict_info:
            self.m_nToken = int(dict_info["token"])
        if "atttoken" in dict_info:
            self.m_nAttToken = int(dict_info["atttoken"])
        if "attacktoken" in dict_info:
            self.m_nAttToken = int(dict_info["attacktoken"])
        if "cityhp" in dict_info:
            self.m_nCityHp = int(dict_info["cityhp"])

        if "imposecd" in dict_info:
            self.m_nImposeCd = int(dict_info["imposecd"])
        if "imposecdflag" in dict_info:
            self.m_bImposeCdFlag = dict_info["imposecdflag"] == "1"
        if "tokencd" in dict_info:
            self.m_nTokenCd = int(dict_info["tokencd"])
        if "tokencdflag" in dict_info:
            self.m_bTokenCdFlag = dict_info["tokencdflag"] == "1"
        if "transfercd" in dict_info:
            self.m_nTransferCd = int(dict_info["transfercd"])
        if "protectcd" in dict_info:
            self.m_nProtectCd = int(dict_info["protectcd"])
        if "inspirecd" in dict_info:
            self.m_nInspireCd = int(dict_info["inspirecd"])
        if "inspirestate" in dict_info:
            self.m_nInspireState = int(dict_info["inspirestate"])

        if "maxbowlder" in dict_info:
            self.m_nMaxBowlder = int(eval(dict_info["maxbowlder"]))
        if "maxtoken" in dict_info:
            self.m_nMaxToken = int(dict_info["maxtoken"])
        if "maxattacktoken" in dict_info:
            self.m_nMaxAttToken = int(dict_info["maxattacktoken"])
        if "maxcityhp" in dict_info:
            self.m_nMaxCityHp = int(dict_info["maxcityhp"])
        if "maxfood" in dict_info:
            self.m_nMaxFood = int(dict_info["maxfood"])
        if "maxcoin" in dict_info:
            self.m_nMaxCopper = int(dict_info["maxcoin"])
        if "maxforce" in dict_info:
            self.m_nMaxForces = int(dict_info["maxforce"])
        if "maxactive" in dict_info:
            self.m_nMaxActive = int(dict_info["maxactive"])

        if "jailbaoshi" in dict_info:
            self.m_nJailBaoShi += int(dict_info["jailbaoshi"])
        if "battlescore" in dict_info:
            self.m_nBattleScore = int(dict_info["battlescore"])
        if "curactive" in dict_info:
            self.m_nCurActive = int(dict_info["curactive"])
        if "arreststate" in dict_info:
            self.m_nArrestState = int(dict_info["arreststate"])
        if "cantech" in dict_info:
            self.m_bCanTech = dict_info["cantech"] == "1"

        if "areaid" in dict_info:
            self.m_nAreaId = int(dict_info["areaid"])
        if "areaname" in dict_info:
            self.m_szAreaName = dict_info["areaname"]

    def update_player_info(self, dict_player_info):
        if dict_player_info is not None:
            self.handle_info(dict_player_info)

    def update_player_battle_info(self, dict_player_battle_info):
        if dict_player_battle_info is not None:
            self.handle_info(dict_player_battle_info)

    def refresh_player_info(self, dict_player_info):
        self.m_bHasPerDayReward = dict_player_info.get("perdayreward", "0") == "1"
        self.m_bHasVersionGift = dict_player_info.get("version_gift", "0") == "1"
        if dict_player_info.get("gifteventbaoshi4", "0") == "1":
            self.m_dictActivities[ActivityType.GiftEventBaoShi4] = True
        if dict_player_info.get("dumpevent", "0") == "1":
            self.m_dictActivities[ActivityType.DumpEvent] = True
        if dict_player_info.get("kfwdeventreward", "0") == "1":
            self.m_dictActivities[ActivityType.KfWDEventReward] = True
        if dict_player_info is not None:
            self.handle_info(dict_player_info)

    def update_limits(self, dict_limits):
        if dict_limits is not None:
            self.handle_info(dict_limits)

    def update_player_extra_info(self, dict_player_extra_info):
        if dict_player_extra_info is not None:
            self.handle_info(dict_player_extra_info)

    def update_player_extra_info2(self, dict_player_extra_info):
        if dict_player_extra_info is not None:
            self.handle_info(dict_player_extra_info)

    def clear_activities(self):
        self.m_dictActivities = dict()

    def set_season(self, season):
        season_tuple = ("春", "夏", "秋", "冬")
        self.m_szSeason = season_tuple[season - 1]

    def set_nation(self, nation):
        nation_tuple = ("中立", "魏国", "蜀国", "吴国")
        self.m_szNation = nation_tuple[nation]

    def set_main_city_dto(self, list_main_city_dto):
        self.m_dictMainCityBuildings = dict()
        for main_city_dto in list_main_city_dto:
            dto = MainCityDto()
            dto.handle_info(main_city_dto)
            self.m_dictMainCityBuildings[dto.id] = dto

    def set_constructor_dto(self, list_constructor_dto):
        self.m_listConstructorDto = list()
        for constructor_dto in list_constructor_dto:
            dto = ConstructorDto()
            dto.handle_info(constructor_dto)
            self.m_listConstructorDto.append(dto)

    def set_mo_zi_building(self, list_mo_zi_building):
        self.m_dictMoZiBuildings = dict()
        for mo_zi_building in list_mo_zi_building:
            building = MoZiBuilding()
            building.handle_info(mo_zi_building)
            self.m_dictMoZiBuildings[building.id] = building

    def set_task(self, list_task):
        self.m_dictTasks = dict()
        for task in list_task:
            if task["taskstate"] == "1":
                t = Task()
                t.handle_info(task)
                self.m_dictTasks[t.type] = t

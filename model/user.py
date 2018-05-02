# -*- coding: utf-8 -*-
# 角色信息


class User(object):
    def __init__(self):
        super(User, self).__init__()
        self.m_bHasPerDayReward = False  # 今日手气
        self.m_bHasVersionGift = False  # 版本更新奖励
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

        self.m_nImposeCd = 0  # 征收冷却时间
        self.m_bImposeCdFlag = False  # 征收冷却状态
        self.m_nTokenCd = 0  # 军令冷却时间
        self.m_bTokenCdFlag = False  # 军令冷却状态
        self.m_nTransferCd = 0  # 迁移冷却时间
        self.m_nProtectCd = 0  # 保护冷却时间
        self.m_nInspireCd = 0  # 鼓舞冷却时间
        self.m_nInspireState = 0  # 鼓舞状态

        self.m_nMaxBowlder = 0  # 原石上限
        self.m_nMaxToken = 0  # 军令上限
        self.m_nMaxAttToken = 0  # 攻击令上限
        self.m_nMaxCityHp = 0  # 城防值上限
        self.m_nMaxFood = 0  # 粮草上限
        self.m_nMaxCopper = 0  # 银币上限
        self.m_nMaxForces = 0  # 兵力上限

        self.m_nJailBaoShi = 0  # 监狱劳作获得宝石
        self.m_nBattleScore = 0  # 战绩
        self.m_nCurActive = 0  # 当前行动力
        self.m_nArrestState = 0  # 劳作状态
        self.m_bCanTech = False  # 技术研究

        self.m_nAreaId = 0  # 当前所在城池id
        self.m_szAreaName = ""  # 当前所在城池名称

        self.m_listActivities = []  # 活动列表

    def update_player_info(self, dict_player_info):
        self.m_nJailBaoShi += int(dict_player_info.get("battlescore", "0"))
        self.m_nBattleScore = int(dict_player_info.get("battlescore", "0"))
        self.m_nCurActive = int(dict_player_info.get("curactive", "0"))
        self.m_nArrestState = int(dict_player_info.get("arreststate", "0"))

    def update_player_battle_info(self, dict_player_battle_info):
        pass

    def refresh_player_info(self, dict_player_info):
        if dict_player_info is not None:
            self.m_bHasPerDayReward = dict_player_info.get("perdayreward", "0") == "1"
            self.m_bHasVersionGift = dict_player_info.get("version_gift", "0") == "1"
            self.m_nId = int(dict_player_info["playerid"])
            self.m_szUserName = dict_player_info["playername"]
            self.m_nLevel = int(dict_player_info["playerlevel"])
            self.m_nYear = int(dict_player_info["year"])
            self.set_season(int(dict_player_info["season"]))
            self.set_nation(int(dict_player_info["nation"]))
            self.m_bInNewArea = dict_player_info.get("innewarea", "0") == "1"

            self.m_nCopper = int(dict_player_info["copper"])
            self.m_nFood = int(dict_player_info["food"])
            self.m_nForces = int(dict_player_info["forces"])
            self.m_nGold = int(dict_player_info["sys_gold"])
            self.m_nRechargeGold = int(dict_player_info["user_gold"])
            self.m_nJunGong = int(dict_player_info["jyungong"])
            self.m_nPrestige = int(dict_player_info["prestige"])
            self.m_nBowlder = int(dict_player_info["bowlder"])
            self.m_nToken = int(dict_player_info["token"])
            self.m_nAttToken = int(dict_player_info["atttoken"])
            self.m_nCityHp = int(dict_player_info["cityhp"])

            self.m_nImposeCd = int(dict_player_info["imposecd"])
            self.m_bImposeCdFlag = dict_player_info.get("imposecdflag", "0") == "1"
            self.m_nTokenCd = int(dict_player_info["tokencd"])
            self.m_bTokenCdFlag = dict_player_info.get("tokencdflag", "0") == "1"
            self.m_nTransferCd = int(dict_player_info["transfercd"])
            self.m_nProtectCd = int(dict_player_info["protectcd"])
            self.m_nInspireCd = int(dict_player_info["inspirecd"])
            self.m_nInspireState = int(dict_player_info["inspirestate"])

            self.m_nMaxBowlder = int(eval(dict_player_info["maxbowlder"]))
            self.m_nMaxToken = int(dict_player_info["maxtoken"])
            self.m_nMaxAttToken = int(dict_player_info["maxattacktoken"])
            self.m_nMaxCityHp = int(dict_player_info["maxcityhp"])

            self.m_nAreaId = int(dict_player_info["areaid"])
            self.m_szAreaName = dict_player_info["areaname"]

    def update_limits(self, dict_limits):
        if dict_limits is not None:
            self.m_nMaxFood = int(dict_limits["maxfood"])
            self.m_nMaxCopper = int(dict_limits["maxcoin"])
            self.m_nMaxForces = int(dict_limits["maxforce"])

    def update_player_extra_info(self, dict_player_extra_info):
        if dict_player_extra_info is not None:
            pass

    def update_player_extra_info2(self, dict_player_extra_info):
        if dict_player_extra_info is not None:
            self.m_bCanTech = dict_player_extra_info.get("cantech", "0") == "1"
            self.m_nCurActive = int(dict_player_extra_info.get("curactive", "0"))
            self.m_nArrestState = int(dict_player_extra_info.get("arreststate", "0"))

    def clear_activities(self):
        self.m_listActivities = []

    def set_season(self, season):
        season_tuple = ("春", "夏", "秋", "冬")
        self.m_szSeason = season_tuple[season - 1]

    def set_nation(self, nation):
        nation_tuple = ("中立", "魏国", "蜀国", "吴国")
        self.m_szNation = nation_tuple[nation]

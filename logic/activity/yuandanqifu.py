# -*- coding: utf-8 -*-
# 酒神觉醒
from logic.activity.activity_task import ActivityTask
from model.enum.activity_type import ActivityType
from model.reward_info import RewardInfo


class YuanDanQiFu(ActivityTask):
    def __init__(self):
        super(YuanDanQiFu, self).__init__(ActivityType.YuanDanQiFu)
        self.m_szName = self.__class__.__name__
        self.m_szReadable = "酒神觉醒"

    def run(self):
        if not self.enable():
            return self.next_half_hour()

        info = self.get_qifu_event_info()
        if info is None:
            return self.next_half_hour()

        self.info("福气：{}/{}".format(info["福气"], info["最大福气"]))

        if info["状态"] == 0:
            if info["祈福花费金币"] <= self.m_dictConfig["gold"] and info["祈福花费金币"] <= self.get_available_gold():
                self.start_qifu(info["祈福花费金币"])
                return self.immediate()
        elif info["状态"] == 1:
            if info["福气"] >= info["最大福气"]:
                self.qifu_active()
            self.qifu_choose(2)
            return self.immediate()
        elif info["状态"] == 2:
            # if info["宝箱总福气"] >= self.m_dictConfig["all_open_fuqi"] and info["全开花费金币"] <= self.m_dictConfig["all_open_gold"] and info["全开花费金币"] <= self.get_available_gold():
            # if info["类型"] in self.m_dictConfig["type"] and info["剩余的酒数量"] >= self.m_dictConfig["all_open_jiu"] and info["全开花费金币"] <= self.m_dictConfig["all_open_gold"] and info["全开花费金币"] <= self.get_available_gold():
            if info["本次祈福倍数"] >= self.m_dictConfig["all_open_xs"] and info["全开花费金币"] <= self.m_dictConfig["all_open_gold"] and info["全开花费金币"] <= self.get_available_gold():
                if info["福气"] >= info["最大福气"]:
                    self.qifu_active()
                self.fuling_enze(info["全开花费金币"])
                return self.immediate()
            else:
                self.next_qifu()
                return self.immediate()

        return self.next_half_hour()

    def get_qifu_event_info(self):
        url = "/root/yuandanqifu!getQifuEventInfo.action"
        result = self.get_xml(url, "酒神觉醒")
        if result and result.m_bSucceed:
            info = dict()
            info["类型"] = int(result.m_objResult["type"])
            info["状态"] = int(result.m_objResult["qifustate"])
            info["福气"] = int(result.m_objResult["fuqi"])
            info["最大福气"] = int(result.m_objResult["maxfuqi"])
            info["本次祈福倍数"] = int(result.m_objResult["xs"])
            info["下次祈福倍数"] = int(result.m_objResult["nextxs"])
            info["祈福花费金币"] = int(result.m_objResult["qifuneedcoin"])
            info["全开花费金币"] = int(result.m_objResult["fulingneedcoin"])
            info["宝箱总福气"] = 0
            info["剩余的酒数量"] = 0
            if "card" in result.m_objResult:
                for card in result.m_objResult["card"]:
                    info["宝箱总福气"] += int(card["fuqi"])
                    if int(card["get"]) == 0:
                        info["剩余的酒数量"] += int(card["tickets"]) * info["本次祈福倍数"]
            return info

    def qifu_active(self):
        url = "/root/yuandanqifu!qifuActive.action"
        result = self.get_xml(url, "双倍祈福")
        if result and result.m_bSucceed:
            self.info("激活{}倍祈福".format(result.m_objResult["xs"]))

    def qifu_choose(self, index):
        url = "/root/yuandanqifu!qifuChoose.action"
        data = {"indexId": index}
        result = self.post_xml(url, data, "选择祈福")
        if result and result.m_bSucceed:
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["reward"]["rewardinfo"])
            self.add_reward(reward_info)
            self.info("选择祈福[{}]，福气+{}，获得{}".format(result.m_objResult["reward"]["indexid"], result.m_objResult["reward"]["fuqi"], reward_info))

    def next_qifu(self):
        url = "/root/yuandanqifu!nextQifu.action"
        result = self.get_xml(url, "下一轮祈福")
        if result and result.m_bSucceed:
            self.info("进入下一轮祈福")

    def start_qifu(self, cost):
        url = "/root/yuandanqifu!startQifu.action"
        result = self.get_xml(url, "开始祈福")
        if result and result.m_bSucceed:
            self.consume_gold(cost)
            if cost > 0:
                self.info("花费{}金币，开始祈福".format(cost), True)
            else:
                self.info("免费开始祈福")

    def fuling_enze(self, cost):
        url = "root/yuandanqifu!qifuChooseAll.action"
        result = self.get_xml(url, "金币全开")
        if result and result.m_bSucceed:
            self.consume_gold(cost)
            self.info("花费{}金币，全开宝箱".format(cost), True)

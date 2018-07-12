# -*- coding: utf-8 -*-
# 宝石翻牌
from logic.activity.activity_task import ActivityTask
from model.enum.activity_type import ActivityType
from model.reward_info import RewardInfo, Reward


class GemCard(ActivityTask):
    def __init__(self):
        super(GemCard, self).__init__(ActivityType.GiftEventBaoShi4)
        self.m_szName = self.__class__.__name__
        self.m_szReadable = "宝石翻牌"

    def run(self):
        if not self.enable():
            return self.next_half_hour()

        info = self.get_gem_card_info()
        if info is None:
            return self.next_half_hour()

        if info["免费次数"] > 0:
            cost = 0
            double = 0
            cost_cost = 0
            double_cost = 0
            is_combo, can_combo, combo_id = self.check_combo(info["卡牌"])
            if can_combo:
                if info["升级次数"] < info["免费升级次数"]:
                    for card in info["卡牌"]:
                        if card["id"] == combo_id:
                            card["combo"] += 1
                            is_combo = True
                            break
                elif info["升级花费金币"] <= self.m_dictConfig["upgradegold"] and info["升级花费金币"] <= self.get_available_gold():
                    for card in info["卡牌"]:
                        if card["id"] == combo_id:
                            card["combo"] += 1
                            cost_cost = info["升级花费金币"]
                            is_combo = True
                            break
            total = sum([item["combo"] for item in info["卡牌"]])
            if (is_combo and info["组合倍数"] >= self.m_dictConfig["comboxs"] and total >= self.m_dictConfig["total"]) or (info["免费次数"] <= info["免费翻倍次数"]):
                if info["免费翻倍次数"] > 0:
                    double = 1
                elif info["翻倍花费金币"] <= self.m_dictConfig["doublecost"] and info["翻倍花费金币"] <= self.get_available_gold():
                    double = 1
                    double_cost = info["翻倍花费金币"]
                else:
                    double = 0
            card_list = ",".join([str(item["combo"]) for item in info["卡牌"]])
            if is_combo:
                total *= 6
            if double == 1:
                total *= 10
            total *= 100
            self.receive_gem(double, cost, card_list, double_cost, cost_cost, total)
            return self.immediate()
        elif info["购买次数花费金币"] <= self.m_dictConfig["buygold"] and info["购买次数花费金币"] <= self.get_available_gold():
            return self.immediate()

        return self.next_half_hour()

    def get_gem_card_info(self):
        url = "/root/gemCard!getGemCardInfo.action"
        result = self.get_xml(url, "宝石翻牌")
        if result and result.m_bSucceed:
            info = dict()
            info["免费翻倍次数"] = int(result.m_objResult["gemcardinfo"]["freedouble"])
            info["翻倍花费金币"] = int(result.m_objResult["doublecost"])
            info["免费升级次数"] = int(result.m_objResult["freeupgradetimes"])
            info["升级花费金币"] = int(result.m_objResult["gemcardinfo"]["upgradegold"])
            info["升级次数"] = int(result.m_objResult["gemcardinfo"]["upgradetimes"])
            info["组合倍数"] = int(result.m_objResult["gemcardinfo"]["comboxs"])
            info["免费次数"] = int(result.m_objResult["gemcardinfo"]["freetimes"])
            info["购买次数花费金币"] = int(result.m_objResult["gemcardinfo"]["buygold"])
            info["卡牌"] = list()
            combos = map(int, result.m_objResult["gemcardinfo"]["gemcardliststring"][:-1].split(","))
            for idx, combo in enumerate(combos):
                info["卡牌"].append({"id": idx, "combo": combo})
            return info

    def receive_gem(self, double, cost, card_list, double_cost, cost_cost, baoshi):
        url = "/root/gemCard!receiveGem.action"
        data = {"cost": cost, "doubleCard": double, "list": card_list}
        result = self.post_xml(url, data, "领取")
        if result and result.m_bSucceed:
            reward = Reward()
            reward.type = 5
            reward.lv = 1
            reward.num = baoshi
            reward.init()
            reward_info = RewardInfo()
            reward_info.m_listRewards.append(reward)
            self.add_reward(reward_info)
            self.consume_gold(double_cost)
            self.consume_gold(cost_cost)
            use_gold = False
            msg = ""
            if double == 1:
                if double_cost > 0:
                    use_gold = True
                    msg += "花费{}金币翻倍，".format(double_cost)
                else:
                    msg += "免费翻倍，"
            if cost_cost > 0:
                use_gold = True
                msg += "花费{}金币升级，"
            else:
                msg += "免费升级，"
            msg += "领取翻牌奖励，获得{}".format(reward_info)
            self.info(msg, use_gold)

    # return is_combo, can_combo, combo_id
    def check_combo(self, card_list):
        tmp_card_list = sorted(card_list, key=lambda obj: obj["combo"])
        combo = 0
        for card in tmp_card_list:
            combo = combo * 10 + card["combo"]
        if combo in self.m_dictConfig["combo"]:
            return True, False, -1
        else:
            if combo in self.m_dictConfig["upgrade"]:
                return False, True, tmp_card_list[self.m_dictConfig["upgrade"][combo]]["id"]
            else:
                return False, False, -1

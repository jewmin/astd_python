# -*- coding: utf-8 -*-
# 新年敲钟
from logic.activity.activity_task import ActivityTask
from model.enum.activity_type import ActivityType
from model.reward_info import RewardInfo


class RingEvent(ActivityTask):
    def __init__(self):
        super(RingEvent, self).__init__(ActivityType.RingEvent)
        self.m_szName = self.__class__.__name__
        self.m_szReadable = "新年敲钟"

    def run(self):
        if not self.enable():
            return self.next_half_hour()

        info = self.get_ring_event_info()
        if info is None:
            return self.next_half_hour()

        for reward in info["奖励"]:
            if reward["state"] == "1":
                self.get_progress_reward(reward, self.m_dictConfig["reward"])

        while info["红包"] > 0:
            self.recv_red_paper()
            info["红包"] -= 1

        if info["对联状态"] == 1:
            self.open_reel()
            return self.immediate()
        elif info["对联状态"] == 2:
            need_reel_num_list = [0, 0, 0, 0]
            reel_list = map(int, info["对联"][:-1].split(","))
            if info["已激活次数"] == 0 and (info["敲钟"][0]["免费次数"] > 0 or info["敲钟"][0]["花费金币"] <= self.m_dictConfig["cost"]):
                for idx in xrange(1, len(reel_list)):
                    need_reel_num_list[reel_list[idx]] += 1
            else:
                for idx in xrange(info["已激活次数"], len(reel_list)):
                    need_reel_num_list[reel_list[idx]] += 1
            for bell_id, reel in enumerate(info["敲钟"]):
                num = reel["免费次数"]
                if reel["花费金币"] <= self.m_dictConfig["cost"]:
                    num += 2
                if need_reel_num_list[bell_id] > num:
                    self.give_up_reel()
                    return self.immediate()
            if info["已激活次数"] == 0:
                if info["敲钟"][0]["免费次数"] > 0:
                    self.ring(0, 0)
                    return self.immediate()
                elif info["敲钟"][0]["花费金币"] <= self.m_dictConfig["cost"] and info["敲钟"][0]["花费金币"] <= self.get_available_gold():
                    self.ring(0, info["敲钟"][0]["花费金币"])
                    return self.immediate()
                else:
                    bell_id = reel_list[0]
                    if info["敲钟"][bell_id]["免费次数"] > 0:
                        self.ring(bell_id, 0)
                        return self.immediate()
                    elif info["敲钟"][bell_id]["花费金币"] <= self.m_dictConfig["cost"] and info["敲钟"][bell_id]["花费金币"] <= self.get_available_gold():
                        self.ring(bell_id, info["敲钟"][bell_id]["花费金币"])
                        return self.immediate()
                    else:
                        self.give_up_reel()
                        return self.immediate()
            else:
                bell_id = reel_list[info["已激活次数"]]
                if info["敲钟"][bell_id]["免费次数"] > 0:
                    self.ring(bell_id, 0)
                    return self.immediate()
                elif info["敲钟"][bell_id]["花费金币"] <= self.m_dictConfig["cost"] and info["敲钟"][bell_id]["花费金币"] <= self.get_available_gold():
                    self.ring(bell_id, info["敲钟"][bell_id]["花费金币"])
                    return self.immediate()
                else:
                    self.give_up_reel()
                    return self.immediate()
        else:
            for bell_id, reel in enumerate(info["敲钟"]):
                if reel["免费次数"] > 0:
                    self.ring(bell_id, 0)
                    return self.immediate()
                elif reel["花费金币"] <= self.m_dictConfig["cost"] and reel["花费金币"] <= self.get_available_gold():
                    self.ring(bell_id, reel["花费金币"])
                    return self.immediate()

        return self.next_half_hour()

    def get_ring_event_info(self):
        url = "/root/ringEvent!getRingEventInfo.action"
        result = self.get_xml(url, "新年敲钟")
        if result and result.m_bSucceed:
            info = dict()
            info["奖励"] = result.m_objResult["ringstate"]
            info["对联状态"] = int(result.m_objResult["reelstatus"])
            info["敲钟"] = list()
            info["敲钟"].append({"免费次数": int(result.m_objResult["randomtimes"]), "花费金币": int(result.m_objResult["randomcost"])})
            info["敲钟"].append({"免费次数": int(result.m_objResult["firsttimes"]), "花费金币": int(result.m_objResult["firstcost"])})
            info["敲钟"].append({"免费次数": int(result.m_objResult["secondtimes"]), "花费金币": int(result.m_objResult["secondcost"])})
            info["敲钟"].append({"免费次数": int(result.m_objResult["thirdtimes"]), "花费金币": int(result.m_objResult["thirdcost"])})
            info["对联"] = result.m_objResult.get("need", "")
            info["已激活次数"] = int(result.m_objResult.get("reelnum", "0"))
            info["红包"] = int(result.m_objResult.get("redpapernum", "0"))
            return info

    def get_progress_reward(self, reward, reward_type):
        url = "/root/ringEvent!getProgressReward.action"
        data = {"rewardId": reward["id"], "type": reward_type}
        result = self.post_xml(url, data, "领取进度奖励")
        if result and result.m_bSucceed:
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["rewardinfo"])
            self.add_reward(reward_info)
            self.info("领取进度奖励，获得{}".format(reward_info))

    def open_reel(self):
        reel_tuple = ("随机", "福", "禄", "寿")
        url = "/root/ringEvent!openReel.action"
        result = self.get_xml(url, "打开对联")
        if result and result.m_bSucceed:
            needs = map(int, result.m_objResult["need"][:-1].split(","))
            msg = "打开对联：{}".format(result.m_objResult["words"])
            for need in needs:
                msg += " {}".format(reel_tuple[need])
            self.info(msg)

    def ring(self, bell_id, cost):
        url = "/root/ringEvent!ring.action"
        data = {"bellId": bell_id}
        result = self.post_xml(url, data, "敲钟")
        if result and result.m_bSucceed:
            if cost > 0:
                msg = "花费{}金币".format(cost)
                use_gold = True
            else:
                msg = "免费"
                use_gold = False
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["rewardinfo"])
            self.add_reward(reward_info)
            self.consume_gold(cost)
            msg += "，敲钟，获得{}".format(reward_info)
            if "bigreward" in result.m_objResult:
                big_reward_info = RewardInfo()
                big_reward_info.handle_info(result.m_objResult["bigreward"]["rewardinfo"])
                self.add_reward(big_reward_info)
                msg += " {}".format(big_reward_info)
            self.info(msg, use_gold)

    def give_up_reel(self):
        url = "/root/ringEvent!giveUpReel.action"
        result = self.get_xml(url, "放弃对联")
        if result and result.m_bSucceed:
            self.info("放弃对联")

    def recv_red_paper(self):
        url = "/root/ringEvent!recvRedPaper.action"
        result = self.get_xml(url, "领取红包")
        if result and result.m_bSucceed:
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["rewardinfo"])
            self.add_reward(reward_info)
            self.info("领取红包，获得{}".format(reward_info))

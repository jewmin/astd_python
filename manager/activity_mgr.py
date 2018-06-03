# -*- coding: utf-8 -*-
# 活动管理
from manager.base_mgr import BaseMgr
from model.reward_info import RewardInfo
from model.global_func import GlobalFunc


class ActivityMgr(BaseMgr):
    def __init__(self, time_mgr, service_factory, user, index):
        super(ActivityMgr, self).__init__(time_mgr, service_factory, user, index)

    def get_match_detail(self):
        url = "/root/kfrank!getMatchDetail.action"
        result = self.get_protocol_mgr().get_xml(url, "乱世风云榜")
        if result and result.m_bSucceed:
            info = dict()
            info["花费军令"] = int(result.m_objResult["message"]["needtoken"])
            info["可领取上届排名奖励"] = result.m_objResult["message"]["boxinfo"]["havegetlast"] == "0"
            info["对战可领取宝箱"] = result.m_objResult["message"]["boxinfo"]["canget"] == "1"
            info["拥有宝箱"] = int(result.m_objResult["message"]["boxinfo"]["boxnum"])
            info["任务"] = result.m_objResult["message"]["taskinfo"]
            info["对战状态"] = result.m_objResult["message"]["status"]
            info["状态"] = result.m_objResult["message"]["globalstate"]
            info["准备状态"] = result.m_objResult["message"].get("canready", "0") == "1"
            info["下次战斗冷却时间"] = int(result.m_objResult["message"].get("nextbattlecd", "0"))
            for player_info in result.m_objResult["message"]["selfrank"]["playerinfo"]:
                if player_info.get("self", "0") == "1":
                    info["排名"] = int(player_info["rank"])
                    info["积分"] = int(player_info["score"])
                    break
            return info

    def start_match(self, token):
        url = "/root/kfrank!startMatch.action"
        result = self.get_protocol_mgr().get_xml(url, "匹配对手")
        if result and result.m_bSucceed:
            self.info("花费{}军令匹配对手".format(token))

    def ready(self):
        url = "/root/kfrank!ready.action"
        result = self.get_protocol_mgr().get_xml(url, "准备就绪")
        if result and result.m_bSucceed:
            self.info("准备就绪")

    def sync_data(self):
        url = "/root/kfrank!syncData.action"
        result = self.get_protocol_mgr().get_xml(url, "同步阵型")
        if result and result.m_bSucceed:
            self.info("同步阵型")

    def change_task(self):
        url = "/root/kfrank!changeTask.action"
        result = self.get_protocol_mgr().get_xml(url, "刷新对战任务")
        if result and result.m_bSucceed:
            task_info = result.m_objResult["message"]["taskinfo"]
            self.info("刷新对战任务，新任务[{} - {}({}宝箱)]".format(task_info["name"], task_info["intro"], task_info["reward"]))
            return task_info

    def open_box(self):
        url = "/root/kfrank!openBox.action"
        result = self.get_protocol_mgr().get_xml(url, "打开对战宝箱")
        if result and result.m_bSucceed:
            msg = "打开对战宝箱，获得"
            if "tickets" in result.m_objResult["message"]:
                msg += "{}点券 ".format(result.m_objResult["message"]["tickets"]["num"])
            if "rewardgeneral" in result.m_objResult["message"]:
                msg += "{}大将令[{}] ".format(result.m_objResult["message"]["rewardgeneral"]["num"], result.m_objResult["message"]["rewardgeneral"]["name"])
            self.info(msg)

    def recv_task_reward(self):
        url = "/root/kfrank!recvTaskReward.action"
        result = self.get_protocol_mgr().get_xml(url, "领取对战任务奖励")
        if result and result.m_bSucceed:
            self.info("领取对战任务奖励，获得{}宝箱".format(result.m_objResult["message"]["boxnum"]))

    def recv_last_reward(self):
        url = "/root/kfrank!recvLastReward.action"
        result = self.get_protocol_mgr().get_xml(url, "领取对战上届排名奖励")
        if result and result.m_bSucceed:
            self.info("领取对战上届排名奖励，获得{}宝箱".format(result.m_objResult["message"]["boxreward"]))

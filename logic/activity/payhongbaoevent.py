# -*- coding: utf-8 -*-
# 充值送红包
from logic.activity.activity_task import ActivityTask
from model.enum.activity_type import ActivityType
from model.reward_info import RewardInfo


class PayHongBaoEvent(ActivityTask):
    def __init__(self):
        super(PayHongBaoEvent, self).__init__(ActivityType.PayHongBaoEvent)
        self.m_szName = self.__class__.__name__
        self.m_szReadable = "充值送红包"

    def run(self):
        if not self.enable():
            return self.next_half_hour()

        info = self.get_pay_hongbao_event_info()
        if info is None:
            return self.next_half_hour()

        # if info["红包"] < info["红包上限"]:
        #     self.open_pay_hongbao()
        #     return self.immediate()

        for hongbaoinfo in info["共享红包信息"]:
        #     if "rewardid" in hongbaoinfo:
        #         self.recv_share_hongbao(hongbaoinfo["rewardid"], hongbaoinfo["playerid"])
        # if int(info["共享红包信息"].get('cangetnum', 0)) > 0:
            # self.recv_share_hongbao(0, info["共享红包信息"]["playerid"])
            # return self.immediate()
            if int(hongbaoinfo.get('cangetnum', 0)) > 0:
                self.recv_share_hongbao(0, hongbaoinfo["playerid"])
                return self.immediate()

        return self.next_half_hour()

    def get_pay_hongbao_event_info(self):
        url = "/root/event!getPayHongbaoEventInfo.action"
        result = self.get_xml(url, "充值送红包")
        if result and result.m_bSucceed:
            info = dict()
            info["红包"] = int(result.m_objResult["hongbaonum"])
            info["红包上限"] = int(result.m_objResult["hongbaolimit"])
            info["福袋"] = int(result.m_objResult["luckybagnum"])
            info["共享红包信息"] = result.m_objResult.get("hongbaoinfo", [])
            if not isinstance(info["共享红包信息"], list):
                info["共享红包信息"] = [info["共享红包信息"]]
            return info

    def open_pay_hongbao(self):
        url = "/root/event!openPayHongbao.action"
        result = self.get_xml(url, "打开红包")
        if result and result.m_bSucceed:
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["hongbaoreward"]["rewardinfo"])
            self.add_reward(reward_info)
            self.info("打开红包，获得{}".format(reward_info))

    def recv_share_hongbao(self, reward_id, player_id):
        url = "/root/event!recvShareHongbao.action"
        data = {"rewardId": reward_id, "playerId": player_id}
        result = self.post_xml(url, data, "拜年")
        if result and result.m_bSucceed:
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["hongbaoreward"]["rewardinfo"])
            self.add_reward(reward_info)
            self.info("拜年，获得{}个红包 {}".format(result.m_objResult["thishongbaonum"], reward_info))

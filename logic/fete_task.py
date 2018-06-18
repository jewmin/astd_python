# -*- coding: utf-8 -*-
# 祭祀任务
from logic.base_task import BaseTask
from logic.config import config
from model.enum.activity_type import ActivityType


class FeteTask(BaseTask):
    def __init__(self):
        super(FeteTask, self).__init__()
        self.m_szName = "fete"
        self.m_szReadable = "祭祀"

    def run(self):
        if config["fete"]["auto_fete"]:
            fete_gem_task = self.m_objUser.m_dictTasks.get(3, None)
            big_fete_task = self.m_objUser.m_dictTasks.get(4, None)
            if fete_gem_task is not None and fete_gem_task.finishline == 15:
                fete_config = config["fete"]["task15"]
            elif self.m_objUser.m_dictActivities.get(ActivityType.FeteEvent, False):
                fete_config = config["fete"]["event"]
            elif big_fete_task is not None and big_fete_task.finishline == 50:
                fete_config = config["fete"]["task50"]
            else:
                fete_config = config["fete"]["common"]
            misc_mgr = self.m_objServiceFactory.get_misc_mgr()
            fete_list, free_all_fete = misc_mgr.fete()
            for item in fete_list:
                if item.gold <= fete_config.get(item.name, 0) and item.gold <= self.get_available_gold():
                    misc_mgr.do_fete(item.id, item.gold, item.name)
                    return self.immediate()
            if free_all_fete > 0:
                misc_mgr.do_fete(6, 0, "大祭祀")
                return self.immediate()

            if self.m_objUser.m_dictActivities.get(ActivityType.FeteEvent, False):
                info = self.get_fete_event_info()
                if info is not None:
                    for god in info["神"]:
                        if god["state"] == "1":
                            self.recv_fete_ticket(god)

        return self.next_half_hour()

    def get_fete_event_info(self):
        url = "/root/fete!getFeteEventInfo.action"
        result = self.m_objProtocolMgr.get_xml(url, "祭祀活动")
        if result and result.m_bSucceed:
            info = dict()
            info["神"] = result.m_objResult["god"]
            return info

    def recv_fete_ticket(self, god):
        url = "/root/fete!recvFeteTicket.action"
        data = {"feteId": god["godticket"]["id"]}
        result = self.m_objProtocolMgr.post_xml(url, data, "领取祭祀活动奖励")
        if result and result.m_bSucceed:
            self.m_objServiceFactory.get_misc_mgr().info("领取祭祀活动奖励，获得{}宝石".format(result.m_objResult["godticket"]["baoshi"]))

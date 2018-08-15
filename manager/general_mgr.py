# -*- coding: utf-8 -*-
# 武将管理
from manager.base_mgr import BaseMgr


class GeneralMgr(BaseMgr):
    def __init__(self, time_mgr, service_factory, user, index):
        super(GeneralMgr, self).__init__(time_mgr, service_factory, user, index)

    #######################################
    # general begin
    #######################################
    def get_refresh_general_info(self):
        url = "/root/general!getRefreshGeneralInfo.action"
        result = self.get_protocol_mgr().get_xml(url, "培养")
        if result and result.m_bSucceed:
            dict_info = dict()
            dict_info["免费白金洗次数"] = int(result.m_objResult["freebaijintime"])
            dict_info["免费至尊洗次数"] = int(result.m_objResult["freezizuntime"])
            dict_info["武将"] = result.m_objResult["general"]
            return dict_info

    def get_refresh_general_detail_info(self, general):
        url = "/root/general!getRefreshGeneralDetailInfo.action"
        data = {"generalId": general["generalid"]}
        result = self.get_protocol_mgr().post_xml(url, data, "培养详情")
        if result and result.m_bSucceed:
            dict_info = dict()
            dict_info["武将等级"] = int(result.m_objResult["generaldto"]["generallevel"])
            dict_info["原始属性"] = result.m_objResult["general"]["originalattr"]
            if "newattr" in result.m_objResult["general"]:
                dict_info["新属性"] = result.m_objResult["general"]["newattr"]
            return dict_info

    def refresh_general_confirm(self, general, accept):
        url = "/root/general!refreshGeneralConfirm.action"
        data = {"generalId": general["generalid"], "choose": 1 if accept else 0}
        result = self.get_protocol_mgr().post_xml(url, data, "属性确定")
        if result and result.m_bSucceed:
            self.info(result.m_objResult["message"])

    def refresh_general(self, general, model):
        url = "/root/general!refreshGeneral.action"
        data = {"generalId": general["generalid"], "refreshModel": model}
        result = self.get_protocol_mgr().post_xml(url, data, "洗属性")
        if result and result.m_bSucceed:
            dict_info = dict()
            dict_info["新属性"] = dict()
            dict_info["新属性"]["plusforces"] = result.m_objResult["general"]["plusforces"]
            dict_info["新属性"]["plusintelligence"] = result.m_objResult["general"]["plusintelligence"]
            dict_info["新属性"]["plusleader"] = result.m_objResult["general"]["plusleader"]
            return dict_info

    def get_awaken_general_info(self, general):
        url = "/root/general!getAwakenGeneralInfo.action"
        data = {"generalId": general["generalid"]}
        result = self.get_protocol_mgr().post_xml(url, data, "觉醒详情")
        if result and result.m_bSucceed:
            dict_info = dict()
            dict_info["免费觉醒酒"] = int(result.m_objResult["generalawakeinfo"]["freeliquornum"])
            dict_info["需要觉醒酒"] = int(result.m_objResult["generalawakeinfo"]["needliquornum"])
            dict_info["拥有觉醒酒"] = int(result.m_objResult["generalawakeinfo"]["liquornum"])
            dict_info["千杯佳酿需求"] = int(result.m_objResult["generalawakeinfo"]["maxnum"])
            dict_info["当前已喝"] = int(result.m_objResult["generalawakeinfo"]["invalidnum"])
            dict_info["满技能"] = result.m_objResult["generalawakeinfo"]["isfull"] == "1"
            return dict_info

    def awaken_general(self, general, need_num=0):
        url = "/root/general!awakenGeneral.action"
        data = {"generalId": general["generalid"]}
        result = self.get_protocol_mgr().post_xml(url, data, "觉醒")
        if result and result.m_bSucceed:
            msg = "免费" if need_num == 0 else "消耗{}觉醒酒".format(need_num)
            msg += "，觉醒大将{}".format(general["generalname"])
            self.info(msg)

    def use_special_liquor(self, general):
        url = "/root/general!useSpecialLiquor.action"
        data = {"generalId": general["generalid"]}
        result = self.get_protocol_mgr().post_xml(url, data, "千杯佳酿")
        if result and result.m_bSucceed:
            self.info("大将[{}]使用千杯佳酿".format(general["generalname"]))

    def get_all_big_generals(self):
        url = "/root/general!getAllBigGenerals.action"
        result = self.get_protocol_mgr().get_xml(url, "大将")
        if result and result.m_bSucceed:
            dict_info = dict()
            dict_info["大将"] = result.m_objResult["general"]
            return dict_info

    def get_big_train_info(self):
        url = "/root/general!getBigTrainInfo.action"
        result = self.get_protocol_mgr().get_xml(url, "大将训练位")
        if result and result.m_bSucceed:
            dict_info = dict()
            dict_info["经验书"] = result.m_objResult["expbook"]
            dict_info["免费次数"] = int(result.m_objResult["freenum"])
            dict_info["等级上限"] = int(result.m_objResult["maxbglv"])
            dict_info["训练位数"] = int(result.m_objResult["totalpos"])
            dict_info["训练位"] = result.m_objResult["traininfo"]
            return dict_info

    def start_big_train(self, general, pos=1):
        url = "/root/general!startBigTrain.action"
        data = {"trainPosId": pos, "generalId": general["generalid"]}
        result = self.get_protocol_mgr().post_xml(url, data, "训练大将")
        if result and result.m_bSucceed:
            self.info("训练大将[{}]".format(general["name"]))

    def fast_train_big_general(self, general, num=0):
        url = "/root/general!fastTrainBigGeneral.action"
        data = {"generalId": general["generalid"]}
        result = self.get_protocol_mgr().post_xml(url, data, "突飞大将")
        if result and result.m_bSucceed:
            self.info("花费{}大将令突飞大将[{}]".format(num, general["name"]))

    def to_big_general(self, general):
        url = "/root/general!toBigGeneral.action"
        data = {"generalId": general["generalid"]}
        result = self.get_protocol_mgr().post_xml(url, data, "转生成大将")
        if result and result.m_bSucceed:
            self.info("武将[{}]转生成大将".format(general["name"]))

    def big_general_change(self, general):
        url = "/root/general!bigGeneralChange.action"
        data = {"generalId": general["generalid"]}
        result = self.get_protocol_mgr().post_xml(url, data, "晋升大将")
        if result and result.m_bSucceed:
            self.info("大将[{}]晋升为大将军".format(general["name"]))

    def new_train_big_general(self, general):
        url = "/root/general!newTrainBigGeneral.action"
        data = {"generalId": general["generalid"]}
        result = self.get_protocol_mgr().post_xml(url, data, "突破大将")
        if result and result.m_bSucceed:
            self.info("对大将[{}]进行突破".format(general["name"]))

    def use_exp_book(self, general):
        url = "/root/general!useExpBook.action"
        data = {"generalId": general["generalid"]}
        result = self.get_protocol_mgr().post_xml(url, data, "使用经验书")
        if result and result.m_bSucceed:
            self.info("使用经验书突飞大将[{}]".format(general["name"]))

    def formation(self):
        url = "/root/general!formation.action"
        result = self.get_protocol_mgr().get_xml(url, "阵型")
        if result and result.m_bSucceed:
            formation_id = int(result.m_objResult["formation"]["formationid"])
            if formation_id > 0:
                formation_id /= 20
                return self.get_formation_by_id(formation_id)
        return self.get_formation_by_id(0)

    def save_default_formation(self, formation):
        formation_id = self.get_formation_by_name(formation)
        if formation_id > 0:
            formation_id *= 20
            url = "/root/general!saveDefaultFormation.action"
            data = {"formationId": formation_id}
            result = self.get_protocol_mgr().post_xml(url, data, "设置默认阵型")
            if result and result.m_bSucceed:
                self.info("设置默认阵型为{}".format(formation))
            else:
                self.info(result.m_szError)

    #######################################
    # tech begin
    #######################################
    def get_new_tech(self):
        url = "/root/tech!getNewTech.action"
        result = self.get_protocol_mgr().get_xml(url, "科技")
        if result and result.m_bSucceed:
            dict_info = dict()
            dict_info["科技"] = result.m_objResult["technology"]
            dict_info["可用宝石"] = int(result.m_objResult["baoshi18num"])
            dict_info["可用镔铁"] = int(result.m_objResult["bintienum"])
            dict_info["可用点券"] = int(result.m_objResult["ticketsnum"])
            return dict_info

    def research_new_tech(self, tech):
        url = "/root/tech!researchNewTech.action"
        data = {"techId": tech["techid"]}
        result = self.get_protocol_mgr().post_xml(url, data, "研究科技")
        if result and result.m_bSucceed:
            self.info("消耗{}{}，研究科技[{}]，进度+{}".format(tech["consumenum"], self.get_tech_consume_name(tech["consumerestype"]), tech["techname"], result.m_objResult["addprogress"]))

    @staticmethod
    def get_tech_consume_name(consume_res_type):
        if consume_res_type == "bintie":
            return "镔铁"
        elif consume_res_type == "baoshi_18":
            return "宝石lv.18"
        elif consume_res_type == "tickets":
            return "点券"
        else:
            return consume_res_type

# -*- coding: utf-8 -*-
# 装备管理
from manager.base_mgr import BaseMgr
from model.reward_info import RewardInfo


class EquipMgr(BaseMgr):
    def __init__(self, time_mgr, service_factory, user, index):
        super(EquipMgr, self).__init__(time_mgr, service_factory, user, index)
        self.m_nMagic = 100

    #######################################
    # warChariot begin
    #######################################
    def get_war_chariot_info(self):
        url = "/root/warChariot!getWarChariotInfo.action"
        result = self.get_protocol_mgr().get_xml(url, "战车")
        if result and result.m_bSucceed:
            dict_info = dict()
            dict_info["当前等级"] = int(result.m_objResult["equiplevel"])
            dict_info["可提升等级"] = int(result.m_objResult["needtofull"])
            dict_info["升级"] = result.m_objResult["islaststrengthenflag"] == "1"
            dict_info["总进度"] = int(result.m_objResult["total"])
            dict_info["当前进度"] = int(result.m_objResult["upgradeeffectnum"])
            dict_info["普通强化进度"] = int(result.m_objResult["upgradenum"])
            dict_info["库存玉石"] = int(result.m_objResult["bowlder"]) / 1000
            dict_info["消耗玉石"] = int(result.m_objResult["needbowlder"])
            dict_info["库存兵器"] = int(result.m_objResult["equipitemnum"])
            dict_info["消耗兵器"] = int(result.m_objResult["needequipitem"])
            dict_info["铁锤列表"] = result.m_objResult["hammer"]
            return dict_info

    def strengthen_war_chariot(self, chui_zi_cri, tips):
        url = "/root/warChariot!strengthenWarChariot.action"
        data = {"chuiziCri": chui_zi_cri}
        result = self.get_protocol_mgr().post_xml(url, data, "强化战车")
        if result and result.m_bSucceed:
            dict_info = dict()
            dict_info["总进度"] = int(result.m_objResult["total"])
            dict_info["当前进度"] = int(result.m_objResult["upgradeeffectnum"])
            dict_info["使用铁锤"] = result.m_objResult["chuizi"] == "1"
            dict_info["进度"] = int(result.m_objResult["isbaoji"])
            dict_info["余料"] = int(result.m_objResult["surplus"])
            hammer_tips = "使用铁锤，" if dict_info["使用铁锤"] else ""
            msg = "{}，{}强化战车，进度+{}，{}/{}，余料+{}".format(tips, hammer_tips, dict_info["进度"], dict_info["当前进度"], dict_info["总进度"], dict_info["余料"])
            self.info(msg)
            return True
        else:
            self.info("强化战车报错：{}".format(result.m_szError))
            return False

    #######################################
    # equip begin
    #######################################
    def get_special_equip_cast_info(self):
        url = "/root/equip!getSpecialEquipCastInfo.action"
        result = self.get_protocol_mgr().get_xml(url, "装备铸造")
        if result and result.m_bSucceed:
            dict_info = dict()
            dict_info["免费铸造次数"] = int(result.m_objResult["freetimes"])
            dict_info["铸造消耗金币"] = int(result.m_objResult["firstcost"])
            dict_info["精火铸造消耗金币"] = int(result.m_objResult["secondcost"])
            dict_info["总进度"] = int(result.m_objResult["maxprogress"])
            dict_info["当前进度"] = int(result.m_objResult["progress"])
            self.info("铸造进度：{}/{}，免费铸造次数：{}".format(dict_info["当前进度"], dict_info["总进度"], dict_info["免费铸造次数"]))
            return dict_info

    def special_equip_cast(self, cast_type, msg):
        url = "/root/equip!specialEquipCast.action"
        data = {"type": cast_type}
        result = self.get_protocol_mgr().post_xml(url, data, "铸造")
        if result and result.m_bSucceed:
            msg += "，获得 "
            if isinstance(result.m_objResult["specialequipcast"], list):
                for special_equip_cast in result.m_objResult["specialequipcast"]:
                    reward_info = RewardInfo()
                    reward_info.handle_info(special_equip_cast["rewardinfo"])
                    msg += "{} ".format(reward_info)
            else:
                special_equip_cast = result.m_objResult["specialequipcast"]
                reward_info = RewardInfo()
                reward_info.handle_info(special_equip_cast["rewardinfo"])
                msg += "{} ".format(reward_info)
            self.info(msg)

    def get_upgrade_info(self):
        url = "/root/equip!getUpgradeInfo.action"
        result = self.get_protocol_mgr().get_xml(url, "装备强化")
        if result and result.m_bSucceed:
            self.m_nMagic = int(result.m_objResult["magic"])
            self.info("强化魔力值：{}".format(self.m_nMagic))

    #######################################
    # polish begin
    #######################################
    def get_bao_wu_polish_info(self):
        url = "/root/polish!getBaowuPolishInfo.action"
        result = self.get_protocol_mgr().get_xml(url, "炼化")
        if result and result.m_bSucceed:
            dict_info = dict()
            dict_info["炼化机会"] = int(result.m_objResult["num"])
            dict_info["专属玉佩"] = result.m_objResult["specialtreasure"]
            dict_info["家传玉佩"] = result.m_objResult["baowu"]
            return dict_info

    def polish(self, baowu, use_gold=False):
        url = "/root/polish!polish.action"
        data = {"storeId": baowu["storeid"]}
        result = self.get_protocol_mgr().post_xml(url, data, "玉佩炼化")
        if result and result.m_bSucceed:
            old_attribute_base = int(baowu["attribute_base"])
            baowu["polishtimes"] = result.m_objResult["baowu"]["polishtimes"]
            baowu["attribute_base"] = result.m_objResult["baowu"]["attribute_base"]
            baowu["gold"] = result.m_objResult["baowu"]["gold"]
            diff_attribute_base = int(baowu["attribute_base"]) - old_attribute_base
            msg = "炼化玉佩，"
            if diff_attribute_base > 0:
                msg += "属性+{}".format(diff_attribute_base)
            else:
                msg += "属性无变化"
            self.info(msg, use_gold)
            return True
        else:
            self.info("炼化玉佩报错：{}".format(result.m_szError))
            return False

    def consecrate_special_treasure(self, special_treasure):
        url = "/root/polish!consecrateSpecialTreasure.action"
        data = {"storeId": special_treasure["storeid"]}
        result = self.get_protocol_mgr().post_xml(url, data, "专属玉佩开光")
        if result and result.m_bSucceed:
            msg = "专属玉佩开光"
            if "additionalattribute" in result.m_objResult:
                msg += "，激活属性"
                special_treasure["additionalattribute"] = {"attribute": list()}
                for attribute in result.m_objResult["additionalattribute"]:
                    special_treasure["additionalattribute"]["attribute"].append(":".join(attribute["attribute"], attribute["name"], attribute["lv"], attribute["value"]))
                    msg += "，{}".format(attribute["name"])
            self.info(msg)

    def evolve_special_treasure(self, special_treasure):
        url = "/root/polish!evolveSpecialTreasure.action"
        data = {"storeId": special_treasure["storeid"]}
        result = self.get_protocol_mgr().post_xml(url, data, "专属玉佩进化")
        if result and result.m_bSucceed:
            self.info("专属玉佩进化")

    def upgrade_baowu(self, special_treasure, baowu, is_special_treasure=False):
        url = "/root/polish!upgradeBaowu.action"
        data = {"storeId": special_treasure["storeid"], "storeId2": baowu["storeid"]}
        desc = "家传玉佩"
        if is_special_treasure:
            data["type"] = 2
            desc = "专属玉佩"
        result = self.get_protocol_mgr().post_xml(url, data, "玉佩升级")
        if result and result.m_bSucceed:
            self.info("{}升级成功".format(desc))
            return True
        else:
            self.info("{}升级报错：{}".format(desc, result.m_szError))
            return False

    #######################################
    # stoneMelt begin
    #######################################
    def melt(self, baowu, is_special_treasure=False):
        url = "/root/stoneMelt!melt.action"
        data = {"gold": 0, "meltGold": 0, "magic": self.m_nMagic, "storeId": baowu["storeid"]}
        if is_special_treasure:
            data["type"] = 2
        else:
            data["type"] = 1
        result = self.get_protocol_mgr().post_xml(url, data, "熔化")
        if result and result.m_bSucceed:
            self.info("熔化[{}(统+{} 勇+{} 智+{})]，获得{}玉石".format(baowu["name"], baowu["attribute_lea"], baowu["attribute_str"], baowu["attribute_int"], result.m_objResult.get("gainbowlder", "0")))

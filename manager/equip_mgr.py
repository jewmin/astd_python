# -*- coding: utf-8 -*-
# 装备管理
from manager.base_mgr import BaseMgr
from model.reward_info import RewardInfo
from model.global_func import GlobalFunc


class EquipMgr(BaseMgr):
    def __init__(self, time_mgr, service_factory, user, index):
        super(EquipMgr, self).__init__(time_mgr, service_factory, user, index)
        self.m_nMagic = 100
        self.m_nMoliStone = 0
        self.m_nTicketNumber = 0
        self.m_nMaxTaoZhuangLv = 0

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
            dict_info["使用铁锤"] = result.m_objResult.get("chuizi", "0") == "1"
            dict_info["进度"] = int(result.m_objResult.get("isbaoji", "0"))
            dict_info["余料"] = int(result.m_objResult.get("surplus", "0"))
            if dict_info["进度"] == 0:
                msg = "战车升级"
            else:
                hammer_tips = "使用铁锤，" if dict_info["使用铁锤"] else ""
                msg = "{}，{}强化战车，进度+{}，{}/{}，余料+{}".format(tips, hammer_tips, dict_info["进度"], dict_info["当前进度"], dict_info["总进度"], dict_info["余料"])
            self.info(msg)
            return True
        else:
            self.warning("强化战车报错：{}".format(result.m_szError))
            return False

    #######################################
    # warDrum begin
    #######################################
    def get_war_drum_info(self):
        url = "/root/warDrum!getWarDrumInfo.action"
        result = self.get_protocol_mgr().get_xml(url, "战鼓")
        if result and result.m_bSucceed:
            dict_info = dict()
            dict_info["最大等级"] = int(result.m_objResult["maxupdatelevel"])
            dict_info["库存点券"] = int(result.m_objResult["ticketnum"])
            dict_info["库存玉石"] = int(result.m_objResult["bowldernum"])
            dict_info["库存镔铁"] = int(result.m_objResult["steelnum"])
            dict_info["最大战鼓等级"] = 0
            dict_info["最小战鼓等级"] = 0
            dict_info["战鼓列表"] = dict()
            for war_drum in result.m_objResult["getwardruminfo"]["wardrum"]:
                war_drum_info = dict()
                war_drum_info["名称"] = war_drum["name"]
                war_drum_info["类型"] = int(war_drum["type"])
                war_drum_info["当前等级"] = int(war_drum["drumlevel"])
                war_drum_info["特殊等级"] = int(war_drum["speciallevel"])
                war_drum_info["最大特殊等级"] = int(war_drum["maxspeciallevel"])
                war_drum_info["消耗镔铁"] = int(war_drum["needsteelnum"])
                war_drum_info["消耗玉石"] = int(war_drum["needbowldernum"])
                war_drum_info["消耗点券"] = int(war_drum["needticketnum"])
                war_drum_info["当前进度"] = int(war_drum["effectnum"])
                war_drum_info["总进度"] = int(war_drum["totalnum"])
                dict_info["战鼓列表"][war_drum_info["类型"]] = war_drum_info
                if dict_info["最大战鼓等级"] < war_drum_info["当前等级"]:
                    dict_info["最大战鼓等级"] = war_drum_info["当前等级"]
                if dict_info["最小战鼓等级"] > war_drum_info["当前等级"]:
                    dict_info["最小战鼓等级"] = war_drum_info["当前等级"]
            dict_info["最大等级差"] = dict_info["最大战鼓等级"] - dict_info["最小战鼓等级"]
            return dict_info

    def strengthen_war_drum(self, drum_type):
        url = "/root/warDrum!strengthenWarDrum.action"
        data = {"type": drum_type}
        result = self.get_protocol_mgr().post_xml(url, data, "强化战鼓")
        if result and result.m_bSucceed:
            dict_info = dict()
            dict_info["战鼓"] = result.m_objResult["wardrumdto"]["name"]
            dict_info["当前进度"] = int(result.m_objResult["wardrumdto"]["effectnum"])
            dict_info["总进度"] = int(result.m_objResult["wardrumdto"]["totalnum"])
            dict_info["进度"] = int(result.m_objResult.get("crits", "0"))
            dict_info["余料"] = int(result.m_objResult.get("surplus", "0"))
            if dict_info["当前进度"] == 0:
                msg = "战鼓升级"
            else:
                msg = "强化战鼓[{}]，进度+{}，{}/{}，余料+{}".format(dict_info["战鼓"], dict_info["进度"], dict_info["当前进度"], dict_info["总进度"], dict_info["余料"])
            self.info(msg)
            return True
        else:
            self.warning("强化战鼓报错：{}".format(result.m_szError))
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
            dict_info["免费神火铸造次数"] = int(result.m_objResult["times"])
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

    def get_crystal(self):
        url = "/root/equip!getCrystal.action"
        result = self.get_protocol_mgr().get_xml(url, "水晶石")
        if result and result.m_bSucceed:
            dict_info = dict()
            dict_info["水晶石"] = result.m_objResult["baoshidto"]
            return dict_info

    def upgrade_crystal(self, baoshidto):
        url = "/root/equip!upgradeCrystal.action"
        data = {"storeId": baoshidto["storeid"]}
        result = self.get_protocol_mgr().post_xml(url, data, "水晶石进阶")
        if result and result.m_bSucceed:
            self.info("水晶石lv.{}[{}({})]进阶成功".format(baoshidto["baoshilevel"], baoshidto["goodsname"], baoshidto["generalname"]))
            return True
        else:
            self.warning("水晶石进阶报错：{}".format(result.m_szError))
            return False

    def get_upgrade_info(self, show=False):
        url = "/root/equip!getUpgradeInfo.action"
        result = self.get_protocol_mgr().get_xml(url, "套装")
        if result and result.m_bSucceed:
            self.m_nMagic = int(result.m_objResult["magic"])
            self.m_nMoliStone = int(result.m_objResult["molistone"])
            self.m_nTicketNumber = int(result.m_objResult["ticketnumber"])
            self.m_nMaxTaoZhuangLv = int(result.m_objResult["taozhuang"]["maxtaozhuanglv"])
            dict_info = dict()
            dict_info["套装"] = result.m_objResult["playerequipdto"]
            self.info("魔力值：{}，磨砺石：{}，点券：{}".format(self.m_nMagic, self.m_nMoliStone, GlobalFunc.get_short_readable(self.m_nTicketNumber)))
            if show:
                for equipdto in dict_info["套装"]:
                    power = equipdto["powerstr"].split(";")
                    self.info("套装[id={} name={} general={} 强攻({}/{}) 强防({}/{})]".format(equipdto["composite"], equipdto["equipname"], equipdto["generalname"], power[0], equipdto["attfull"], power[1], equipdto["deffull"]))
            return dict_info

    def upgrade_monkey_tao(self, equipdto, num=0):
        url = "/root/equip!upgradeMonkeyTao.action"
        data = {"composite": equipdto["composite"], "num": num}
        result = self.get_protocol_mgr().post_xml(url, data, "套装强化")
        if result and result.m_bSucceed:
            self.m_nTicketNumber = int(result.m_objResult["changeinfo"]["remaintickets"])
            equipdto["tickets"] = result.m_objResult["changeinfo"]["tickets"]
            equipdto["ticketsstatus"] = result.m_objResult["changeinfo"]["ticketsstatus"]
            equipdto["canupgrade"] = result.m_objResult["changeinfo"]["canupgrade"]
            if "xuli" in result.m_objResult["changeinfo"]:
                equipdto["xuli"] = result.m_objResult["changeinfo"]["xuli"]
            msg = "套装强化，{}倍暴击".format(result.m_objResult["baoji"])
            if isinstance(result.m_objResult["addinfo"], list):
                for addinfo in result.m_objResult["addinfo"]:
                    msg += "，{}+{}".format(addinfo["name"], addinfo["val"])
            else:
                msg += "，{}+{}".format(result.m_objResult["addinfo"]["name"], result.m_objResult["addinfo"]["val"])
            self.info(msg)

    def use_xuli(self, equipdto):
        url = "/root/equip!useXuli.action"
        data = {"composite": equipdto["composite"]}
        result = self.get_protocol_mgr().post_xml(url, data, "套装蓄力")
        if result and result.m_bSucceed:
            msg = "套装蓄力"
            if "addinfo" in result.m_objResult["xuliinfo"]:
                addinfo = result.m_objResult["xuliinfo"]["addinfo"]
                msg += "，{}+{}".format(addinfo["name"], addinfo["val"])
            if "gethighnum" in result.m_objResult["xuliinfo"]:
                msg += "，高效次数+{}".format(result.m_objResult["xuliinfo"]["gethighnum"])
            self.info(msg)

    def get_all_special_equip(self):
        url = "/root/equip!getAllSpecialEquip.action"
        result = self.get_protocol_mgr().get_xml(url, "专属仓库")
        if result and result.m_bSucceed:
            dict_info = dict()
            dict_info["专属"] = result.m_objResult["equipdto"]
            return dict_info

    def smelt_special_equip(self, equipdto, is_all=1):
        url = "/root/equip!smeltSpecialEquip.action"
        data = {"specialId": equipdto["storeid"], "all": is_all}
        result = self.get_protocol_mgr().post_xml(url, data, "熔炼专属")
        if result and result.m_bSucceed:
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["rewardinfo"])
            self.info("熔炼专属[{}]lv.{}，获得{}".format(equipdto["equipname"], equipdto["equiplevel"], reward_info))

    def get_equip(self):
        url = "/root/equip!getEquip.action"
        result = self.get_protocol_mgr().get_xml(url, "武将装备")
        if result and result.m_bSucceed:
            dict_info = dict()
            dict_info["诸葛套装"] = result.m_objResult["general"]
            return dict_info

    def get_xi_zhuge_info(self, general):
        url = "/root/equip!getXiZhugeInfo.action"
        data = {"generalId": general["generalid"]}
        result = self.get_protocol_mgr().post_xml(url, data, "淬炼详情")
        if result and result.m_bSucceed:
            dict_info = dict()
            dict_info["免费淬炼次数"] = int(result.m_objResult.get("freenum", "0"))
            dict_info["最大属性"] = int(result.m_objResult["maxattr"])
            dict_info["当前属性"] = result.m_objResult["curattr"]
            if isinstance(result.m_objResult["newattr"], dict):
                dict_info["新属性"] = result.m_objResult["newattr"]
            return dict_info

    def xi_zhu_ge(self, general):
        url = "/root/equip!xiZhuge.action"
        data = {"storeId": general["zhugeid"]}
        result = self.get_protocol_mgr().post_xml(url, data, "淬炼")
        if result and result.m_bSucceed:
            attrs = result.m_objResult["newattr"].split(",")
            dict_info = dict()
            dict_info["新属性"] = {"int": attrs[0], "lea": attrs[1], "str": attrs[2]}
            return dict_info

    def xi_zhu_ge_confirm(self, general, accept):
        url = "/root/equip!xiZhugeConfirm.action"
        data = {"storeId": general["zhugeid"], "type": 1 if accept else 2}
        result = self.get_protocol_mgr().post_xml(url, data, "淬炼确认")
        if result and result.m_bSucceed:
            self.info("淬炼成功，替换属性" if accept else "淬炼失败，保持原样")

    def moli(self):
        url = "/root/equip!moli.action"
        data = {"composite": 0, "num": 0}
        result = self.get_protocol_mgr().post_xml(url, data, "套装磨砺")
        if result and result.m_bSucceed:
            pass

    def update_baoshi_whole_level(self, gem_level):
        url = "/root/equip!updateBaoshiWholeLevel.action"
        data = {"baoshiId": gem_level}
        result = self.get_protocol_mgr().post_xml(url, data, "同级合成")
        if result and result.m_bSucceed:
            self.info("{}个{}级宝石合成{}个{}级宝石".format(result.m_objResult["num"], result.m_objResult["baoshilevel"], result.m_objResult["numup"], result.m_objResult["baoshilevelup"]))

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
            self.warning("炼化玉佩报错：{}".format(result.m_szError))
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
                    special_treasure["additionalattribute"]["attribute"].append(":".join([attribute["attribute"], attribute["name"], attribute["lv"], attribute["value"]]))
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
        if "generalname" in special_treasure:
            desc += "[{}]".format(special_treasure["generalname"])
        result = self.get_protocol_mgr().post_xml(url, data, "玉佩升级")
        if result and result.m_bSucceed:
            if result.m_objResult.get("upgraderesult", "0") == "1":
                self.info("{}升级成功，统+{} 勇+{} 智+{}".format(desc, result.m_objResult.get("succlea", "0"), result.m_objResult.get("succstr", "0"), result.m_objResult.get("succint", "0")))
            else:
                self.info("{}升级失败".format(desc))
            return True
        else:
            self.warning("{}升级报错：{}".format(desc, result.m_szError))
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

    #######################################
    # goods begin
    #######################################
    def open_store_house(self):
        url = "/root/goods!openStorehouse.action"
        result = self.get_protocol_mgr().get_xml(url, "仓库")
        if result and result.m_bSucceed:
            dict_info = dict()
            dict_info["使用"] = int(result.m_objResult["usesize"])
            dict_info["总量"] = int(result.m_objResult["storesize"])
            dict_info["物品"] = result.m_objResult["storehousedto"]
            return dict_info

    def draw(self, storehousedto):
        url = "/root/goods!draw.action"
        data = {"baoshiLv": 0, "count": 1, "goodsId": storehousedto["id"]}
        result = self.get_protocol_mgr().post_xml(url, data, "取出物品")
        if result and result.m_bSucceed:
            if "equipname" in storehousedto:
                name = storehousedto["equipname"]
            else:
                name = storehousedto["name"]
            self.info("从临时仓库拿取物品[{}]".format(name))

# -*- coding: utf-8 -*-
# 武将任务
from logic.base_task import BaseTask
from logic.config import config


class GeneralTask(BaseTask):
    def __init__(self):
        super(GeneralTask, self).__init__()
        self.m_szName = "general"
        self.m_szReadable = "武将"

    def run(self):
        general_mgr = self.m_objServiceFactory.get_general_mgr()

        # generalid generalname ishave online isawaken
        dict_info = general_mgr.get_refresh_general_info()
        if dict_info is not None:
            awaken_generals = list()
            left_awaken = 0
            for general in dict_info["武将"]:
                if "generalname" not in general or general["online"] == "1":
                    continue

                if config["general"]["wash"]["enable"] and (dict_info["免费白金洗次数"] > 0 or dict_info["免费至尊洗次数"] > 0):
                    detail = general_mgr.get_refresh_general_detail_info(general)
                    if detail is not None:
                        if "新属性" in detail:
                            self.refresh_general_confirm(general, detail["原始属性"], detail["新属性"])
                            return self.immediate()

                        limit_attr = detail["武将等级"] + 20
                        if detail["武将等级"] == 400:
                            limit_attr = self.m_objUser.m_nLevel + 20

                        for value in detail["原始属性"].itervalues():
                            if limit_attr - int(value) > 1:
                                if dict_info["免费白金洗次数"] > 0:
                                    result = general_mgr.refresh_general(general, 2)
                                else:
                                    result = general_mgr.refresh_general(general, 3)
                                if result is not None:
                                    self.refresh_general_confirm(general, detail["原始属性"], result["新属性"])
                                return self.immediate()

                # isfull maxlevel liquornum freeliquornum needliquornum needbaoshinum isawaken maxnum invalidnum
                if config["general"]["awaken"]["enable"]:
                    if general.get("awaken2", "0") == "1" and general["generalname"] in config["general"]["awaken"]["general2"]:
                        detail = general_mgr.get_awaken2_info(general)
                        if detail is None:
                            continue
                        if detail["满技能"]:
                            continue
                        if detail["未觉醒"] or not config["general"]["awaken"]["only_awaken2"]:
                            if detail["当前已喝"] >= detail["千杯佳酿需求"]:
                                general_mgr.use_special_liquor(general)
                                return self.immediate()
                            if config["general"]["awaken"]["use_stone2"] and detail["剩余杜康酒"] >= detail["每次消耗杜康酒"]:
                                general_mgr.awaken_general2(general, detail["每次消耗杜康酒"])
                                return self.immediate()
                    elif "isawaken" in general and general["generalname"] in config["general"]["awaken"]["general"]:
                        detail = general_mgr.get_awaken_general_info(general)
                        if detail is None:
                            continue
                        if detail["满技能"]:
                            continue
                        if general["isawaken"] == "0" or not config["general"]["awaken"]["only_awaken"]:
                            if detail["当前已喝"] >= detail["千杯佳酿需求"]:
                                general_mgr.use_special_liquor(general)
                                return self.immediate()
                            if detail["免费觉醒酒"] >= detail["需要觉醒酒"]:
                                general_mgr.awaken_general(general)
                                return self.immediate()
                            elif config["general"]["awaken"]["use_stone"] and detail["拥有觉醒酒"] >= detail["需要觉醒酒"]:
                                general_mgr.awaken_general(general, detail["需要觉醒酒"])
                                return self.immediate()
                        else:
                            left_awaken = detail["免费觉醒酒"]
                            awaken_generals.append((general, detail))
            if left_awaken > 0:
                for general, detail in awaken_generals:
                    if detail["当前已喝"] >= detail["千杯佳酿需求"]:
                        general_mgr.use_special_liquor(general)
                        return self.immediate()
                    if left_awaken >= detail["需要觉醒酒"]:
                        general_mgr.awaken_general(general)
                        return self.immediate()

        # techid techname techlevel progress requireprogress consumerestype('bintie','baoshi_18','tickets') consumenum
        if config["general"]["tech"]["enable"]:
            dict_info = general_mgr.get_new_tech()
            if dict_info is not None:
                upgrade = False
                for tech in dict_info["科技"]:
                    if tech["techname"] not in config["general"]["tech"]["list"]:
                        continue
                    elif int(tech["techlevel"]) >= 5:
                        continue
                    elif tech["consumerestype"] == "tickets":
                        if int(tech["consumenum"]) > self.get_available_tickets():
                            continue
                    elif tech["consumerestype"] == "bintie":
                        if int((tech["consumenum"])) > dict_info["可用镔铁"]:
                            continue
                    elif tech["consumerestype"] == "baoshi_18":
                        if int((tech["consumenum"])) > dict_info["可用宝石"]:
                            continue
                    general_mgr.research_new_tech(tech)
                    upgrade = True

                if upgrade:
                    return self.immediate()

        # big biglv generalid generallv istop name num
        # pos biglv generalid generaltype change name num
        if config["general"]["big"]["enable"]:
            dict_info = general_mgr.get_all_big_generals()
            train_info = general_mgr.get_big_train_info()
            if dict_info is not None and train_info is not None:
                big_config = config["general"]["big"]
                dict_info["待转生大将"] = list()
                dict_info["待突破大将"] = list()
                dict_info["待突飞大将"] = list()
                for i in range(len(dict_info["大将"]) - 1, -1, -1):
                    general = dict_info["大将"][i]
                    general["biglv"] = int(general["biglv"])
                    general["num"] = int(general["num"])
                    if general["big"] == "0":
                        dict_info["待转生大将"].append(general)
                    elif general["num"] > 0:
                        if general["biglv"] == train_info["等级上限"]:
                            dict_info["待突破大将"].append(general)
                        else:
                            dict_info["待突飞大将"].append(general)

                for general in dict_info["待转生大将"]:
                    general_mgr.to_big_general(general)

                pos = 1
                for general in dict_info["待突破大将"]:
                    general_mgr.start_big_train(general, pos)
                    pos += 1
                    if pos > train_info["训练位数"]:
                        pos = 1
                        self.train_general(train_info["训练位数"], big_config["new_train"])
                if pos > 1:
                    self.train_general(pos - 1, big_config["new_train"])

                for general in dict_info["待突飞大将"]:
                    if general["num"] >= big_config["fast_train"]:
                        general_mgr.start_big_train(general)
                        while general["num"] >= big_config["fast_train"]:
                            general_mgr.fast_train_big_general(general, big_config["fast_train"])
                            general["num"] -= big_config["fast_train"]

                dict_info = general_mgr.get_all_big_generals()
                for i in range(len(dict_info["大将"]) - 1, -1, -1):
                    general = dict_info["大将"][i]
                    if int(general["biglv"]) == train_info["等级上限"]:
                        dict_info["大将"].remove(general)
                    else:
                        general["index"] = big_config["dict"].get(general["name"], 9999)
                dict_info["大将"] = sorted(dict_info["大将"], key=lambda obj: obj["index"])
                pos = 1
                for general in dict_info["大将"]:
                    general_mgr.start_big_train(general, pos)
                    pos += 1
                    if pos > train_info["训练位数"]:
                        break

                train_info = general_mgr.get_big_train_info()
                for expbook in train_info["经验书"]:
                    expbook["num"] = int(expbook["num"])
                for train in train_info["训练位"]:
                    while train_info["免费次数"] >= big_config["fast_train"]:
                        general_mgr.fast_train_big_general(train)
                        train_info["免费次数"] -= big_config["fast_train"]
                    for expbook in train_info["经验书"]:
                        if expbook["type"] == train["generaltype"] and expbook["num"] > 0:
                            general_mgr.use_exp_book(train)
                            expbook["num"] -= 1

        return self.next_half_hour()

    def refresh_general_confirm(self, general, old_attrs, new_attrs):
        general_mgr = self.m_objServiceFactory.get_general_mgr()
        old_total_attr = 0
        new_total_attr = 0
        for value in old_attrs.itervalues():
            old_total_attr += int(value)
        for value in new_attrs.itervalues():
            new_total_attr += int(value)
        general_mgr.refresh_general_confirm(general, new_total_attr > old_total_attr)

    def train_general(self, num, new_train):
        general_mgr = self.m_objServiceFactory.get_general_mgr()
        train_info = general_mgr.get_big_train_info()
        if train_info is None:
            return
        for train in train_info["训练位"]:
            if num > 0:
                num -= 1
                if train["change"] == "0":
                    general_mgr.big_general_change(train)
                else:
                    train["num"] = int(train["num"])
                    while train["num"] > new_train:
                        general_mgr.new_train_big_general(train)
                        train["num"] -= new_train

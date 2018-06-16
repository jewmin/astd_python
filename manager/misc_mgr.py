# -*- coding: utf-8 -*-
# 杂七杂八管理
from manager.base_mgr import BaseMgr
from model.fete import Fete
from model.reward_info import RewardInfo
from model.global_func import GlobalFunc
from model.supper_market_dto import SupperMarketDto
from model.supper_market_dto import SupperMarketSpecialDto
from model.ticket import Ticket
from logic.config import config
from manager.time_mgr import TimeMgr


class MiscMgr(BaseMgr):
    def __init__(self, time_mgr, service_factory, user, index):
        super(MiscMgr, self).__init__(time_mgr, service_factory, user, index)

    #######################################
    # server begin
    #######################################
    def get_server_time(self):
        url = "/root/server!getServerTime.action"
        result = self.get_protocol_mgr().get_xml(url, "获取系统时间")
        if result and result.m_bSucceed:
            server_time = int(result.m_objResult["time"])
            self.m_objTimeMgr.set_timestamp(server_time)
            self.debug("got timestamp = {}".format(server_time))

    def get_player_info_by_user_id(self, role_name):
        url = "/root/server!getPlayerInfoByUserId.action"
        result = self.get_protocol_mgr().get_xml(url, "获取玩家信息")
        if result is None or not result.m_bSucceed:
            self.warning("获取用户信息失败，请重试")
            return False

        # 选择角色
        if result.m_objResult.get("op", "") == "xzjs":
            code = result.m_objResult["code"]
            for v in result.m_objResult["player"]:
                if role_name == v["playername"]:
                    player_id = v["playerid"]
                    break
            if player_id is None:
                self.warning("您选择的角色不存在")
                return False

            if not self.choose_role(player_id, code):
                self.warning("切换角色失败")
                return False

            result = self.get_protocol_mgr().get_xml(url, "获取玩家信息")
            if result is None or not result.m_bSucceed:
                self.warning("获取用户信息失败，请重试")
                return False

        if "blockreason" in result.m_objResult:
            self.warning("角色被封号，原因是：{}".format(result.m_objResult["blockreason"]))
            return False

        self.m_objUser.clear_activities()
        if "player" in result.m_objResult:
            self.m_objUser.refresh_player_info(result.m_objResult["player"])
        else:
            self.m_objUser.refresh_player_info(result.m_objResult["message"]["player"])
        if "limitvalue" in result.m_objResult:
            self.m_objUser.update_limits(result.m_objResult["limitvalue"])
        else:
            self.m_objUser.update_limits(result.m_objResult["message"]["limitvalue"])

        self.info(str(self.m_objUser))

        if self.m_objUser.m_bHasVersionGift:
            self.get_service_factory().get_city_mgr().get_update_reward()

        return True

    def choose_role(self, player_id, code):
        url = "/root/server!chooseRole.action"
        data = {"playerId": player_id, "code": code}
        result = self.get_protocol_mgr().post_xml(url, data, "选择玩家角色")
        if result and result.m_bSucceed:
            self.info("选择角色成功")
            return True

    def get_extra_info(self):
        url = "/root/server!getExtraInfo.action"
        result = self.get_protocol_mgr().get_xml(url, "获取玩家额外信息")
        if result and result.m_bSucceed:
            self.m_objUser.update_player_extra_info(result.m_objResult["player"])

    def get_player_extra_info2(self):
        url = "/root/server!getPlayerExtraInfo2.action"
        result = self.get_protocol_mgr().get_xml(url, "获取玩家额外信息")
        if result and result.m_bSucceed:
            self.m_objUser.update_player_extra_info2(result.m_objResult["player"])

    #######################################
    # newGift begin
    #######################################
    def get_new_gift_list(self):
        url = "/root/newGift!getNewGiftList.action"
        data = {"type": 1}
        result = self.get_protocol_mgr().post_xml(url, data, "礼包")
        if result and result.m_bSucceed:
            if "weekendgift" in result.m_objResult:
                self.get_new_gift_reward(result.m_objResult["weekendgift"]["id"])
            if "gift" in result.m_objResult:
                if result.m_objResult["gift"]["intime"] == "1" and result.m_objResult["gift"]["statuts"] == "0":
                    self.get_new_gift_reward(result.m_objResult["gift"]["id"])

    def get_new_gift_reward(self, gift_id):
        url = "/root/newGift!getNewGiftReward.action"
        data = {"giftId": gift_id}
        result = self.get_protocol_mgr().post_xml(url, data, "领取礼包")
        if result and result.m_bSucceed:
            content = result.m_objResult.get("content", "无效奖励")
            self.info("领取礼包，获得{}".format(content))

    #######################################
    # fete begin
    #######################################
    def fete(self):
        fete_list = list()
        free_all_fete = 0
        url = "/root/fete.action"
        result = self.get_protocol_mgr().get_xml(url, "祭祀神庙")
        if result and result.m_bSucceed:
            for v in result.m_objResult["fetelist"]["fete"]:
                f = Fete()
                f.handle_info(v)
                fete_list.append(f)
            free_all_fete = int(result.m_objResult["fetelist"].get("freeallfete", "0"))
        return fete_list, free_all_fete

    def do_fete(self, fete_id, fete_gold, fete_name):
        url = "/root/fete!dofete.action"
        data = {"feteId": fete_id}
        result = self.get_protocol_mgr().post_xml(url, data, "祭祀")
        if result and result.m_bSucceed:
            use_gold = False
            if fete_gold > 0:
                use_gold = True
            self.info("花费{}金币祭祀{}".format(fete_gold, fete_name), use_gold)
            gain = result.m_objResult["gains"]["gain"]
            if isinstance(gain, list):
                for v in gain:
                    self.info("{}倍暴击，获得{}+{}".format(v["pro"], v["addtype"], v["addvalue"]))
            else:
                self.info("{}倍暴击，获得{}+{}".format(gain["pro"], gain["addtype"], gain["addvalue"]))

    #######################################
    # task begin
    #######################################
    def get_new_per_day_task(self):
        url = "/root/task!getNewPerdayTask.action"
        result = self.get_protocol_mgr().get_xml(url, "日常任务")
        if result and result.m_bSucceed:
            day_box_state = result.m_objResult["dayboxstate"].split(",")
            for k, v in enumerate(day_box_state, 1):
                if v == "0":
                    self.open_day_box(k)
            if result.m_objResult["redpacketinfo"]["redpacket"] == "0":
                self.open_week_red_packet()
            self.m_objUser.set_task(result.m_objResult["task"])
            for task in result.m_objResult["task"]:
                if task["taskstate"] == "3":
                    self.get_new_per_day_task_reward(task["taskid"])

    def open_day_box(self, reward_id):
        url = "/root/task!openDayBox.action"
        data = {"rewardId": reward_id}
        result = self.get_protocol_mgr().post_xml(url, data, "开启宝箱")
        if result and result.m_bSucceed:
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["rewardinfo"])
            self.info("开启日常任务活跃宝箱，获得{}".format(reward_info))

    def open_week_red_packet(self):
        url = "/root/task!openWeekRedPacket.action"
        result = self.get_protocol_mgr().get_xml(url, "活跃红包")
        if result and result.m_bSucceed:
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["rewardinfo"])
            self.info("日常任务活跃红包开奖，获得{}".format(reward_info))

    def get_new_per_day_task_reward(self, reward_id):
        url = "/root/task!getNewPerdayTaskReward.action"
        data = {"rewardId": reward_id}
        result = self.get_protocol_mgr().post_xml(url, data, "日常任务领奖")
        if result and result.m_bSucceed:
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["rewardinfo"])
            self.info("日常任务领奖，获得{}".format(reward_info))

    #######################################
    # officer begin
    #######################################
    def officer(self):
        url = "/root/officer.action"
        result = self.get_protocol_mgr().get_xml(url, "升官")
        if result and result.m_bSucceed:
            if result.m_objResult["savesalary_cd"] == "0":
                self.save_salary()

    def save_salary(self):
        url = "/root/officer!saveSalary.action"
        result = self.get_protocol_mgr().get_xml(url, "领取俸禄")
        if result and result.m_bSucceed:
            gain = int(result.m_objResult["gain"])
            troop = result.m_objResult["troop"]
            reward_info = RewardInfo()
            reward_info.handle_info(result.m_objResult["rewardinfo"])
            self.info("领取俸禄，获得银币+{}，{}，{}".format(GlobalFunc.get_short_readable(gain), troop, reward_info))

    #######################################
    # market begin
    #######################################
    def get_player_supper_market(self):
        supper_market_dto_set = set()
        supper_market_special_dto_set = set()
        fresh_time = None
        supplement_num = 0
        url = "/root/market!getPlayerSupperMarket.action"
        result = self.get_protocol_mgr().get_xml(url, "集市")
        if result and result.m_bSucceed:
            fresh_time = int(result.m_objResult["freshtime"])
            supplement_num = int(result.m_objResult["supplementnum"])
            if "suppermarketdto" in result.m_objResult:
                supper_market_dto = result.m_objResult["suppermarketdto"]
                if isinstance(supper_market_dto, list):
                    for v in supper_market_dto:
                        dto = SupperMarketDto()
                        dto.handle_info(v)
                        supper_market_dto_set.add(dto)
                else:
                    dto = SupperMarketDto()
                    dto.handle_info(supper_market_dto)
                    supper_market_dto_set.add(dto)
            if "special" in result.m_objResult:
                special = result.m_objResult["special"]
                if isinstance(special, list):
                    for v in special:
                        dto = SupperMarketSpecialDto()
                        dto.handle_info(v)
                        supper_market_special_dto_set.add(dto)
                else:
                    dto = SupperMarketSpecialDto()
                    dto.handle_info(special)
                    supper_market_special_dto_set.add(dto)
            if "giftdto" in result.m_objResult:
                dto = SupperMarketDto()
                dto.handle_info(result.m_objResult["giftdto"])
                self.handle_supper_market_gift(dto)

        return supper_market_dto_set, supper_market_special_dto_set, fresh_time, supplement_num

    def bargain_supper_market_commodity(self, commodity_id):
        url = "/root/market!bargainSupperMarketCommodity.action"
        data = {"commodityId": commodity_id}
        result = self.get_protocol_mgr().post_xml(url, data, "商品还价")
        if result and result.m_bSucceed:
            self.info("一键还价" if commodity_id == -1 else "商品还价")

    def off_supper_market_commodity(self, supper_market_dto):
        url = "/root/market!offSupperMarketCommodity.action"
        data = {"commodityId": supper_market_dto.id}
        result = self.get_protocol_mgr().post_xml(url, data, "下架商品")
        if result and result.m_bSucceed:
            self.info("下架商品{}".format(supper_market_dto))

    def buy_supper_market_commodity(self, supper_market_dto, use_gold=False):
        url = "/root/market!buySupperMarketCommodity.action"
        data = {"commodityId": supper_market_dto.id}
        result = self.get_protocol_mgr().post_xml(url, data, "购买商品")
        if result and result.m_bSucceed:
            self.info("购买商品[{}]".format(supper_market_dto), use_gold)
            if "giftdto" in result.m_objResult:
                dto = SupperMarketDto()
                dto.handle_info(result.m_objResult["giftdto"])
                self.handle_supper_market_gift(dto)

    def buy_supper_market_special_goods(self, supper_market_special_dto, use_gold=False):
        url = "/root/market!buySupperMarketSpecialGoods.action"
        data = {"commodityId": supper_market_special_dto.id}
        result = self.get_protocol_mgr().post_xml(url, data, "购买每日特供")
        if result and result.m_bSucceed:
            self.info("购买每日特供，获得{}".format(supper_market_special_dto), use_gold)

    def supplement_supper_market(self):
        url = "/root/market!supplementSupperMarket.action"
        result = self.get_protocol_mgr().get_xml(url, "使用进货令")
        if result and result.m_bSucceed:
            self.info("使用进货令")

    def abandon_supper_market_gift(self, supper_market_dto):
        url = "/root/market!abandonSupperMarketGift.action"
        result = self.get_protocol_mgr().get_xml(url, "放弃赠送商品")
        if result and result.m_bSucceed:
            self.info("放弃赠送商品[{}]".format(supper_market_dto.name))

    def recv_supper_market_gift(self):
        url = "/root/market!recvSupperMarketGift.action"
        result = self.get_protocol_mgr().get_xml(url, "领取赠送商品")
        if result and result.m_bSucceed:
            if "num" in result.m_objResult:
                msg = "领取赠送商品[{}{}]".format(result.m_objResult["num"], result.m_objResult["name"])
            else:
                msg = "使用赠送商品[{}]".format(result.m_objResult["name"])
            self.info(msg)

    def handle_supper_market_gift(self, supper_market_dto):
        if config["market"]["gift"]["enable"]:
            if supper_market_dto.name in config["market"]["gift"]["list"]:
                self.recv_supper_market_gift()
            else:
                self.abandon_supper_market_gift(supper_market_dto)
        else:
            self.abandon_supper_market_gift(supper_market_dto)

    def get_player_merchant(self):
        url = "/root/market!getPlayerMerchant.action"
        result = self.get_protocol_mgr().get_xml(url, "委派商人")
        if result and result.m_bSucceed:
            if result.m_objResult["free"] == "1":
                self.trade(result.m_objResult["merchant"][0])

    def trade(self, merchant):
        url = "/root/market!trade.action"
        data = {"gold": 0, "merchantId": merchant["merchantid"]}
        result = self.get_protocol_mgr().post_xml(url, data, "委派")
        if result and result.m_bSucceed:
            self.confirm(result.m_objResult["tradesn"], result.m_objResult["merchandise"])

    def confirm(self, trade_sn, merchandise):
        url = "/root/market!confirm.action"
        data = {"tradeSN": trade_sn}
        result = self.get_protocol_mgr().post_xml(url, data, "卖出委派商品")
        if result and result.m_bSucceed:
            self.info("卖出委派商品[{}]，获得{}银币".format(merchandise["merchandisename"], result.m_objResult["cost"]))

    #######################################
    # tickets begin
    #######################################
    def tickets(self):
        ticket_list = list()
        url = "/root/tickets.action"
        result = self.get_protocol_mgr().get_xml(url, "点券商城")
        if result and result.m_bSucceed:
            self.m_objUser.m_nTickets = int(result.m_objResult["tickets"])
            for v in result.m_objResult["rewards"]["reward"]:
                ticket = Ticket()
                ticket.handle_info(v)
                ticket_list.append(ticket)
        return ticket_list

    def get_tickets_reward(self, ticket, num):
        url = "/root/tickets!getTicketsReward.action"
        data = {"rewardId": ticket.id, "num": num}
        result = self.get_protocol_mgr().post_xml(url, data, "兑换奖励")
        if result and result.m_bSucceed:
            use_tickets = GlobalFunc.get_short_readable(ticket.tickets * num)
            get_num = GlobalFunc.get_short_readable(ticket.item.num * num)
            self.info("兑换奖励，花费{}点券，获得{}+{}".format(use_tickets, ticket.item.name, get_num))

    def get_tickets_reward_by_name(self, name, num):
        ticket = self.m_objUser.m_dictTicketExchange.get(name, None)
        if ticket is not None:
            self.get_tickets_reward(ticket, num)

    #######################################
    # dayTreasureGame begin
    #######################################
    def get_new_treasure_game_info(self):
        url = "/root/dayTreasureGame!getNewTreasureGameInfo.action"
        result = self.get_protocol_mgr().get_xml(url, "王朝寻宝")
        if result and result.m_bSucceed:
            dice_num = int(result.m_objResult["dicenum"])
            self.info("王朝寻宝，当前骰子：{}".format(dice_num))
            return dice_num

    def start_new_t_game(self):
        url = "/root/dayTreasureGame!startNewTGame.action"
        result = self.get_protocol_mgr().get_xml(url, "开始探宝")
        if result and result.m_bSucceed:
            dict_info = dict()
            dict_info["当前骰子"] = int(result.m_objResult["dicenum"])
            dict_info["可购买骰子"] = int(result.m_objResult["golddicenum"])
            dict_info["购买骰子消耗金币"] = int(result.m_objResult["buycost"])
            dict_info["可购买次数"] = int(result.m_objResult["havebuytimes"])
            dict_info["当前位置"] = int(result.m_objResult["curpos"])
            dict_info["事件位置"] = int(result.m_objResult["eventpos"])
            dict_info["剩余步数"] = int(result.m_objResult["remainnum"])
            dict_info["当前地图"] = int(result.m_objResult["curmapid"])
            dict_info["下一地图"] = int(result.m_objResult.get("nextmapid", "0"))
            dict_info["换地图"] = result.m_objResult.get("changemap", "0") == "1"
            dict_info["探宝完毕"] = result.m_objResult.get("needfinish", "0") == "1"
            if "eventtype" in result.m_objResult:
                self.handle_treasure_event(dict_info, result.m_objResult)
            self.info("当前骰子：{}".format(dict_info["当前骰子"]))
            return dict_info

    def use_new_t_dice(self):
        url = "/root/dayTreasureGame!useNewTDice.action"
        result = self.get_protocol_mgr().get_xml(url, "掷骰子")
        if result and result.m_bSucceed:
            msg = "掷到{}点".format(result.m_objResult["movenum"])
            if "pointreward" in result.m_objResult:
                msg += "，获得 {}".format(self.handle_point_reward(result.m_objResult["pointreward"]))
            self.info(msg)

    def handler_event(self, op, msg):
        url = "/root/dayTreasureGame!handlerEvent.action"
        data = {"open": op}
        result = self.get_protocol_mgr().post_xml(url, data, "执行探宝事件")
        if result and result.m_bSucceed:
            if "rewardinfo" in result.m_objResult:
                reward_info = RewardInfo()
                reward_info.handle_info(result.m_objResult["rewardinfo"])
                msg += "，获得{}".format(reward_info)
            self.info(msg)

    def transfer(self):
        url = "/root/dayTreasureGame!transfer.action"
        result = self.get_protocol_mgr().get_xml(url, "换地图")
        if result and result.m_bSucceed:
            msg = "更换寻宝地图"
            if "pointreward" in result.m_objResult:
                msg += "，获得 {}".format(self.handle_point_reward(result.m_objResult["pointreward"]))
            self.info(msg)

    @staticmethod
    def handle_treasure_event(dict_info, result):
        event_type = result["eventtype"]
        dict_info["事件"] = event_type
        if event_type == "1":
            dict_info["探索路径步数"] = int(result["footnum"])
            dict_info["事件名称"] = "[探索路径]事件，行走了{}步".format(dict_info["探索路径步数"])
        elif event_type == "2":
            dict_info["免费摇摇钱树"] = int(result["freeshake"])
            dict_info["下一次宝石奖励"] = RewardInfo()
            dict_info["下一次宝石奖励"].handle_info(result["nextbaoshi"]["rewardinfo"])
            dict_info["事件名称"] = "[摇钱树]事件，下一次宝石奖励[{}]".format(dict_info["下一次宝石奖励"])
        elif event_type == "3":
            dict_info["购买宝箱消耗金币"] = int(result["goldboxcost"])
            dict_info["购买宝箱"] = result["rewardname"]
            dict_info["事件名称"] = "[购买宝箱]事件，宝箱[{}({}金币)]".format(dict_info["购买宝箱"], dict_info["购买宝箱消耗金币"])

    def handle_point_reward(self, result):
        msg = ""
        if isinstance(result, list):
            for point_reward in result:
                if "rewardinfo" in point_reward:
                    reward_info = RewardInfo()
                    reward_info.handle_info(point_reward["rewardinfo"])
                    msg += "{} ".format(reward_info)
                if "eventtype" in point_reward:
                    dict_info = dict()
                    self.handle_treasure_event(dict_info, point_reward)
                    msg += "发现{}".format(dict_info["事件名称"])
        else:
            point_reward = result
            if "rewardinfo" in point_reward:
                reward_info = RewardInfo()
                reward_info.handle_info(point_reward["rewardinfo"])
                msg += "{} ".format(reward_info)
            if "eventtype" in point_reward:
                dict_info = dict()
                self.handle_treasure_event(dict_info, point_reward)
                msg += "发现{}".format(dict_info["事件名称"])
        return msg

    def away_new_t_game(self):
        url = "/root/dayTreasureGame!awayNewTGame.action"
        result = self.get_protocol_mgr().get_xml(url, "探宝完毕")
        if result and result.m_bSucceed:
            self.info("探宝完毕")

    #######################################
    # secretary begin
    #######################################
    def secretary(self):
        url = "/root/secretary.action"
        result = self.get_protocol_mgr().get_xml(url, "秘书")
        if result and result.m_bSucceed:
            max_token_num = int(result.m_objResult.get("maxtokennum", "0"))
            token_num = int(result.m_objResult.get("tokennum", "0"))
            cd = int(result.m_objResult.get("cd", "0"))
            if max_token_num - token_num > 0 and cd == 0:
                self.apply_token()

    def apply_token(self):
        url = "/root/secretary!applyToken.action"
        result = self.get_protocol_mgr().get_xml(url, "领取每日军令")
        if result and result.m_bSucceed:
            max_token_num = int(result.m_objResult.get("maxtokennum", "0"))
            token_num = int(result.m_objResult.get("tokennum", "0"))
            cd = int(result.m_objResult.get("cd", "0"))
            self.info("领取每日军令，还有{}个，领取CD：{}".format(max_token_num - token_num, TimeMgr.get_datetime_string(cd)))

    #######################################
    # secretary begin
    #######################################
    def get_all_dinner(self):
        url = "/root/dinner!getAllDinner.action"
        result = self.get_protocol_mgr().get_xml(url, "宴会")
        if result and result.m_bSucceed:
            info = dict()
            info["宴会期间"] = result.m_objResult.get("indinnertime", "0") == "1"
            info["已加入队伍"] = result.m_objResult["teamstate"] == "1"
            if "normaldinner" in result.m_objResult:
                info["剩余宴会次数"] = int(result.m_objResult["normaldinner"]["num"])
            else:
                info["剩余宴会次数"] = 0
            if "team" in result.m_objResult:
                team = result.m_objResult["team"]
                if isinstance(team, list):
                    for t in team:
                        if int(t["num"]) < int(t["maxnum"]):
                            info["宴会队伍"] = t
                            break
                elif int(team["num"]) < int(team["maxnum"]):
                    info["宴会队伍"] = team
            return info

    def join_dinner(self, team):
        url = "/root/dinner!joinDinner.action"
        data = {"teamId": team["teamid"]}
        result = self.get_protocol_mgr().post_xml(url, data, "加入宴会队伍")
        if result and result.m_bSucceed:
            self.info("加入[{}]宴会队伍".format(team["creator"]))
        else:
            self.warning(result.m_szError)

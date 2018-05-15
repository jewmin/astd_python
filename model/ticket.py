# -*- coding: utf-8 -*-
# 点券商城可兑换商品
from model.base_object import BaseObject


class Ticket(BaseObject):
    def __init__(self):
        super(Ticket, self).__init__()
        self.id = 0
        self.tickets = 0
        self.selltype = -1
        self.item = TicketItem()


class TicketItem(BaseObject):
    def __init__(self):
        super(TicketItem, self).__init__()
        self.name = ""
        self.num = 0

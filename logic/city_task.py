# -*- coding: utf-8 -*-
# 建造任务
from logic.base_task import BaseTask
from logic.config import config


class CityTask(BaseTask):
    def __init__(self):
        super(CityTask, self).__init__()
        self.m_szName = "city"
        self.m_szReadable = "建造"

    def run(self):
        city_mgr = self.m_objServiceFactory.get_city_mgr()
        city_mgr.get_main_city()

        low_city_dto_list = list()
        high_city_dto_list = list()
        for main_city_dto in self.m_objUser.m_dictMainCityBuildings.values():
            if main_city_dto.buildlevel == self.m_objUser.m_nLevel:
                continue
            elif main_city_dto.buildname in config["mainCity"]["build_list"]:
                if main_city_dto.cdtime < 240:
                    low_city_dto_list.append(main_city_dto)
                else:
                    high_city_dto_list.append(main_city_dto)

        if len(low_city_dto_list) == 0 and len(high_city_dto_list) == 0:
            return self.next_half_hour()

        low_city_dto_list = sorted(low_city_dto_list, key=lambda dto: config["mainCity"]["build_list"].index(dto.buildname))
        high_city_dto_list = sorted(high_city_dto_list, key=lambda dto: config["mainCity"]["build_list"].index(dto.buildname))
        cd_time = -1
        constructor = None
        for constructor_dto in self.m_objUser.m_listConstructorDto:
            if not (constructor_dto.cdflag == 1 and constructor_dto.ctime > 0):
                constructor = constructor_dto
                break
            else:
                if cd_time < 0 or cd_time > constructor_dto.ctime:
                    cd_time = constructor_dto.ctime

        if constructor is not None:
            if constructor.ctime > 0:
                if len(high_city_dto_list) > 0:
                    city_mgr.upgrade_level(high_city_dto_list[0])
                else:
                    city_mgr.upgrade_level(low_city_dto_list[0])
                return self.immediate()
            else:
                if len(low_city_dto_list) > 0:
                    city_mgr.upgrade_level(low_city_dto_list[0])
                else:
                    city_mgr.upgrade_level(high_city_dto_list[0])
                return self.immediate()
        else:
            return cd_time

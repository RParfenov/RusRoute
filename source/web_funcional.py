from source.handler_files import HandlerFiles
from source.handler_info_city import HandlerInfo

class WebFunc:
    def __init__(self):
        self.roads_handler_free = HandlerFiles('free-trails_city.json')
        self.roads_handler_toll = HandlerFiles('toll_trails_city.json')
        self.train_handler = HandlerFiles('train_ways.json')
        self.plane_handler = HandlerFiles('plane_ways.json')
        self.detail_info = HandlerInfo('detailed_info_about_cities.json', flag_detail=True)
        self.simple_info = HandlerInfo('info_city.json')

    def currect_time(self, to, fr, date_start, transport):
        cur_time = 0
        if transport == "train":
            base_time = self.train_handler.get_info_route(to, fr)['time']
            cur_time = base_time
        elif transport == "plane":
            base_time = self.plane_handler.get_info_route(to, fr)['time']
            cur_time = base_time
        elif transport == "toll_trails":
            base_time = float(self.roads_handler_toll.get_info_route(to, fr)['time'])
            cur_time = base_time
        elif transport == "free_trails":
            base_time = float(self.roads_handler_free.get_info_route(to, fr)['time'])
            cur_time = base_time
        else:
            raise KeyError("Неизвестный вид транспорта.")
        return cur_time

    def sorted_mass_time(self, to, fr, date_start):
        time = []
        train_time = self.currect_time(to=to, fr=fr, date_start=date_start, transport="train")
        plane_time = self.currect_time(to=to, fr=fr, date_start=date_start, transport="plane")
        toll_trails_time = self.currect_time(to=to, fr=fr, date_start=date_start, transport="toll_trails")
        free_trails_time = self.currect_time(to=to, fr=fr, date_start=date_start, transport="free_trails")
        time.append(train_time)
        time.append(plane_time)
        time.append(toll_trails_time)
        time.append(free_trails_time)
        time.sort()
        return time

    def sorted_mass_cost(self, to, fr):
        cost = []
        train_cost = self.train_handler.get_info_route(to, fr)['cost']
        plane_cost = self.plane_handler.get_info_route(to, fr)['cost']
        toll_trails_cost = self.roads_handler_toll.get_info_route(to, fr)['fuel_cost'] + \
                           self.roads_handler_toll.get_info_route(to, fr)['trails_cost']
        free_trails_cost = self.roads_handler_free.get_info_route(to, fr)['fuel_cost']
        cost.append(train_cost)
        cost.append(plane_cost)
        cost.append(toll_trails_cost)
        cost.append(free_trails_cost)
        cost.sort()
        return cost


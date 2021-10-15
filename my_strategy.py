from model import *
from math import cos, sqrt


class MyStrategy:
    def __init__(self):
        pass

    '''
    Примитивная стратегия, которая пытается застроить всю карту каменоломнями и получать очки за добычу камня.
    Смотри подсказки по ее улучшению, оформленные в виде специальных комментариев: # TODO ...
    '''

    def get_action(self, game: Game) -> Action:
        gh = 0
        moves = []
        builds = []
        cv = 999999999999999999
        c = 0
        c1 = 0
        bild = 0
        c2 = 0
        fly = []
        bld = [BuildingType.FOUNDRY, BuildingType.FARM, BuildingType.CAREER, BuildingType.MINES, BuildingType.QUARRY,BuildingType.FURNACE]
        for f, i in enumerate(game.planets):
            if len(i.worker_groups) != 0 and i.building != None:
                if i.worker_groups[0].player_index == 0 and f != 0:
                    if i.building.building_type == BuildingType.QUARRY:
                        bld.remove(BuildingType.QUARRY)
                    if i.building.building_type == BuildingType.MINES:
                        bld.remove(BuildingType.MINES)
                    if i.building.building_type == BuildingType.CAREER:
                        bld.remove(BuildingType.CAREER)
                    if i.building.building_type == BuildingType.FARM:
                        bld.remove(BuildingType.FARM)
                    if i.building.building_type == BuildingType.FOUNDRY:
                        bld.remove(BuildingType.FOUNDRY)
                    if i.building.building_type == BuildingType.FURNACE:
                        bld.remove(BuildingType.FURNACE)
        for f, i in enumerate(game.planets):

            for g in i.worker_groups:
                if g.number is not None and g.player_index == 0:
                    if g.number > c1:
                        c2 = i
                        c1 = g.number
                        c = f
        s = 0
        o = 0
        sa = 0
        org = 0
        bild1 =0
        for f, i in enumerate(game.planets):
            if i.building is not None and len(i.worker_groups) != 0:
                if i.building.building_type == BuildingType.FOUNDRY and len(bld)!= 0:
                    if i.worker_groups[0].player_index == 0:
                        bild = 1
        for f, i in enumerate(game.planets):
            if i.building is not None and len(i.worker_groups) != 0:
                if i.building.building_type == BuildingType.FURNACE and len(bld)!= 0:
                    if i.worker_groups[0].player_index == 0:
                        bild1 = 1
        for i in game.planets:

            if len(i.worker_groups) != 0:
                if i.worker_groups[0].player_index == 0:
                    if i.harvestable_resource == Resource.STONE and i.worker_groups[0].number > 99:
                        s += 1
                    if i.harvestable_resource == Resource.ORE and i.worker_groups[0].number > 99:
                        o += 1
                    if i.harvestable_resource == Resource.SAND and i.worker_groups[0].number > 99:
                        sa += 1
                    if i.harvestable_resource == Resource.ORGANICS and i.worker_groups[0].number > 99:
                        org += 1

        res = [Resource.STONE, Resource.SAND, Resource.ORE, Resource.ORGANICS]
        if s >= 2:
            res.remove(Resource.STONE)
        if o >= 1:
            res.remove(Resource.ORE)
        if sa >= 1:
            res.remove(Resource.SAND)
        if org >= 1:
            res.remove(Resource.ORGANICS)

        if len(res) == 0:
            if len(bld) ==2:

                gh = 1
        gh1 = 0
        if len(res) == 0:
            if len(bld) ==1:

                gh1 = 1

        #print(bld)
        lat1 = c2.x
        lng1 = c2.y
        ch = 0
        MN = None
        for f, i in enumerate(game.planets):
            if f != 0:
                if i.harvestable_resource in res:
                    if len(i.worker_groups) == 0:
                        if len(game.flying_worker_groups) == 0:
                            lat2 = i.x
                            lng2 = i.y
                            x = lat2 - lat1
                            y = (lng2 - lng1) * cos((lat2 + lat1) * 0.00872664626)
                            bg = int(111.138 * sqrt(x * x + y * y) * 1000)
                            if cv > bg:
                                MN = i.harvestable_resource
                                cv = bg
                                ch = f
                        else:
                            for g in game.flying_worker_groups:
                                if g.player_index == 0:
                                    fly.append(g.player_index)
                            if len(fly) < 1:
                                lat2 = i.x
                                lng2 = i.y
                                x = lat2 - lat1
                                y = (lng2 - lng1) * cos((lat2 + lat1) * 0.00872664626)
                                bg = int(111.138 * sqrt(x * x + y * y) * 1000)
                                if cv > bg:
                                    MN = i.harvestable_resource
                                    cv = bg
                                    ch = f
                    else:
                        if game.planets[f].worker_groups[0].number < 101 and i.worker_groups[0].player_index == 0:
                            if len(game.flying_worker_groups) == 0:
                                lat2 = i.x
                                lng2 = i.y
                                x = lat2 - lat1
                                y = (lng2 - lng1) * cos((lat2 + lat1) * 0.00872664626)
                                bg = int(111.138 * sqrt(x * x + y * y) * 1000)
                                if cv > bg:
                                    cv = bg
                                    ch = f
                            else:
                                for g in game.flying_worker_groups:
                                    if g.player_index == 0:
                                        fly.append(g.player_index)

                                if len(fly) < 1:
                                    lat2 = i.x
                                    lng2 = i.y
                                    x = lat2 - lat1
                                    y = (lng2 - lng1) * cos((lat2 + lat1) * 0.00872664626)
                                    bg = int(111.138 * sqrt(x * x + y * y) * 1000)
                                    if cv > bg:
                                        MN = i.harvestable_resource
                                        cv = bg
                                        ch = f

        # прочитать свойства здания "каменоломня"
        quarry_properties = game.building_properties[BuildingType.FURNACE]
        print(quarry_properties)
        if c2.worker_groups[0].number > 1:
            moves.append(MoveAction(0, ch, 50, Resource.STONE))

        for f, i in enumerate(game.planets):
            if len(i.worker_groups) != 0:
                if i.worker_groups[0].player_index == 0:
                    if i.worker_groups[0].number == 100:
                        if i.harvestable_resource == Resource.STONE and BuildingType.QUARRY in bld:
                            builds.append(BuildingAction(f, BuildingType.QUARRY))
                        if i.harvestable_resource == Resource.ORE and BuildingType.MINES in bld:
                            builds.append(BuildingAction(f, BuildingType.MINES))
                        if i.harvestable_resource == Resource.SAND and BuildingType.CAREER in bld:
                            builds.append(BuildingAction(f, BuildingType.CAREER))
                        if i.harvestable_resource == Resource.ORGANICS and BuildingType.FARM in bld:
                            builds.append(BuildingAction(f, BuildingType.FARM))
                        if bild==0 and len(bld) == 2:

                            builds.append(BuildingAction(f, BuildingType.FOUNDRY))
                        if bild1==0 and len(bld) == 1:

                            builds.append(BuildingAction(f, BuildingType.FURNACE))


        if len(res) == 0:
            for f, i in enumerate(game.planets):
                if len(i.worker_groups) != 0:
                    if i.worker_groups[0].player_index == 0:
                        if game.planets[0].worker_groups[0].number < 500 and len(bld) !=0 :
                            if i.worker_groups[0].number > 100:

                                moves.append(MoveAction(f, 0, 50, None))
                            if 0 < i.worker_groups[0].number < 100 and len(bld) != 1 :

                                moves.append(MoveAction(0, f, 50, Resource.STONE))

        if len(res) == 0 and gh == 1 and len(bld)==2 and bild == 0 :

            for f, i in enumerate(game.planets):
                if f!= 0:
                    if len(i.worker_groups) == 0:
                        if len(game.flying_worker_groups) == 0:
                            lat2 = i.x
                            lng2 = i.y
                            x = lat2 - lat1
                            y = (lng2 - lng1) * cos((lat2 + lat1) * 0.00872664626)
                            bg = int(111.138 * sqrt(x * x + y * y) * 1000)
                            if cv > bg:
                                MN = i.harvestable_resource
                                cv = bg
                                ch = f
                        else:
                            for g in game.flying_worker_groups:
                                if g.player_index == 0:
                                    fly.append(g.player_index)
                            if len(fly) < 1:
                                lat2 = i.x
                                lng2 = i.y
                                x = lat2 - lat1
                                y = (lng2 - lng1) * cos((lat2 + lat1) * 0.00872664626)
                                bg = int(111.138 * sqrt(x * x + y * y) * 1000)
                                if cv > bg:
                                    MN = i.harvestable_resource
                                    cv = bg
                                    ch = f
                    else:
                        if i.worker_groups[0].number == 50:
                            if len(game.flying_worker_groups) == 0:
                                lat2 = i.x
                                lng2 = i.y
                                x = lat2 - lat1
                                y = (lng2 - lng1) * cos((lat2 + lat1) * 0.00872664626)
                                bg = int(111.138 * sqrt(x * x + y * y) * 1000)
                                if cv > bg:
                                    MN = i.harvestable_resource
                                    cv = bg
                                    ch = f
                            else:
                                for g in game.flying_worker_groups:
                                    if g.player_index == 0:
                                        fly.append(g.player_index)
                                if len(fly) < 1:
                                    lat2 = i.x
                                    lng2 = i.y
                                    x = lat2 - lat1
                                    y = (lng2 - lng1) * cos((lat2 + lat1) * 0.00872664626)
                                    bg = int(111.138 * sqrt(x * x + y * y) * 1000)
                                    if cv > bg:
                                        MN = i.harvestable_resource
                                        cv = bg
                                        ch = f
            if ch != 0:

                moves.append(MoveAction(0, ch, 50, Resource.STONE))
        ore = 0
        met = 0
        if len(bld)==1:
            for f,i in enumerate(game.planets):
                if i.building != None and game.planets[0].worker_groups[0].number >=500:
                    if i.building.building_type == BuildingType.MINES and i.worker_groups[0].number <=100:
                        if i.worker_groups[0].player_index == 0:

                            ore = f


                    if i.building.building_type == BuildingType.FOUNDRY:
                        if i.worker_groups[0].player_index == 0 and i.worker_groups[0].number <=100:
                            met = f




                else:
                    if len(i.worker_groups) != 0 and i.building == None and i.worker_groups[0].number == 50:
                        for g in game.flying_worker_groups:
                            if g.player_index == 0:
                                fly.append(g.player_index)
                        if len(fly) < 1:
                            moves.append(MoveAction(f, 0, 50, None))
                            break
            if met != 0 and ore != 0:
                moves = []
                moves.append(MoveAction(ore, met, 5, Resource.ORE))
                moves.append(MoveAction(met, ore, 5, None))


        # сформировать ответ серверу
        return Action(moves, builds)

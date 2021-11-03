from constants import world_size

def create_map(world_map):

    # world borders:

    # left border

    world_map[0:world_size+1, 0:2] = 20
    # right border
    world_map[0:world_size+1, world_size-1:world_size+1] = 20
    # top border
    world_map[0:2, 0:world_size+1] = 20
    # bottom border
    world_map[world_size-1:world_size+1, 0:world_size+1] = 20

    # small classroom:

    # left wall
    world_map[47:254, 47:51] = 20
    # right wall
    world_map[47:354, 250:254] = 20
    # top wall
    world_map[47:51, 47:254] = 20
    # bottom wall
    world_map[250:254, 47:254] = 20

    #corridor
    world_map[350:354, 253:375] = 20
    world_map[280:394, 372:375] = 20

    #classroom 2
    world_map[390:394,372:525] = 20 #down
    world_map[240:394,521:525] = 20 #right
    world_map[240:244,372:525] = 20 #top
    world_map[220:254,372:376] = 20 # left

    #classroom 3
    world_map[220:224,333:490] = 20 #bottom
    world_map[100:224,486:490] = 20 #right
    world_map[100:104,330:490] = 20 #top
    world_map[100:224,330:334] = 20 # left
    world_map[220:251,341:345] = 20 #extra
    #door
    world_map[220:224,348:368] = 0


    #main entrance
    world_map[350:354, 280:310] = 0

    world_map[250:324, 341:345] = 20
    world_map[320:324, 285:345] = 20

    world_map[190:324, 285:289] = 20
    world_map[190:194,250:285] = 20

    # desks

    '''# teacher desk dimensions x = 30 y = 10
    world_map[75:85, 135:165] = 20
    # middle row
    # short desk dimensions x = 30 y = 10
    world_map[105:115, 135:165] = 20
    # long desk dimensions x = 40 y = 10
    world_map[130:140, 130:170] = 20
    world_map[155:165, 130:170] = 20
    world_map[190:200, 130:170] = 20
    world_map[215:225, 130:170] = 20

    # left side
    # short desk dimensions x = 30 y = 10
    world_map[105:115, 75:105] = 20
    # long desk dimensions x = 40 y = 10
    world_map[130:140, 70:110] = 20
    world_map[155:165, 70:110] = 20
    world_map[190:200, 70:110] = 20
    world_map[215:225, 70:110] = 20


    # right side
    # short desk dimensions x = 30 y = 10
    world_map[105:115, 195:225] = 20
    # long desk dimensions x = 40 y = 10
    world_map[130:140, 190:230] = 20
    world_map[155:165, 190:230] = 20
    world_map[190:200, 190:230] = 20
    world_map[215:225, 190:230] = 20
'''
    # door
    world_map[200:225, 250:254] = 0

    return world_map
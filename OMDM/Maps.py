"""

"""
import numpy as np
import cv2
from OMDM.Campus import Campus
img = cv2.imread('color_test.png', cv2.IMREAD_UNCHANGED)


height = img.shape[0]
width = img.shape[1]
x_coordinates = []
y_coordinates = []

#   print(height)
#   print(width)
#   print (img[0][0][0])
#   world_map = np.zeros((height, width), np.int32)
#   infected_surfaces_map = np.full((height, width), -1)


#   def create_map_from_img(world_map):

def create_map_from_img(world_map,infected_surfaces_map):
    classroom_entrance_list = []
    classroom_seats_list = []

    for y in range(width):
        for x in range(height):

                # Check for walls
                if img[y][x][0] == 0 and img[y][x][1] == 0 and img[y][x][2] == 0:
                    world_map[y][x] = 20

                # Check for spawning point
                if img[y][x][0] == 0 and img[y][x][1] == 0 and img[y][x][2] == 255:
                    start_location_x = x
                    start_location_y = y


                # Check for desks
                if img[y][x][0] == 255 and img[y][x][1] == 0 and img[y][x][2] == 255:
                    world_map[y][x] = 20
                    infected_surfaces_map[x][y] = 0

                # Check for doors
                if img[y][x][0] == 255 and img[y][x][1] == 0 and img[y][x][2] == 255:
                    infected_surfaces_map[x][y] = 0

                # Check for classroom entrance/exit
                if img[y][x][0] >= 200 and img[y][x][1] == 0 and img[y][x][2] == 0:
                    for i in range(200,256,5):
                        if img[y][x][0] == i:
                            #classroom_entrance_list.append(((len(classroom_entrance_list)+1),(x,y)))
                            classroom_entrance_list.append((i,(x,y)))


                # check seats
                if img[y][x][0] == 0 and img[y][x][1] >= 200 and img[y][x][2] == 0:
                    for i in range(200,256,5):
                        if img[y][x][1] == i:
                            if i not in classroom_seats_list:
                                classroom_seats_list.append((i,(x,y)))




    # sort classroom list of according to the lowest blue channel value
    classroom_entrance_list.sort(key=lambda c:c[0])
    print(classroom_entrance_list)




    # left border
    world_map[0:height + 1, 0:2] = 20
    # right border
    world_map[0:height + 1, width - 1:width + 1] = 20
    # top border
    world_map[0:2, 0:width + 1] = 20
    # bottom border
    world_map[height - 1:height + 1, 0:width + 1] = 20

    return world_map,infected_surfaces_map,classroom_entrance_list,start_location_x,start_location_y



def create_map(world_map, world_size):

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
    '''
    # teacher desk dimensions x = 30 y = 10
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
    world_map[215:225, 190:230] = 20'''

    # door
    world_map[200:225, 250:254] = 0

    return world_map
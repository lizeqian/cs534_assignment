#!/usr/bin/env python

import numpy as np

class vacuum_world:
    def __init__(self):
        self.world_h    =   8
        self.world_w    =   8
        self.vacuum_x   =   0
        self.vacuum_y   =   0
        self.dirt       =   np.zeros((self.world_h, self.world_w))
        self.score      =   0

    def sensor(self):
        self.current_dirt   =   self.dirt[self.vacuum_y, self.vacuum_y]
        return self.current_dirt, self.vacuum_x, self.vacuum_y


    def environment_init(self, height, width, dirtiness, vacuum_init_x, vacuum_init_y):
        self.world_h    =   height
        self.world_w    =   width
        self.dirt       =   dirtiness
        self.vacuum_x   =   vacuum_init_x
        self.vacuum_y   =   vacuum_init_y
    
    def actuator(self, action): #action = "left", "right", "up", "down", "suck"


        if action=="left":
            self.vacuum_x-=1
        elif action=="right":
            self.vacuum_x+=1

        if action=="up":
            self.vacuum_y-=1
        elif action=="down":
            self.vacuum_y+=1

        if action=="suck":
            self.dirt[self.vacuum_y, self.vacuum_x]=0
            print ("suck")
       
    def performance_evaluation(self):       #needs to be called very step
        self.score  += self.world_h*self.world_w-np.sum(self.dirt)
        return self.score
        
if __name__ == '__main__':
    world_height = 1
    world_width  = 2
    dirtiness    = np.ones((1,2))
    vacuum_x     = 0
    vacuum_y     = 0
    lifetime     = 1000


    vacuum_env = vacuum_world()

    vacuum_env.environment_init(world_height, world_width, dirtiness, vacuum_x, vacuum_y)

    lifetime_cnt = 0

    while lifetime_cnt < lifetime:
        cur_dirt, cur_x, cur_y = vacuum_env.sensor()
        if cur_dirt == 1:
            cur_action = "suck"
        elif cur_x == 0:
            cur_action = "right"
        else:
            cur_action = "left"
        
        print (cur_action)
        vacuum_env.actuator(cur_action)
        (vacuum_env.performance_evaluation())

        lifetime_cnt += 1

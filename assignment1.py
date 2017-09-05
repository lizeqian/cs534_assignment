#!/usr/bin/env python

import numpy as np



class vacuum_world:
    def __init__(self):
        self.world_h    =   8
        self.world_w    =   8
        self.vacuum_x   =   0
        self.vacuum_y   =   0
        self.dirt       =   np.zeros((self.world_h, self.world_w))
        self.step_num   =   0

    def sensor(self):
        self.current_dirt   =   self.dirt[self.vacuum_y, self.vacuum_y]
        self.hit_top        =   (self.vacuum_y==0)
        self.hit_bottom     =   (self.vacuum_y==(self.world_h-1))
        self.hit_left       =   (self.vacuum_x==0)
        self.hit_right      =   (self.vacuum_x==(self.world_w-1))
        return self.current_dirt, self.hit_top, self.hit_bottom, self.hit_left, self.hit_right


    def environment_init(self, height, width, dirtiness, vacuum_init_x, vacuum_init_y):
        self.world_h    =   height
        self.world_w    =   width
        self.dirt       =   dirtiness
        self.vacuum_x   =   vacuum_init_x
        self.vacuum_y   =   vacuum_init_y
    
    def actuator(self, action): #action = "left", "right", "up", "down", "suck"

        self.step_num+=1

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
       
    def performance_evaluation(self):
        self.score  =   100 - self.step_num - (10*np.sum(self.dirt))
        return self.score
        
if __name__ == '__main__':
    vacuum_env = vacuum_world()

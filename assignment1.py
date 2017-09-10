#!/usr/bin/env python

import numpy as np
import random

class vacuum_world:
    def __init__(self):
        self.world_h    =   8
        self.world_w    =   8
        self.vacuum_x   =   0
        self.vacuum_y   =   0
        self.dirt       =   np.zeros((self.world_h, self.world_w)) #the location of dirt, defined by a 2darray(world_h, world_w), 0 means clean, 1 means dirty
        self.score      =   0
        self.world_shape=   np.ones((self.world_h, self.world_w))  #world_shape is defined by a 2darray(world_h, world_w), 0 means unaccessible like a wall, 1 means accessible places 

    def sensor(self):
        self.current_dirt   =   self.dirt[self.vacuum_y, self.vacuum_x]
        return self.current_dirt, self.vacuum_x, self.vacuum_y


    def environment_init(self, height, width, world_shape, dirtiness, vacuum_init_x, vacuum_init_y): #dirtiness sould be a 2darray
        self.world_h    =   height
        self.world_w    =   width
        self.dirt       =   dirtiness
        self.vacuum_x   =   vacuum_init_x
        self.vacuum_y   =   vacuum_init_y
        self.world_shape=   world_shape
    
    def actuator(self, action): #action = "left", "right", "up", "down", "suck"
        self.performance_evaluation()       #evaluated before vacuum's action
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
        
        #self.performance_evaluation()      #evaluated after vacuum's action

       
    def performance_evaluation(self):       #needs to be called every step
        self.score  += self.world_h*self.world_w-np.sum(self.dirt)

    def print_score(self):
        print ("score = %d\n"%(self.score))
       
class vacuum:
    def __init__(self):
        self.world_h        = 8
        self.world_w        = 8
        self.world_shape    = np.ones((self.world_h, self.world_w))
        self.vacuum_x       = 0
        self.vacuum_y       = 0

    def vacuum_init(self, world_h, world_w, world_shape):
        self.world_h = world_h
        self.world_w = world_w
        self.world_shape = world_shape

    def sensor(self, info):
        self.dirt, self.vacuum_x, self.vacuum_y = info
        
    def actuator(self):     #move randomly 
        possible_moves = {"up", "down", "right", "left"}

        if self.dirt:
            vac_action = "suck"
        else:
            if self.vacuum_x == 0:
                possible_moves.discard("left")
            elif self.world_shape[self.vacuum_y, self.vacuum_x-1] == 0:
                possible_moves.discard("left")

            if self.vacuum_x == self.world_w-1: 
                possible_moves.discard("right")
            elif self.world_shape[self.vacuum_y, self.vacuum_x+1]==0:
                possible_moves.discard("right")

            if self.vacuum_y == 0:
                possible_moves.discard("up")
            elif self.world_shape[self.vacuum_y-1, self.vacuum_x] == 0:
                possible_moves.discard("up")

            if self.vacuum_y == self.world_h -1:
                possible_moves.discard("down")
            elif self.world_shape[self.vacuum_y+1, self.vacuum_x] == 0:
                possible_moves.discard("down")

            vac_action = random.sample(possible_moves, 1)[0]
        

        return vac_action





if __name__ == '__main__':
    world_height = 1
    world_width  = 2
    vacuum_x_set     = {0, 1}
    vacuum_y_set     = {0}
    lifetime     = 1000
    world_shape  = np.ones((world_height, world_width))


    for vacuum_x in vacuum_x_set:
        for vacuum_y in vacuum_y_set:
            dirtiness_set    = [np.array([[0,0]]), np.array([[0,1]]), np.array([[1,0]]), np.array([[1,1]])]
            for dirtiness in dirtiness_set:
                world_env = vacuum_world()
                vacuum_env = vacuum()
                world_env.environment_init(world_height, world_width, world_shape, dirtiness, vacuum_x, vacuum_y)
                vacuum_env.vacuum_init(world_height, world_width, world_shape)

                lifetime_cnt = 0
                filename = "vacuum_position_("+str(vacuum_x)+","+str(vacuum_y)+")_dirt_location_"+str(dirtiness[0,0])+"_"+str(dirtiness[0,1])+".txt"
                print(filename)
                f = open(filename,"w")

                while lifetime_cnt < lifetime:
                    vacuum_env.sensor(world_env.sensor())
                    action = vacuum_env.actuator()
                    world_env.actuator(action)
                    f.write("%s\n"%(action))

                    lifetime_cnt += 1
                f.close()
                world_env.print_score()


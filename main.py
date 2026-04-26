#import pygame
import pygame

pygame.init()

import button
import graphs
import draw_basic
import random

import settings
import algorithms

#class jeu
class Game():

    #fonction qui s'exucute quand game1 est cree
    def __init__(self, screen, screen_width, screen_height):

        #set les varioble
        #screen
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.game_screen = "default"

        self.move_the_nodes = True
        self.clicked_node: graphs.Node = None #type: ignore

        #running variable
        self.running = True

        self.left_mouse_down = False
        self.right_mouse_down = False

        self.buttons = []

        self.setup_graph()

        self.start_end_nodes = [] #type: ignore
    
    def setup_graph(self):
        graphs.load_graph_from_json('graph.json')  

    def left_mouse_click(self, pos):
        if len(graphs.get_all_nodes()) == 0:
            graphs.create_node(str(len(graphs.get_all_nodes())), pos[0], pos[1])
            return

        distances = [(node, (node.x - pos[0]) ** 2 + (node.y - pos[1]) ** 2) for node in graphs.get_all_nodes()]
        closest_node = min(distances, key=lambda x: x[1])

        if closest_node[1] <= settings.NODE_SIZE ** 2:
            self.clicked_node = closest_node[0]
            self.left_mouse_down = True
        
        else:
            graphs.create_node(str(graphs.get_next_available_name()), pos[0], pos[1])
    
    def left_mouse_release(self, pos):
        if self.left_mouse_down:
            self.left_mouse_down = False
            self.clicked_node.set_position(pos[0], pos[1])
            self.clicked_node = None #type: ignore
    
    def right_mouse_click(self, pos):
        distances = [(node, (node.x - pos[0]) ** 2 + (node.y - pos[1]) ** 2) for node in graphs.get_all_nodes()]
        closest_node = min(distances, key=lambda x: x[1])

        if closest_node[1] <= settings.NODE_SIZE ** 2:
            self.clicked_node = closest_node[0]
            self.right_mouse_down = True
    
    def right_mouse_release(self, pos):
        if self.right_mouse_down:
            self.right_mouse_down = False
            distances = [(node, (node.x - pos[0]) ** 2 + (node.y - pos[1]) ** 2) for node in graphs.get_all_nodes()]
            closest_node = min(distances, key=lambda x: x[1])

            if closest_node[1] <= settings.NODE_SIZE ** 2:
                if closest_node[0] == self.clicked_node:
                    graphs.delete_node(self.clicked_node)
                    if self.clicked_node in self.start_end_nodes:
                        self.start_end_nodes.remove(self.clicked_node)
                else:
                    if graphs.get_edge(self.clicked_node, closest_node[0]) is None:
                        graphs.create_edge(self.clicked_node, closest_node[0], True, 5)
                    else:
                        if (graphs.get_edge(self.clicked_node, closest_node[0]).directed and graphs.get_edge(self.clicked_node, closest_node[0]).node1 == self.clicked_node): #type: ignore
                            graphs.delete_edge(self.clicked_node, closest_node[0]) #type: ignore
                        elif (graphs.get_edge(self.clicked_node, closest_node[0]).directed and graphs.get_edge(self.clicked_node, closest_node[0]).node1 == closest_node[0]): #type: ignore
                            edge_value = graphs.get_edge(self.clicked_node, closest_node[0]).value #type: ignore
                            graphs.delete_edge(self.clicked_node, closest_node[0]) #type: ignore
                            graphs.create_edge(self.clicked_node, closest_node[0], False, edge_value)
                        elif not graphs.get_edge(self.clicked_node, closest_node[0]).directed: #type: ignore
                            edge_value = graphs.get_edge(self.clicked_node, closest_node[0]).value #type: ignore
                            graphs.delete_edge(self.clicked_node, closest_node[0]) #type: ignore
                            graphs.create_edge(self.clicked_node, closest_node[0], True, edge_value)


    def middle_mouse_click(self, pos):
        distances = [(node, (node.x - pos[0]) ** 2 + (node.y - pos[1]) ** 2) for node in graphs.get_all_nodes()]
        closest_node = min(distances, key=lambda x: x[1])
        if closest_node[1] <= settings.NODE_SIZE ** 2:
            if len(self.start_end_nodes) == 0:
                self.start_end_nodes.append(closest_node[0])
            elif len(self.start_end_nodes) == 1:
                if closest_node[0] == self.start_end_nodes[0]:
                    self.start_end_nodes = []
                else:
                    self.start_end_nodes.append(closest_node[0])
            elif len(self.start_end_nodes) == 2 and closest_node[0] not in self.start_end_nodes:
                self.start_end_nodes[1] = closest_node[0]
            elif len(self.start_end_nodes) == 2 and closest_node[0] in self.start_end_nodes:
                self.start_end_nodes.remove(closest_node[0])
    
    def mouse_wheel_scroll(self, y):
        pos = pygame.mouse.get_pos()

        all_mid_points = []
        for edge in graphs.get_all_edges():
            mid_point = (edge, ((edge.node1.x + edge.node2.x) / 2, (edge.node1.y + edge.node2.y) / 2))
            all_mid_points.append(mid_point)
        

        distances = [(edge, (mid_point[0] - pos[0]) ** 2 + (mid_point[1] - pos[1]) ** 2) for edge, mid_point in all_mid_points]
        closest_mid_point = min(distances, key=lambda x: x[1])

        if closest_mid_point[1] <= settings.NODE_SIZE ** 2:
            edge = closest_mid_point[0]
            if edge.value + y >= 0:
                edge.value += y

    def check_buttons(self):
        for i in self.buttons:
            i.check_click()

    def check_event(self):
        #verifie les evenement pygame
        for event in pygame.event.get():
            #input de la croix rouge (en haut a droite de la fenetre)
            if event.type == pygame.QUIT:
                self.running = False
            
            #check le temps
            if event.type == pygame.USEREVENT:
                self.every_ten_milli_sec_action()
            
            #input de la souris
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    #left
                    self.check_buttons()
                    self.left_mouse_click(event.pos)

                elif event.button == 3:
                    #right
                    self.right_mouse_click(event.pos)
                
                elif event.button == 2:
                    #middle
                    self.middle_mouse_click(event.pos)
            
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    #left
                    self.left_mouse_release(event.pos)

                elif event.button == 3:
                    #right
                    self.right_mouse_release(event.pos)
                
                elif event.button == 2:
                    #middle
                    pass
            
            if event.type == pygame.MOUSEWHEEL:
                self.mouse_wheel_scroll(event.y)

            #check input clavier
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                
                if event.key == pygame.K_m:
                    graphs.print_adjacency_matrix()
        #other
        #self.test.


    def refresh(self):
        #refresh l'ecran
        pygame.display.flip()

    def update(self):
        #delete tous sur l'ecran
        self.screen.fill((220, 220, 220))

        for i in self.buttons:
            i.draw(self.screen)
        
        if len(self.start_end_nodes) == 2:
            distance, path = algorithms.dijkstra(self.start_end_nodes[0], self.start_end_nodes[1])
        else:
            path = []
                
        for node in graphs.get_all_nodes():
            node.draw(self.screen, self.start_end_nodes, path)
        
        for edge in graphs.get_all_edges():
            edge.draw(self.screen, path)
        
        if self.left_mouse_down:
            pos = pygame.mouse.get_pos()
            self.clicked_node.set_position(pos[0], pos[1])
        
        
    def run(self):
        #boucle global du jeu
        while self.running:
            self.check_event()
            self.update()
            self.refresh()
        
        graphs.save_graph_to_json('graph.json')
    
    def every_ten_milli_sec_action(self):
        pass
    
#import pygame et les differentes classes

#start un event toute les 10 milli sec
pygame.time.set_timer(pygame.USEREVENT, 10)

#set taille fenetre
screen_width = settings.SCREEN_WIDTH

screen_height = settings.SCREEN_HEIGHT

#set la fenetre
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("default")

#cree le jeu a partir le l'objet 'game'
game1 = Game(screen, screen_width, screen_height)

#lance la boucle global
game1.run()

#quitte pygame
pygame.quit()

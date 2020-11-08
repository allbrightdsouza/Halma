#!/usr/bin/env python
# coding: utf-8

# In[89]:


from time import time
import random
from heapq import heappush, heappop


# In[104]:


global global_move
class Halma:
    def __init__(self,mode,color,time_left,board):
        self.mode = mode
        self.p_color = color
        self.e_color = 'B' if color == 'W' else 'W'
        self.baseClear = { 'B' : 0 , 'W' : 0}
        self.time_left = time_left
        self.game_time = time_left
        self.board_state = board
        self.playerPos,self.enemyPos = self.getPieces(board, mode)
        self.MoveCounter = 0
        self.pruneCounter = 0
        
    def getPieces(self,board,mode):
        player = set()
        enemy = set()
        for group in goal:
            for goalPos in goal[group]:
                if('W' == group and board[goalPos[1]][goalPos[0]] == 'B'):#group white implies B base
                    self.baseClear['B'] += 1
                if('B' == group and board[goalPos[1]][goalPos[0]] == 'W'): #group white implies B base
                    self.baseClear['W'] += 1
        print(self.baseClear)         
        for y in range(16):
            for x in range(16):
                if board[y][x] == self.p_color:
                    player.add((x,y))
#                     if (x,y) in goal[self.e_color]:
#                         self.baseClear[self.p_color] += 1;
                elif board[y][x] == self.e_color:
                    enemy.add((x,y))
#                     if (x,y) in goal[self.p_color]:
#                         self.baseClear[self.e_color] += 1;
        return player,enemy
    
    def minimax(self,depth = 3):
        global global_move
        time_fail = False
        best_val = -float('inf')
#         beta = float('inf')
        path = {}
        count = 0
        chosen_move = None
        if(self.baseClear[self.p_color] != 0):
            nextMoves,path = self.getMoveBegin(is_player = True,get_path = True)
            count = len(nextMoves)
#             print('No. of Moves Beg',count)
#                 self.playerPos[self.playerPos.index(move[0])] = move[1]
                
        else:
            nextMoves,path = self.getMoves(is_player = True, get_path = True)
            count = len(nextMoves)
#             print('No. of Moves Beg',count)
        
        while len(nextMoves) != 0 and not time_fail:
            move = heappop(nextMoves)[1]
            count -= 1
            self.move_swap(move)
            self.pos_swap(move[0],move[1],isPlayer = True)
#                 self.playerPos[self.playerPos.index(move[0])] = move[1]

            val,time_fail = self.getMinValue(depth = depth-1)
#             print(move," Score ", val, " rem ", count )

#                 print(move,val, ' rem ', len(nextMoves))
            self.move_swap(move)
            self.pos_swap(move[1],move[0],isPlayer = True)
#                 self.playerPos[self.playerPos.index(move[1])] = move[0]
#                 print("Val n move",val,move)
            if val >= best_val:
                best_val = val
#                 selected_state = state
                chosen_move = move

        print("max score of root: " ,str(best_val))
        print("best move: " , chosen_move)
        global_move = chosen_move
        return self.find_path(path,chosen_move), time_fail
   
        
    def getMaxValue(self,alpha = float("-inf"), beta = float("inf"),time_left = 0, timed = True, depth = 3):
        win,rem = self.find_winner()
        time_fail = self.game_time < time() - start_time or (self.mode == 'GAME' and self.time_left*0.9 <time() - start_time)
        
        if win or depth == 0 or (timed and time_fail):
            return self.Eval(rem),time_fail
        
        val = float('-inf')

        if(self.baseClear[self.p_color] != 0) :
            nextMoves,_ = self.getMoveBegin(is_player = True)        
        else:
            nextMoves,_ = self.getMoves(is_player = True)
        time_fail
        while len(nextMoves) != 0:
            move = heappop(nextMoves)[1]
            #do move
            self.move_swap(move)
            self.pos_swap(move[0],move[1],isPlayer = True)
#                 self.playerPos[self.playerPos.index(move[0])] = move[1]
            temp_val,time_fail = self.getMinValue(alpha, beta, depth = depth - 1)
            val = max(val, temp_val)            

            #undo move
            self.move_swap(move)
            self.pos_swap(move[1],move[0],isPlayer = True)
#                 self.playerPos[self.playerPos.index(move[1])] = move[0]

            self.MoveCounter += 1 

            if val >= beta:
                return val,time_fail
            alpha = max(alpha, val)
        return val,time_fail

    def getMinValue(self, alpha = float("-inf"), beta = float("inf"),time_left = 0, timed = True, depth = 3 ):
#         print ("min at: " + node.Name)
        win,rem = self.find_winner()
        time_fail = self.game_time < time() - start_time or (self.mode == 'GAME' and self.time_left*0.9 <time() - start_time)
        if win or depth == 0 or (timed and time_fail ):
            return self.Eval(rem), time_fail
        
        val = float('inf')
        
        if(self.baseClear[self.e_color] != 0) :
            nextMoves,_ = self.getMoveBegin(is_player = False)
        else:
            nextMoves,_ = self.getMoves(is_player = False)

        while len(nextMoves) != 0:
            move = heappop(nextMoves)[1]
            self.move_swap(move)
            self.pos_swap(move[0],move[1],isPlayer = False)

#                 self.enemyPos[self.enemyPos.index(move[0])] = move[1]
            temp_val, time_fail = self.getMaxValue(alpha, beta, depth = depth - 1)
            val = min(val, temp_val)

            self.move_swap(move)
            self.pos_swap(move[1],move[0],isPlayer = False)

#                 self.enemyPos[self.enemyPos.index(move[1])] = move[0]

            self.MoveCounter += 1 

            if val <= alpha:
                return val, time_fail
            beta = min(beta, val)

        return val, time_fail
            
    def getMoveBegin(self,is_player,get_path = False):
        base_camp = goal[self.e_color] if is_player else goal[self.p_color]
        cur_pieces = self.playerPos if is_player else self.enemyPos
        cur_color = self.p_color if is_player else self.e_color
        
        out_of_camp = []
        uniq_moves = set()

        within_camp = []
        path = {}
        
        for piece in cur_pieces:
            jump = []
            low = -1
            high = 2
            cond = 0
            if piece in base_camp:
#                 print(piece)
                if cur_color == 'B':
                    cond = 0
                else:
                    cond = 1
#                 print('low n high',low,high)
            else:
                    continue
#                 print(piece,"\n",base_camp)
            
            for x in range(low,high):                
                for y in range(low,high):
                    new_pos = piece[0] + y, piece[1] + x
                    
                    #Eliminate Degenerate adj moves
                    if new_pos == piece or (new_pos[0] < 0) or (new_pos[1] < 0) or (new_pos[0] > 15) or (new_pos[1] > 15):
#                         print('Degenerate but false',new_pos == piece)
                        continue
                    
                    back_move = False
                    if cond == 0 and ((x + y) <= 0): #Black
                        back_move = True
                    if cond == 1 and ((x + y) >= 0): #WHITE
                        back_move = True
#                     if low != 0 and high != 1 and new_pos in base_camp:
#                         print('enter here?')
#                         continue
                    
#                     if(new_pos in goal[cur_color]):
#                         npriority = cpriority + 1
#                     else:
#                         npriority = cpriority    
                    if self.board_state[new_pos[1]][new_pos[0]] == '.':
                        if not back_move:
                            if(new_pos in base_camp):
                                heappush(within_camp,(0,(piece,new_pos)))
                            else:
                                heappush(out_of_camp,(0,(piece,new_pos)))
                
                        
#                         uniq_moves[(piece,new_pos)] = True not needed

#                         if(get_path)
#                             path[new_pos] = piece
                    else:
                        new_pos = piece[0] + y*2, piece[1] + x*2
                        #Eliminate Degenerate jump moves
                        if (new_pos[0] < 0) or (new_pos[1] < 0) or (new_pos[0] > 15) or (new_pos[1] > 15):
#                             print('jump degenrate')
                            continue
#                         if low != 0 and high != 1 and new_pos in base_camp:
#                             continue
                            
                        if self.board_state[new_pos[1]][new_pos[0]] == '.':
                            if(new_pos in base_camp):
                                heappush(within_camp,(0,(piece,new_pos)))
                            else:
                                heappush(out_of_camp,(0,(piece,new_pos)))
#                             uniq_moves[(piece,new_pos)] = True
                            uniq_moves.add((piece,new_pos))

                            if(get_path):
                                path[(new_pos,piece)] = piece
#                             if piece in 
#                             moves.append((piece,new_pos)) #append first jump
                            jump.append(new_pos) #append pos to check for more jumps
            
            while len(jump) > 0:
                cur_pos = jump.pop()
                
                low = -1
                high = 2
                cond  = 0
                if cur_pos in base_camp:
                    if cur_color == 'B':
                        cond = 0
                    else:
                        cond = 1
#                 else:
#                     print('Comes here even though you thought it wouldnt')
#                     continue
                for x in range(low,high):                
                    for y in range(low,high):
                        new_pos = cur_pos[0] + y*2, cur_pos[1] + x*2
                        #Eliminate Degenerate jump moves
                        if (new_pos[0] < 0) or (new_pos[1] < 0) or (new_pos[0] > 15) or (new_pos[1] > 15):
                            continue
                        if cond == 0 and ((x + y) <= 0): #Black
                            continue
                        if cond == 1 and ((x + y) >= 0): #WHITE                       
                            continue
#                         if low != 0 and high != 1 and new_pos in base_camp:
#                             continue
                            
                        if self.board_state[new_pos[1] - x ][new_pos[0] - y] != '.'                         and self.board_state[new_pos[1]][new_pos[0]] == '.' and (piece,new_pos) not in uniq_moves:
                            
                            if(new_pos in base_camp):
                                heappush(within_camp,(0,(piece,new_pos)))
                            else:
                                heappush(out_of_camp,(0,(piece,new_pos)))
                            
                            if(get_path):
                                path[(new_pos,piece)] = cur_pos
#                             uniq_moves[(piece,new_pos)] = True
                            uniq_moves.add((piece,new_pos))

#                             moves.append((piece,new_pos)) #append first jump
                            jump.append(new_pos) #append pos to check for more jumps
          
#         if -1 in moves:
#             print('-1 exits')
        # if(get_path):
        #     print(out_of_camp)            
        #     print(within_camp)

        if(len(out_of_camp) > 0):
            return out_of_camp,path
        if(len(out_of_camp) == 0 and len(within_camp) == 0):
            return self.getMoves(is_player,get_path)
        return within_camp,path
            
    def getMoves(self,is_player,get_path = False):
        uniq_moves = set()
        def euclid_dist(p1, p2):
            (x1, y1) = p1[0],p1[1]
            (x2, y2) = p2[0],p2[1]
            dx = abs(x1 - x2)
            dy = abs(y1 - y2)
            return min(dx,dy) + abs(dx-dy)
#         print('Im here')
#         def euclid_dist(p1, p2):
#             return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
        
        base_camp = goal[self.e_color] if is_player else goal[self.p_color]
        cur_pieces = self.playerPos if is_player else self.enemyPos
        cur_color = self.p_color if is_player else self.e_color
        #Get Adj moves
        moves = []
        path = {}
#         begin_moves = { 0 : [] , 1 : [], -1 : []}
#         cur_pieces = [(10,15)]
        for piece in cur_pieces:
            jump = []
            low = -1
            high = 2
            cpriority = 0
            npriority = 0
#             if piece in base_camp:
#                 print('should not come here')
#                 if (0,0) in base_camp:
#                     low = 0
#                 else:
#                     high = 1
# #                 print('low n high',low,high)
# #                 print('Comes here even though you thought it wouldnt')
#             else:
#                 if(self.baseClear[cur_color] != 0):
# #                     print('im here')
#                     continue
#                 print(piece,"\n",base_camp)
            if piece in base_camp:
                continue
            if piece in goal[cur_color]:
                cpriority = 32
                if cur_color == 'B':
#                     print(cur_color)
                    low = 0
                else:
                    high = 1
            
            for x in range(low,high):                
                for y in range(low,high):
                    new_pos = piece[0] + y, piece[1] + x
                    
                    #Eliminate Degenerate adj moves
                    if new_pos == piece or (new_pos[0] < 0) or (new_pos[1] < 0) or (new_pos[0] > 15)                     or (new_pos[1] > 15):
                        continue
                    if low != 0 and high != 1 and new_pos in base_camp:
                        continue
                    
                    if(new_pos in goal[cur_color]):
                        npriority = cpriority - 32
                    else:
                        npriority = cpriority   
                        
                    if self.board_state[new_pos[1]][new_pos[0]] == '.':
                        if cur_color == 'B':
                            npriority += euclid_dist(new_pos,(15,15))
                        else:
                            npriority += euclid_dist(new_pos,(0,0))
                            
                        heappush(moves,(npriority,(piece,new_pos)))
#                         uniq_moves[(piece,new_pos)] = True not needed

#                         moves[npriority].append((piece,new_pos)) #append adjmove
#                         if(get_path)
#                             path[new_pos] = piece
                    else:
                        new_pos = piece[0] + y*2, piece[1] + x*2
                        #Eliminate Degenerate jump moves
                        if (new_pos[0] < 0) or (new_pos[1] < 0) or (new_pos[0] > 15) or (new_pos[1] > 15):
                            continue
                        if new_pos in base_camp: # prevent back to base moves
                            continue
                        if(new_pos in goal[cur_color]):
                            npriority = cpriority - 32
                        else:
                            npriority = cpriority
                        
                        
                        if self.board_state[new_pos[1]][new_pos[0]] == '.':
                            
                            if cur_color == 'B':
                                npriority += euclid_dist(new_pos,(15,15))
                            else:
                                npriority += euclid_dist(new_pos,(0,0))

                            heappush(moves,(npriority,(piece,new_pos)))
#                             uniq_moves[(piece,new_pos)] = True
                            uniq_moves.add((piece,new_pos))

                            if(get_path):
                                path[(new_pos,piece)] = piece
#                             if piece in 
#                             moves.append((piece,new_pos)) #append first jump
                            jump.append(new_pos) #append pos to check for more jumps
            
            while len(jump) > 0:
                cur_pos = jump.pop()
                
                low = -1
                high = 2
#                 if cur_pos in base_camp:
#                     if cur_color == 'B':
#                         low = 0
#                     else:
#                         high = 1
                        
                for x in range(low,high):                
                    for y in range(low,high):
                        new_pos = cur_pos[0] + y*2, cur_pos[1] + x*2
                        #Eliminate Degenerate jump moves
                        if (new_pos[0] < 0) or (new_pos[1] < 0) or (new_pos[0] > 15) or (new_pos[1] > 15):
                            continue
#                         if low != 0 and high != 1 and new_pos in base_camp: # prevent back to base moves
                        if new_pos in base_camp: # prevent back to base moves
                            continue
                        
                        if(new_pos in goal[cur_color]):
                            npriority = cpriority - 32
                        else:
                            npriority = cpriority
                        
#                         if cur_color == 'B' and new_pos[1] > piece[1] and new_pos[0] > piece[0]:
#                             npriority += 1
#                         if cur_color == 'W' and new_pos[1] < piece[1] and new_pos[0] < piece[0]:
#                             npriority += 1
                            
                        if self.board_state[new_pos[1] - x ][new_pos[0] - y] != '.'                         and self.board_state[new_pos[1]][new_pos[0]] == '.' and (piece,new_pos) not in uniq_moves:
                            if cur_color == 'B':
                                npriority += euclid_dist(new_pos,(15,15))
                            else:
                                npriority += euclid_dist(new_pos,(0,0))
#                             uniq_moves[(piece,new_pos)] = True
                            uniq_moves.add((piece,new_pos))

                            heappush(moves,(npriority,(piece,new_pos)))
#                             moves.append((piece,new_pos)) #append first jump
                            if(get_path):
                                path[(new_pos,piece)] = cur_pos
                            jump.append(new_pos) #append pos to check for more jumps
          
        return moves,path
        
            
    
    def move_swap(self,move):
        #Board
        from_pos = move[0]
        to_pos = move[1]
        temp = self.board_state[from_pos[1]][from_pos[0]]        
        self.board_state[from_pos[1]][from_pos[0]] = self.board_state[to_pos[1]][to_pos[0]]  
        self.board_state[to_pos[1]][to_pos[0]] = temp
        
        #piece
    def pos_swap(self,a_pos,b_pos,isPlayer):
        #                 self.playerPos[self.playerPos.index(move[0])] = move[1]
        if isPlayer:
            self.playerPos.add(b_pos)
            self.playerPos.discard(a_pos)
        else:
            self.enemyPos.add(b_pos)
            self.enemyPos.discard(a_pos)
        
     
    def find_winner_old(self):
        rem = [19,19]
        count = 0
        for p in self.playerPos: 
            if p in goal[self.p_color]:
                count += 1
        if count != 0:
            for e in self.enemyPos: 
                if e in goal[self.p_color]:
                    count += 1
            rem[0] -= count
            if count == 19:
                return 1,rem
        else:
            for e in self.enemyPos: 
                if e in goal[self.p_color]:
                    count += 1
            rem[0] -= count

        count = 0
        for p in self.enemyPos:
            if p in goal[self.e_color]:
                count += 1
        if count != 0:
            for e in self.playerPos:
                if e in goal[self.e_color]:
                    count += 1
            rem[1] -= count
            if count == 19:
                return 2,rem
        else:
            for e in self.playerPos:
                if e in goal[self.e_color]:
                    count += 1
            rem[1] -= count
        return 0,rem
    
    def find_winner(self):
        rem = [19,19]
        count = 0
        for p in self.playerPos: 
            if p in goal[self.p_color]:
                count += 1
#         if count != 0:
#             for e in self.enemyPos: 
#                 if e in goal[self.p_color]:
#                     count += 1
        rem[0] -= count
        if count == 19:
            return 1,rem
#         else:
#             for e in self.enemyPos: 
#                 if e in goal[self.p_color]:
#                     count += 1
#             rem[0] -= count

        count = 0
        for p in self.enemyPos:
            if p in goal[self.e_color]:
                count += 1
#         if count != 0:
#             for e in self.playerPos:
#                 if e in goal[self.e_color]:
#                     count += 1
        rem[1] -= count
        if count == 19:
            return 2,rem
#         else:
#             for e in self.playerPos:
#                 if e in goal[self.e_color]:
#                     count += 1
#             rem[1] -= count
        return 0,rem
   
    def Eval_old(self,rem):
#         canPrint = False
        
#         if self.board_state[13][11] == 'B' or self.board_state[14][12] == 'B':
#             canPrint = True
#         def euclid_dist(p1, p2):
#             return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
        def euclid_dist(p1, p2):
            (x1, y1) = p1[0],p1[1]
            (x2, y2) = p2[0],p2[1]
            dx = abs(x1 - x2)
            dy = abs(y1 - y2)
            return min(dx,dy) + abs(dx-dy)
#         pMoves = len(self.getMoves(is_player = True))
#         eMoves = len(self.getMoves(is_player = False))
# #         print('Moves',pMoves,eMoves)
#         moveScore = (pMoves - eMoves)
        
        pDist = 0
        pbaseCounter = 0
        for pPos in self.playerPos:
            distances = [ euclid_dist(pPos,goalPos) for goalPos in goal[self.p_color] if self.board_state[goalPos[1]][goalPos[0]] != self.p_color ]
#             pbaseCounter += 1 if pPos in goal[self.p_color] else 0
            pDist -=  max(distances) if len(distances) else -50
        eDist = 0
        ebaseCounter = 0
        for ePos in self.enemyPos:
            distances = [ euclid_dist(ePos,goalPos) for goalPos in goal[self.e_color] if self.board_state[goalPos[1]][goalPos[0]] != self.e_color ]
#             ebaseCounter += 1 if ePos in goal[self.e_color] else 0
            eDist +=  max(distances) if len(distances) else 50
        
        
        distScore = pDist + eDist
#         if canPrint:
#             print('Dist',pDist,eDist,pDist + eDist,distScore)
        
        pbaseScore = 400*(19 - rem[0])/19
        ebaseScore = -400*(19 - rem[1])/19
        
#         if canPrint:
#             print('Counter p and e',pbaseCounter,ebaseCounter)
#         Find_winner_old
#         if pbaseCounter:
#             pbaseScore = 400*(pbaseCounter)/(rem[0]+pbaseCounter)
#         if ebaseCounter:
#             ebaseScore = -400*(ebaseCounter)/(rem[1]+ebaseCounter)
        
        baseScore = pbaseScore + ebaseScore #modify this to be the ratio remaing space occupied to base camputure 
#         if canPrint:
#             print('Base p and e',pbaseScore,ebaseScore,pbaseScore + ebaseScore,baseScore)

#         if baseScore + distScore == 1226.8473468770558:
#             print_board(self.board_state)
#             print('\n\n\n')
        
        return baseScore + distScore        
    
#         return distScore
#         return moveScore + baseScore + distScore
    def Eval(self,rem):
        black_targets = [[(15,15)], 
                         [(14,14), (15,14), (14,15)], 
                         [(13,13), (13,14), (13,15), (14,13), (15,13)],
                         [(12,13), (12,14), (12,15), (13,12), (14,12), (15,12)],
                         [(11,14), (11,15), (14,11), (15,11)]
                        ]
        
        white_targets = [[(0,0)], 
                         [(1,1), (0,1), (1,0)], 
                         [(2,2), (2,1), (2,0), (1,2), (0,2)],
                         [(3,2), (3,1), (3,0), (2,3), (1,3), (0,3)],
                         [(4,1), (4,0), (1,4), (0,4)]
                        ]
        
        def euclid_dist(p1, p2):
            (x1, y1) = p1[0],p1[1]
            (x2, y2) = p2[0],p2[1]
            dx = abs(x1 - x2)
            dy = abs(y1 - y2)
            return min(dx,dy) + abs(dx-dy)
        
        pDist = 0
        
#         black_target_corner = black_targets[0]  
#         white_target_corner = white_targets[0]
#         for target in black_targets:
#             if (self.board_state[target[1]][target[0]] != 'B'):
#                 black_target_corner = target
#                 break
        
#         for target in white_targets:
#             if (self.board_state[target[1]][target[0]] != 'W'):
#                 white_target_corner = target
#                 break        
        for pPos in self.playerPos:
#             distances = [ euclid_dist(pPos,goalPos) for goalPos in goal[self.p_color] if self.board_state[goalPos[1]][goalPos[0]] != self.p_color ]
#             pDist -=  max(distances) if len(distances) else -50
            if pPos not in goal[self.p_color]:
                if self.p_color == 'B':
                    found = False
                    min_dist = float('inf')
                    for target_camp in black_targets:
                        for target in target_camp:
                            if (self.board_state[target[1]][target[0]] != 'B'):
                                found = True
                                min_dist = min(min_dist,euclid_dist(pPos, target)) 
#                                 print("Balck, ", pPos, target)
                        if found:
                            break
    #                     
    #                 pDist -= euclid_dist(pPos, black_target_corner)
                    pDist -= min_dist
                else:
                    found = False
                    min_dist = float('inf')
                    for target_camp in white_targets:
                        for target in target_camp:
                            if (self.board_state[target[1]][target[0]] != 'W'):
                                found = True
                                min_dist = min(min_dist,euclid_dist(pPos, target))    
#                                 print("white, ", pPos, target)
                        if found:
                            break


                    pDist -= min_dist
#                 pDist -= euclid_dist(pPos, white_target_corner)

        eDist = 0
        for ePos in self.enemyPos:
#             distances = [ euclid_dist(ePos,goalPos) for goalPos in goal[self.e_color] if self.board_state[goalPos[1]][goalPos[0]] != self.e_color ]
#             eDist +=  max(distances) if len(distances) else -50
            if ePos not in goal[self.e_color]:
                if self.e_color == 'B':
                    found = False
                    min_dist = float('inf')
                    for target_camp in black_targets:
                        for target in target_camp:
                            if (self.board_state[target[1]][target[0]] != 'B'):
                                found = True
                                min_dist = min(min_dist,euclid_dist(ePos, target))                    
                        if found:
                            break

                    eDist += min_dist
    #                 eDist += euclid_dist(ePos, black_target_corner)
                else:
                    found = False
                    min_dist = float('inf')
                    for target_camp in white_targets:
                        for target in target_camp:
                            if (self.board_state[target[1]][target[0]] != 'W'):
                                found = True
                                min_dist = min(min_dist,euclid_dist(ePos, target))                    
                        if found:
                            break

                    eDist += min_dist
#                 eDist += euclid_dist(ePos, white_target_corner)
        
        distScore = (pDist + eDist) 
        
        pbaseScore = 400*(19 - rem[0])/19
        ebaseScore = -400*(19 - rem[1])/19
        
        baseScore = pbaseScore + ebaseScore #modify this to be the ratio remaing space occupied to base camputure 
#         if self.board_state[13][14] == '.' and self.board_state[11][12] == 'W' and self.board_state[12][13] == '.' and self.board_state[10][11] == 'W':
#             print("THE FINAL BOARD", distScore)
#             print_board_wspace(self.board_state)
#         if (baseScore + distScore) == 1.0:
#             print("THE FINAL BOARD", distScore)
#             print_board_wspace(self.board_state)

        return baseScore + distScore   
    
    def find_path(self,path,nextMove):
        output = ""
        def euclid_dist(p1, p2):
            (x1, y1) = p1[0],p1[1]
            (x2, y2) = p2[0],p2[1]
            dx = abs(x1 - x2)
            dy = abs(y1 - y2)
            return min(dx,dy) + abs(dx-dy)
        
        start = nextMove[0]
        end = nextMove[1]
        
        if (euclid_dist(start,end) == 1) :
            return 'E '+str(start[0])+','+str(start[1])+" "+str(end[0])+','+str(end[1])
            
        
        while(end != start):
            prev = path[(end,start)]
            output = 'J '+str(prev[0])+','+str(prev[1])+" "+str(end[0])+','+str(end[1]) + '\n'+ output
            end = prev
                
        return output[:-1]
    def set_game_time(self):
        depth = 3
        if self.mode == 'SINGLE' :
            playtime = self.time_left - 10.0
        else:
            try :
                file = open('./playerdata1.txt','r')
                print('Opening file')
                line = file.readline()
                time_val, depth_val = line.strip().split()
                playtime = float(time_val)
                depth = int(depth_val)
                file.close()
                
            except IOError as e:
                print('Creating file',e)
                playtime = (self.time_left - 5.0) / 110.0 #divide remaining time needs to be modified to playerdata1 time
                file = open('./playerdata1.txt','w+')
                output_txt = str(playtime) + ' 3'
                file.write(output_txt)
                file.close()
        
        if playtime < 10.0:
            if playtime <= 0 :
                self.game_time = self.time_left*0.8
            else:
                self.game_time = playtime
#         if self.game_time <= 3:
#             return True
        if self.mode == 'SINGLE': #Split time to both depth 3 and 2
            self.game_time = self.game_time/2.0
        self.game_time = playtime
        return depth


# In[105]:


#Contstants
goal = {
    'W' : {(0,0),(1,0),(2,0),(3,0),(4,0),
               (0,1),(1,1),(2,1),(3,1),(4,1),
               (0,2),(1,2),(2,2),(3,2),
               (0,3),(1,3),(2,3),
               (0,4),(1,4)
          },
    'B' : {(15,15),(14,15),(13,15),(12,15),(11,15),
               (15,14),(14,14),(13,14),(12,14),(11,14),
               (15,13),(14,13),(13,13),(12,13),
               (15,12),(14,12),(13,12),
               (15,11),(14,11)
          }
}


# In[106]:


#Helper functions
def input_reader(filename):
    file = open(filename,'r')
    mode = file.readline().strip()
    color = file.readline().strip() 
    time = float(file.readline().strip())
    board = []
    
    line = file.readline()
    
    while line:
        row = list(line.strip())
        board.append(row)
        line = file.readline()

    return mode,color,time,board

def print_board(board_config):
    output_txt = ""
    for row in board_config:
        for ele in row:
#             print(ele,end="")
            output_txt = output_txt + ele
#         print()
        output_txt = output_txt + '\n'
    return output_txt
def print_board_wspace(board_config):
    output_txt = ""
    for row in board_config:
        for ele in row:
            print(ele," ",end="")
            output_txt = output_txt + ele
        print()
        output_txt = output_txt + '\n'
    return output_txt


# In[107]:


if __name__ == '__main__':
    start_time = time()
    real_start_time = start_time
    game_mode,p_color,time_left,board_config= input_reader('./input.txt')
    print(game_mode,p_color,time_left)
    p_color = 'W' if p_color == 'WHITE' else 'B'
    halma = Halma(game_mode,p_color,time_left,board_config)
#     print_board(halma.board_state)
    time_fail = False
    depth = halma.set_game_time()
#     halma.set_game_time(3)
    print('Decided time and depth',halma.game_time,depth)
    if depth == 3:
        print('Perform depth 3')
        print('Time left',halma.game_time)
        time_fail = sel_move,time_fail = halma.minimax(depth = 3) 
        if time_fail:
            time_elapsed = time() - start_time
            print('Depth 3 fail time taken',time_elapsed)
            if time_elapsed > halma.time_left/2:
                time_fail = False
                print('Switcching depth to 2 for future but not performing depth 2')
                file = open('./playerdata1.txt','w+')
                output_txt = str(halma.game_time) + ' 2'
                file.write(output_txt)
                file.close()
            else:
                print('restarting timer')
                start_time = time()
    
    if time_fail or depth == 2:
        if halma.mode == 'SINGLE':
            halma.game_time = (halma.time_left - (time() - start_time))*0.9
        elif depth != 2:
            print('Switcching depth to 2 for future')
            file = open('./playerdata1.txt','w+')
            output_txt = str(halma.game_time) + ' 2'
            file.write(output_txt)
            file.close()
        print('Perform depth 2')
        print('Time left', halma.game_time)
        sel_move,_ =  halma.minimax(depth = 2)
        
        if depth == 2:
            time_elapsed = time() - start_time
            time_rem = halma.game_time - time_elapsed
            perc = time_rem/halma.game_time
            switch_todepth_3 = random.uniform(0,1) > perc
            if(switch_todepth_3):
                print('Switcching depth back to 3')
                file = open('./playerdata1.txt','w+')
                output_txt = str(halma.game_time) + ' 3'
                file.write(output_txt)
                file.close()
            
    file_output = open('./output.txt','w+')
    file_output.write(sel_move)
    print("Time",time() - start_time)
    act_real_time = time()-real_start_time
    print("RealTime",act_real_time)


# In[108]:


pick_move = global_move
print_board(halma.board_state)
# print_board_wspace(halma.board_state)
halma.move_swap(pick_move)
print('\n')
output_txt = print_board(halma.board_state)
output_board = open('./input.txt','w+')
output_board.write('GAME\n')
if halma.p_color == 'W':
    output_board.write('BLACK\n')
else:
    output_board.write('WHITE\n')
output_board.write("300\n")
output_board.write(output_txt)
output_board.close()
# print_board_wspace(halma.board_state)
halma.move_swap(pick_move)


# In[98]:


# SINGLE
# BLACK
# 201.45
# WWWWW...........
# WWWW............
# WWWW............
# WW..............
# WW..............
# ....W...........
# ...W............
# ................
# ................
# ................
# ................
# ..........B.....
# ............BBBB
# ...........BBBBB
# ...........BBBBB
# ............BBBB


# In[ ]:





# In[ ]:





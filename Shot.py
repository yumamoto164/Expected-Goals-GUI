class Player():
    def __init__(self, team, number, name):
        self.team = team
        self.number = number
        self.name = name
        
    def getTeam(self):
        return self.team
    
    def getNumber(self):
        return self.number
    
    def getName(self):
        return self.name
    
    
class Shot():
    def __init__(self, index, team, player_name, player_number, on_target, goal, x, y, body_part, assist_type, shot_type):
        self.index = index
        self.team = team # String
        self.player_name = player_name
        self.player_number = player_number
        self.on_target = on_target # Boolean
        self.goal = goal # Boolean
        self.x = x
        self.y = y
        self.body_part = body_part # foot:0, other:1
        self.assist_type = assist_type # 'pass': 0, 'recovery': 1, 'clearance': 2, 'direct': 3, 'rebound': 4
        self.shot_type = shot_type # free kick:0, corner:1, throw_in:2, direct_set_piece:3, open_play:4
        
    def getIndex(self):
        return self.index
        
    def getTeam(self):
        return self.team
    
    def getPlayerName(self):
        return self.player_name
    
    def getPlayerNumber(self):
        return self.player_number
    
    def getOnTarget(self):
        return self.on_target
    
    def getGoal(self):
        return self.goal
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getBodyPart(self):
        return self.body_part
    
    def getAssistType(self):
        return self.assist_type
    
    def getShotType(self):
        return self.shot_type
    
    
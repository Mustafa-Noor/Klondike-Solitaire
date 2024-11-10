class Score:
    def __init__(self): # constructor of the class
        self.score = 0

    def addPoints(self, points): # this is add 
        self.score += points
    
    def removePoints(self, points): # this is removing
        self.score -= points
        if(self.score<0):
            self.score = 0

    def getScore(self): # this to get the score
        return self.score
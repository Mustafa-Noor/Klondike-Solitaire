class Score:
    def __init__(self):
        self.score = 0

    def addPoints(self, points):
        self.score += points
    
    def removePoints(self, points):
        self.score -= points
        if(self.score<0):
            self.score = 0

    def getScore(self):
        return self.score
"""
The template of the main script of the machine learning process
"""
import random


class MLPlay:
    def __init__(self,side):
        """
        Constructor
        """
        self.ball_served = False
        self.previous_ball = (0, 0)
        self.pred=100
        self.side="1P"
    def update(self, scene_info):
        """
        Generate the command according to the received `scene_info`.
        """
        # Make the caller to invoke `reset()` for the next round.
        if scene_info["status"] !="GAME_ALIVE":
            return "RESET"
        current_ball = scene_info["ball"]
        if not self.ball_served:
            self.ball_served = True
            command = random.choice(["SERVE_TO_RIGHT", "SERVE_TO_LEFT"]) 
        else:
            # 1.Find Direction
            direction = self.getDirection(self.previous_ball, current_ball)

            self.pred = 100
            if self.previous_ball[1]-scene_info["ball"][1] > 0:  # 球正在往上
                pass
            else:  # 球正在往下，判斷球的落點
                self.pred = scene_info["ball"][0] + ((400 - scene_info["ball"][1]) // 7) * (
                    scene_info["ball"][0] - self.previous_ball[0])

            # 調整predict值
            if self.pred > 400:
                self.pred = self.pred - 400
            elif self.pred < 400 and self.pred > 200:
                self.pred = 200 - (self.pred - 200)
            elif self.pred < -200:
                self.pred = 200 - (abs(self.pred) - 200)
            elif self.pred > -200 and self.pred < 0:
                self.pred = abs(self.pred)

            # 判斷command
            if scene_info["platform_1P"][0]+20 - 5 > self.pred:
                command = "MOVE_LEFT"
            elif scene_info["platform_1P"][0]+20 + 5 < self.pred:
                command = "MOVE_RIGHT"
            else:
                command = "NONE"

        self.previous_ball = scene_info["ball"]
        return command

    def getDirection(self, previous_ball, current_ball):
        if previous_ball[0]-current_ball[0]>0:
            if previous_ball[1]>current_ball[1]>0:
                return 2
            else :
                return 3
        elif previous_ball[0]-current_ball[0]==0:
            return 0
        else:
            if previous_ball[1]>current_ball[1]>0:
                return 1
            else :
                return 4
        """
        result
        1 : top right
        2 : top left
        3 : bottom left
        4 : bottom right
        """

        # TODO
        return 3

    def predictFalling_x(self,previous_ball, current_ball):
        x1=previous_ball[0]
        x2=current_ball[0]
        y1=previous_ball[1]
        y2=current_ball[1]
        if (y1-y2)!=0:
            a=(x1-x2)/(y1-y2)
        else:
            a=0
        if a<0:
            y=y1-a*x1
            if y>=400:
                x=x1-(y1-400)/a
            else:
                x=(y-400)*a
            return x
        else:
            y=y1-a*(x1-200)
            if y>=400:
                x=x1-(y1-400)/a
            else:
                x=(y-400)*(a)+200
            return x


    def getCommand(self, platform_x, predict_x):
        """
        return "MOVE_LEFT", "MOVE_RIGHT" or "NONE"
        """
        if platform_x>predict_x:
            return "MOVE_LEFT"
        elif platform_x<predict_x:
            return "MOVE_RIGHT"
        else:
            return "NONE"
        # TODO

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
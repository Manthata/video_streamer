import matplotlib.pyplot as plt
import numpy as np 

class count:
    def __init__(self, y, cord ):
        Counterline = ((0, 300), (1277, 300))
        Inside = 0
        Outside = 0
        self.y = y 
        self.cord = cord
        self.Counterline = Counterline
        self.Inside = Inside
        self.Outside = Outside
    
    # def line(self, Line):

    #     A = (Line[0][1] - Line[1][1])
    #     # print(Line[0][1], Line[1][1] )
    #     B = (Line[1][0] - Line[0][0])
    #     C = (Line[0][0] * Line[1][1] - Line[1][0] * Line[0][1] )

    #     return A, B, -C

    # def intersection(self, cord, Counterline):
    #     L1 = self.line(Counterline)
    #     print(cord[-2])
    #     L2 = self.line(cord)
    #     D = L1[0] * L2[1] - L1[1] * L2[0]
    #     # Dx = cord[2] * Counterline[1] - cord[1] * Counterline[2]
    #     # Dy = cord[0] * Counterline[2] - cord[2] * Counterline[0]
    #     if D  :
    #         # x = Dx / D
    #         #  y = Dy / D
    #         return True
    #     else:
    #         return False
        
    # def intersect(self, cord, Counterline):
    #     if cord[-1] > 
            
    #         # print(yp)
    #         # if yp[i][1] == self.Counterline[0][1] :
    #         #     return True            
            
    def InOut(self, y, cord):
        # seg = (cord[-1], cord[-2]
        
        y_mean = np.mean(self.y)
        # print("this is the mean of the y", y_mean)
        y_direction = self.cord[-1][1] - y_mean

        # print(y_direction)
        # print(self.Counterline[-1][1])
        
        # Checking if the direction  is negative (indicating the object is moving Up) 
        # AND the centroid is Above the centerline. In this case we increment totalUp
        if y_direction < 0 and  cord[-1][1] > self.Counterline[1][1]:
            self.Inside +=1
            # print(self.Inside)
            #into  the meat section
        elif y_direction > 0 and cord[-1][1] < self.Counterline[1][1]:
            self.Outside +=1
            # print(self.Outside)
        return self.Inside, self.Outside
        


# import numpy as np
# import matplotlib.pyplot as plt

# Line1 = ((6, 200), (1277, 328))

# # x_values = [ Line1[0][0], Line1[1][0]]
# # y_values = [Line1[0][1], Line1[1][1]]

# y1_values = 400, 400
# x1_values = 0, 1200
# y = [343, 346, 345, 348, 346, 344, 342, 352, 356, 357, 358, 357, 358, 358, 357, 358, 355, 355, 356, 354, 356, 355, 356, 354, 357, 360, 362,
#     363, 362, 363, 364, 366, 388, 401, 406, 413, 418, 430, 439, 444, 446, 440, 430, 414, 389, 377, 367, 356, 351, 340, 328, 333, 334, 334]
# x = [350, 351, 352, 376, 359, 353, 352, 349, 351, 351, 350, 351, 351, 353, 370, 359, 355, 371, 378, 362, 355, 372, 378, 362, 353, 347, 375,
#     382, 383, 383, 383, 359, 351, 346, 341, 339, 339, 334, 339, 335, 334, 334, 337, 348, 374, 382, 384, 384, 359, 355, 352, 352, 340, 337]
# cord = [(350, 343), (351, 346), (352, 345), (376, 348), (359, 346), (353, 344), (352, 342), (349, 352), (351, 356), (351, 357), (350, 358), (351, 357), (351, 358), (353, 358), (370, 357), (359, 358), (355, 355), (371, 355), (378, 356), (362, 354), (355, 356), (372, 355), (378, 356), (362, 354), (353, 357), (347, 360), (375, 362),
#         (382, 363), (383, 362), (383, 363), (383, 364), (359, 366), (351, 388), (346, 401), (341, 406), (339, 413), (339, 418), (334, 430), (339, 439), (335, 444), (334, 446), (334, 440), (337, 430), (348, 414), (374, 389), (382, 377), (384, 367), (384, 356), (359, 351), (355, 340), (352, 328), (352, 333), (340, 334), (337, 334)]
# # y = ((0, 400), (1200, 400))
# counter = count(y, cord)
# counter.InOut(y, cord)
# print(counter)
# # fig = plt.figure()
# plt.plot(x, y)
# plt.plot(x1_values, y1_values)
# plt.show()
# plt.savefig




















#!/usr/bin/python
import sys, time
import thread
from random import randrange

from PyQt4 import QtGui, QtCore

class Snake(QtGui.QWidget):
	def __init__(self):
		super(Snake, self).__init__()
		self.initUI()
		
	def initUI(self):
		self.newGame()
		self.setStyleSheet("QWidget { background: #A9F5D0 }") 
		self.setFixedSize(800, 600)
		self.setWindowTitle('Snake Game')
		self.show()
		
	def newGame(self):
		self.score = 0
		self.x = 12;
		self.y = 36;
		self.lastKeyPress = 'RIGHT'
		self.timer = QtCore.QBasicTimer()
		self.x_coor = []
		self.y_coor = []
		self.x_coor.insert(0,12)
		self.y_coor.insert(0,36)
		self.makanan_x = 0
		self.makanan_y = 0
		self.makanan = False
		self.speed = 100
		self.start()
		self.game_over = False
		
	def start(self):
		self.timer.start(self.speed, self)
		self.update()
		
	def drawSnake(self, qp):
		qp.setPen(QtCore.Qt.NoPen)
		qp.setBrush(QtGui.QColor(255, 80, 0, 255))
		for i in range(len(self.x_coor)):
			qp.drawRect(self.x_coor[i], self.y_coor[i], 12, 12)

	def paintEvent(self, event):
		qp = QtGui.QPainter()
		qp.begin(self)
		self.drawSnake(qp)
		self.placeFood(qp)
		self.ScoreText(qp)
		if self.game_over == True:
			self.gameOver(event,qp)
		qp.end()
		
	def gameOver(self, event, qp):
		qp.setPen(QtGui.QColor(0, 34, 3))
		qp.setFont(QtGui.QFont('Decorative', 20))
		qp.drawText(event.rect(), QtCore.Qt.AlignCenter, "GAME OVER")
		
	def direction(self, dir):
		if (dir == "DOWN" and self.x<788 and self.x >0 and self.y+12>0 and self.y+12<588):
			self.y += 12
			self.repaint()
		elif (dir == "UP" and self.x<788 and self.x >0 and self.y-12>0 and self.y-12<588):
			self.y -= 12
			self.repaint()
		elif (dir == "RIGHT" and self.x+12<788 and self.x+12 >0 and self.y>0 and self.y<588):
			self.x += 12
			self.repaint()
		elif (dir == "LEFT" and self.x-12<788 and self.x-12 >0 and self.y>0 and self.y<588):
			self.x -= 12
			self.repaint()
		else:
			self.game_over= True
			
		self.x_coor.insert(0,self.x)
		self.y_coor.insert(0,self.y)
		if self.makanan_x == self.x and self.makanan_y == self.y:
			self.makanan = False
			self.score+=1
		else:
			self.x_coor.pop()
			self.y_coor.pop()
		
	def keyPressEvent(self, e):
		if e.key() == QtCore.Qt.Key_Up and self.lastKeyPress != 'UP' and self.lastKeyPress != 'DOWN':
			self.direction("UP")
			self.lastKeyPress = 'UP'
		elif e.key() == QtCore.Qt.Key_Down and self.lastKeyPress != 'DOWN' and self.lastKeyPress != 'UP':
			self.direction("DOWN")
			self.lastKeyPress = 'DOWN'
		elif e.key() == QtCore.Qt.Key_Left and self.lastKeyPress != 'LEFT' and self.lastKeyPress != 'RIGHT':
			self.direction("LEFT")
			self.lastKeyPress = 'LEFT'
		elif e.key() == QtCore.Qt.Key_Right and self.lastKeyPress != 'RIGHT' and self.lastKeyPress != 'LEFT':
			self.direction("RIGHT")
			self.lastKeyPress = 'RIGHT'
		elif e.key() == QtCore.Qt.Key_Escape:
			self.close()

	def placeFood(self, qp):
		if self.makanan == False:
			self.makanan_x = randrange(65)*12
			self.makanan_y = randrange(2, 49)*12
			if not self.makanan_x in self.x_coor and not self.makanan_y in self.y_coor:
				self.makanan = True;
		qp.setBrush(QtGui.QColor(80, 180, 0, 160))
		qp.drawRect(self.makanan_x, self.makanan_y, 12, 12)
		
	def ScoreText(self, qp):
		qp.setPen(QtGui.QColor(0, 0, 0))
		qp.setFont(QtGui.QFont('Decorative', 10))
		qp.drawText(10, 580, "SCORE: " + str(self.score)) 
	
	def timerEvent(self, event):
		if event.timerId() == self.timer.timerId():
			self.direction(self.lastKeyPress)
			self.repaint()
		else:
			QtGui.QFrame.timerEvent(self, event)
			
def main():
	app = QtGui.QApplication(sys.argv)
	ex = Snake()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()


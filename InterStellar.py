import pyengine;
from pyengine import py;
import random;
import time;

class Main:
	def __init__(self):
		py.init();
		self.Disp = pyengine.Display((800,600));
		self.Map = pyengine.Map();
		self.nimbus = pyengine.Ship(self.Map,self.Disp);
		self.Disp.setnimbus(self.nimbus);
		self.Disp.setmap(self.Map);
		self.right ,self.left ,self.accelerate= False,False,False;
		self.deg=0.0;self.stop = False;
		pass;

	def eventhandler(self):
		
		for event in py.event.get():
			if event.type == py.QUIT:
				py.quit();

			elif event.type == 2:
				if event.key == 275:
					self.right = True

				elif event.key == 276:
					self.left = True;

				elif event.key == 273:
					self.accelerate = True;

				elif event.key == 115:
					self.stop = True;

				elif event.key == 113:
					py.quit();

			elif event.type == 3:
				if event.key == 275:
					self.right = False;

				elif event.key == 276:
					self.left = False;

				elif event.key == 273:
					self.accelerate = False;

				elif event.key == 115:
					self.stop = False;


	def rotate(self):
		if self.left == True:
			if self.deg>=0:
				self.deg-=1.;
				self.nimbus.rotate(self.deg);
			else:
				self.deg+=360;
				self.nimbus.rotate(self.deg);

		elif self.right == True:
			if self.deg<=360:
				self.deg+=1.;
				self.nimbus.rotate(self.deg);
			else:
				self.deg = self.deg-360;
				self.nimbus.rotate(self.deg);


	def stoper(self,dt):
		if self.stop == True:
			self.nimbus.stop(dt);

	def speedup(self):
		if self.accelerate == True:
			self.nimbus.accel();

	def action(self,dt):
		self.eventhandler();
		self.nimbus.map.update();
		self.rotate();
		self.speedup();
		self.stoper(dt);
		self.nimbus.update(dt);
		self.nimbus.place();
		self.Disp.DrawPlanets();

	def run(self):
		previoustime = 0;
		currenttime = time.time();

		while True:
			self.Disp.win.fill((30,0,20));
			previoustime = currenttime;
			currenttime = time.time();
			dt = currenttime-previoustime;
			if dt>0.15:
				dt = 0.15;
			self.action(dt);
			self.Disp.parameters();
			py.display.update();



if __name__ == '__main__':
	InterStellar = Main();
	InterStellar.run();
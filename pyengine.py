import pygame as py;
import numpy as np;
import time
import random;

global shipcoords,orshipcoords,white;
shipcoords = [];
orshipcoords = [];
white = (255,255,255);

class Display:
	def __init__(self,size):
		self.scrsize = size;
		self.centerx = int(size[0]/2);
		self.centery = int(size[1]/2);
		self.orgin = np.array([self.centerx,self.centery],int);
		self.win = py.display.set_mode(size);
		py.display.set_caption('InterStellar');
		self.shipcoord();

	def setnimbus(self,nimbus):
		self.ship = nimbus;

	def setmap(self,Map):
		self.map = Map;
	
	def parameters(self):
		degree = str(np.degrees(self.ship.rad))
		fontinst = py.font.Font('freesansbold.ttf',15);

		surfinst = fontinst.render('degree: '+degree,True,white);
		textrectobj = surfinst.get_rect();
		textrectobj.center = (50,20);
		self.win.blit(surfinst,textrectobj);

		surfinst = fontinst.render('fuel: '+str(int(self.ship.fuel)),True,white);
		textrectobj = surfinst.get_rect();
		textrectobj.center = (40,40);
		self.win.blit(surfinst,textrectobj);

		surfinst = fontinst.render('speed: '+str(int(np.linalg.norm(self.ship.velocity))),True,white);
		textrectobj = surfinst.get_rect();
		textrectobj.center = (40,60);
		self.win.blit(surfinst,textrectobj);

		surfinst = fontinst.render('position: '+str(self.ship.map.shippos.astype(int)),True,white);
		textrectobj = surfinst.get_rect();
		textrectobj.center = (40,80);
		self.win.blit(surfinst,textrectobj);

	def shipcoord(self):
		shipcoords.extend([[-30,25],[0,-45],[30,25],[0,0],[-5,35],[-5,25],[5,35],[5,25],[-5,35],[5,35],[-30,25],[-5,35],[30,25],[5,35]]);
		for i in xrange(len(shipcoords)):
			orshipcoords.append(self.o(shipcoords[i]));

	def DrawPlanets(self):
		pos = [];
		for i in xrange(len(self.map.celestia)):
			pos.append(self.map.celestia[i].pos);
		displaycoord = self.Planetcoord(pos);
		for i in xrange(len(self.map.celestia)):
			py.draw.circle(self.win,white,displaycoord[i].astype(int),self.map.celestia[i].radius,1);

		pass;

	def o(self,coord):
		return np.array([coord[0]+self.centerx,coord[1]+self.centery],int);

	def Planetcoord(self,planetsmappositionlists):
		planetspositions = [];
		for i in xrange(len(planetsmappositionlists)):
			shippos = np.array([self.ship.map.shippos[0],-self.ship.map.shippos[1]],int);
			planetspositions.append(planetsmappositionlists[i] -shippos)
			planetspositions[i]+=np.array([self.centerx,self.centery],int);

		return planetspositions;
		

class Star:
	def __init__(self,pos,gravity,size,n):
		self.pos = pos;
		self.gravity = gravity
		self.size = size;
		self.n_of_planets = n;
		self.OUG = [];#OUG means object under gravity

	def setup(self,lists):
		self.OUG.extend(lists);

	def update(self):
		for i in xrange(len(self.OUG)):
			direc = self.pos -self.OUG[i].pos;
			vectorG = (direc/np.linalg.norm(direc))*(self.g*1/(np.linalg.norm(direc)**2))
			self.OUG[i].temppos = self.OUG[i].pos;
			self.OUG[i].temppos += self.OUG[i].velocity;



class Planet:
	def __init__(self):
		self.sun = None;
		self.radius = 0;
		self.gravity  = 0;
		self.issatellites = False;
		self.pos = np.array([0,0],float);



	def setup(self,r,g,sat,pos,star):
		self.sun = star;
		self.radius = r;self.gravity = g;
		self.issatellites = sat;self.pos = np.array(pos,float);

	def set_direc(self,v):
		self.velocity = v;
		self.velocit +=self.speed;



class Map:
	def __init__(self):
		self.shippos = np.array([0,0],float);
		self.sec = [0,0];
		self.limit = [2**63,2**63];
		self.error = None;
		self.celestia  = [];#holds the objects position  in space
		self.tempsec = [self.sec[0]-1,self.sec[1]-1];

	def update(self):
		self.sec = [int(self.shippos[0]/10000),int(self.shippos[1]/10000)];
		if self.tempsec[0]!=self.sec[0] or self.tempsec[1]!=self.sec[1]:
			print True;
			self.celestia = [];
			self.CreatePlanets(self.sec[0]*100+self.sec[1]*10);
			self.tempsec = [self.sec[0],self.sec[1]];



	def CreatePlanets(self,sectorseed):
		random.seed(sectorseed);
		newplanet = Planet();
		randint = random.randint;
		newplanet.pos = np.array([randint(self.sec[0]*10000+600,(self.sec[0]+1)*10000-600),randint(self.sec[1]*10000+600,(self.sec[1]+1)*10000-600)],int);
		print newplanet.pos;
		newplanet.radius=randint(300,600);	newplanet.g = randint(3,12);newplanet.sat = False;
		self.celestia.append(newplanet);
		


class Ship:
	def __init__(self,Map,Screen):
		self.map = Map;
		self.acceleration = np.array([0,0],float);
		self.velocity = np.array([1000,1000],float);
		self.Screen = Screen;
		self.fuel = 500;
		self.rad = 0.0;
		self.velocityper10 = self.velocity*0.10
		
	def rotate(self,deg):
		#X' = X * cos(theta) - Y * sin(theta)
		#Y' = X * sin(theta) + Y *cos(theta)
		self.rad = np.radians(deg);
		
		for i in xrange(len(shipcoords)):
			orshipcoords[i][0] = shipcoords[i][0]*np.cos(self.rad)-shipcoords[i][1]*np.sin(self.rad);
			orshipcoords[i][1] = shipcoords[i][0]*np.sin(self.rad)+shipcoords[i][1]*np.cos(self.rad);
			orshipcoords[i]	   = orshipcoords[i]+self.Screen.orgin;
	
	def line(self,p1,p2):
		py.draw.line(self.Screen.win,white,p1,p2);


	def place(self):
		self.line(orshipcoords[0],orshipcoords[1]);	self.line(orshipcoords[1],orshipcoords[2]);
		self.line(orshipcoords[2],orshipcoords[3]);	self.line(orshipcoords[0],orshipcoords[2]);
		self.line(orshipcoords[0],orshipcoords[3]);	self.line(orshipcoords[1],orshipcoords[3]);
		self.line(orshipcoords[4],orshipcoords[5]);	self.line(orshipcoords[6],orshipcoords[7]);
		self.line(orshipcoords[8],orshipcoords[9]);	self.line(orshipcoords[10],orshipcoords[11]);
		self.line(orshipcoords[12],orshipcoords[13]);

	def accel(self):#acceleration
		currentspeed = np.linalg.norm(self.velocity);
		if self.fuel>0.0000000001:
			direction = np.array([np.sin(self.rad),np.cos(self.rad)],float);
			self.velocity = self.velocity+(direction*0.1);
			self.fuel-=0.01;
		self.velocityper10 = self.velocity*0.10;
		

	def update(self,dt):
		self.map.shippos += self.velocity*dt;
		


	def stop(self,dt):
		if np.linalg.norm(self.velocity)>0:
			self.velocity -=self.velocityper10*dt;
		if np.linalg.norm(self.velocity)<np.linalg.norm(self.velocityper10):
			self.velocity = np.array([0,0],float);
			


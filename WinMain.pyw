
import os
import sys
class dev_null:
	def write(self,s):
		pass

sys.stderr=dev_null()
sys.stdout=dev_null()
os.environ['LANG']='C'
import gtk
import Game
Game.Game()
gtk.main()

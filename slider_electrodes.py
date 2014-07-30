from cStringIO import StringIO
import inkex
import simplestyle

class SliderElectrodes(inkex.Effect):
	def __init__(self):
		inkex.Effect.__init__(self)
		self.OptionParser.add_option("-c", "--count", action="store", type="int", dest="count", default=5, help="Number of electrodes")
		self.OptionParser.add_option("-s", "--spikes", action="store", type="int", dest="spikes", default=5, help="Number of spikes")

	def genPathString(self, bounds, spikeWidth, first=False, last=False):
		s = StringIO()

		cx = bounds[0]
		cy = bounds[1]
		stepx = spikeWidth
		stepy = (bounds[3] - bounds[1]) / (2.0 * self.options.spikes)
		
		s.write(" M %f, %f " % (bounds[0], bounds[1]))
		
		if first:
			s.write(" L %f, %f " % (bounds[0], bounds[3]))
		else:
			for i in range(self.options.spikes):
				s.write(" L %f, %f " % (bounds[0] + stepx, bounds[1] + (2 * i + 1) * stepy))
				s.write(" L %f, %f " % (bounds[0], bounds[1] + (2 * i + 2) * stepy))
		
		if last:
			s.write(" L %f, %f " % (bounds[2], bounds[3]))
			s.write(" L %f, %f " % (bounds[2], bounds[1]))
		else:
			s.write(" L %f, %f " % (bounds[2] - stepx, bounds[3]))
			for i in range(self.options.spikes):
				s.write(" L %f, %f " % (bounds[2], bounds[3] - (2 * i + 1) * stepy))
				s.write(" L %f, %f " % (bounds[2] - stepx, bounds[3] - (2 * i + 2) * stepy))
		s.write(" Z ")
		return s.getvalue()
		
	def effect(self):
		svg = self.document.getroot()
		width = float(self.document.getroot().get('width'))
		height = float(self.document.getroot().get('height'))
		
		group = inkex.etree.SubElement(self.current_layer, 'g', {
			inkex.addNS('label', 'inkscape') : 'Slider electrodes'
		})
		
		style = {
			'stroke'	: 'none',
			'fill'		: '#000000'
		}
		
		eWidth = width / self.options.count
		spikeWidth = 0.6 * eWidth
		
		for eid in range(self.options.count):
			if eid == 0:
				path = self.genPathString((eid * eWidth, 0, (eid + 1) * eWidth + 0.4 * spikeWidth, height), spikeWidth, first=True)
			elif eid == self.options.count - 1:
				path = self.genPathString((eid * eWidth - 0.4 * spikeWidth, 0, (eid + 1) * eWidth, height), spikeWidth, last=True)
			else:
				path = self.genPathString((eid * eWidth - 0.4 * spikeWidth, 0, (eid + 1) * eWidth + 0.4 * spikeWidth, height), spikeWidth)
		
			e = inkex.etree.SubElement(group, inkex.addNS('path', 'svg'), {
				'style' : simplestyle.formatStyle(style),
				'd' : path
			})
			
if __name__ == '__main__':
	effect = SliderElectrodes()
	effect.affect()

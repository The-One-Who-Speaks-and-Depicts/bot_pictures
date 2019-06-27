import re

import numpy as np
from scipy import misc
from collections import namedtuple

from transformer_net import TransformerNet

from PIL import Image
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision.transforms as transforms
import torchvision.models as models
from torch.optim import Adam
from torch.utils.data import DataLoader
from torchvision import datasets



# В данном классе мы хотим полностью производить всю обработку картинок, которые поступают к нам из телеграма.
# Это всего лишь заготовка, поэтому не стесняйтесь менять имена функций, добавлять аргументы, свои классы и
# все такое.
class StyleTransferModel:
	def __init__(self):
		# Сюда необходимо перенести всю иницализацию, вроде загрузки свеерточной сети и т.д.
		self.imsize = 128
		self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
		pass

	def transfer_style(self, content_img_stream):        
		content_image = self._process_image(content_img_stream)
		    
		with torch.no_grad():
			style_model = TransformerNet()
			state_dict = torch.load('rain_princess.pth')            
			for k in list(state_dict.keys()):
				if re.search(r'in\d+\.running_(mean|var)$', k):
					del state_dict[k]
			style_model.load_state_dict(state_dict)
			style_model.to(self.device)
			output = self.style_model(content_image).cpu()
			output = numpy.array(output.squeeze(0))
			output = output.transpose(1, 2, 0).astype("uint8")			 			
			return misc.toimage(output)

    
	def _process_image(self, img_stream):
		loader = transforms.Compose([
			transforms.Resize(self.imsize),  # нормируем размер изображения
			transforms.CenterCrop(self.imsize),
			transforms.ToTensor()])  # превращаем в удобный формат

		image = Image.open(img_stream)
		image = loader(image).unsqueeze(0)
		return image.to(self.device, torch.float)
	
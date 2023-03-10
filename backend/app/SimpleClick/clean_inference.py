import torch
import numpy as np
from PIL import Image

from isegm.inference import utils
from interactive_demo.controller import InteractiveController

def load_controller():
    torch.backends.cudnn.deterministic = True
    checkpoint_path = utils.find_checkpoint('app/SimpleClick/weights/simpleclick_models/', 'cocolvis_vit_base.pth')
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    model = utils.load_is_model(checkpoint_path, device, False, cpu_dist_maps=True)
    controller = InteractiveController(model, device,
                                                predictor_params={'brs_mode': 'NoBRS', 'zoom_in_params': {'skip_clicks':-1, 'target_size': (448, 448)}},
                                                update_image_callback=None)
    def update_image_callback(reset_canvas=True):
      img = controller.get_visualization(0.5, 5)
      Image.fromarray(img).save('/vol/out.png')

    controller.update_image_callback = update_image_callback
    return controller



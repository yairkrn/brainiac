import matplotlib.pyplot as plt
import numpy as np


class DepthImageParser:
    field = 'depth_image'

    def parse(self, context, snapshot):
        width = snapshot.depth_image.w
        height = snapshot.depth_image.h
        values = np.array(snapshot.depth_image.depths).reshape((height, width))
        plt.imshow(values, cmap='hot')
        plt.savefig(context.directory / 'depth_image.png')
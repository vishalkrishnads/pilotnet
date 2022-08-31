# A custom data type that holds the values for a frame (training only).

class PilotData(object):
    def __init__(self, image_file: 'An image file with driving data as filename'):
        self.steering, self.throttle, self.image = self.parse(image_file)

    def parse(self, image_file):
        pass

    def convert(self, image):
        pass
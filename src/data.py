from utils.screen import message
import os, json, cv2

class PilotData(object):
    def __init__(self, path_to: 'Path to the image file', image_file: 'An image file with driving data as filename'):
        self.steering, self.throttle, self.brake, self.image = self.parse(path_to, image_file)

    def __str__(self):
        return f'PilotData(For the given image frame, the telemetry states that steering should be at {self.steering}, brakes should be pressed {self.brake} units & throttle should be held at {self.throttle})'

    def __repr__(self):
        return f"PilotData(steering={self.steering}, throttle={self.throttle}, brake={self.brake} image={self.image})"

    def parse(self, path_to, image_file):
        data = json.loads(image_file[:-4])
        image = cv2.imread(f'{path_to}{image_file}')
        image = cv2.resize(image, (160, 120))
        return (data[1], data[2], data[3], image)

class Data():
    def __init__(self, isTraining: 'whether to prepare data for training or prediction' = True):
        self.data = self.generate_data()

    def generate_data(self):
        data = []
        with os.scandir('recordings/') as recordings:
            for recording in recordings:
                message(f'Extracting from {recording.name}')
                with os.scandir(recording) as images:
                    for image in images:
                        data.append(PilotData(f'recordings/{recording.name}/', image.name))
        return data

    def training_data(self):
        return self.data[:int((len(self.data)*3)/4)]
    
    def testing_data(self):
        return self.data[int((len(self.data)*3)/4)+1:]
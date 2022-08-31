# The data collector. It connects to the carla server and records driving data

from utils.screen import clear
import numpy as np
import carla, datetime, pygame

try:
    display = pygame.display.set_mode((1900, 1000))
except:
    print("Failed to spawn live feed from vehicle. If you're on WSL, this happens as the OS doesn't have a display device yet. Otherwise, check your pygame installation.")
    pass

class Collector:
    def __init__(self, world, time):
        self.start_time = datetime.datetime.now()
        self.world = world
        self.vehicle = None
        try:
            pygame.init()
        except:
            pass
        self.start(time)
    
    def record(self, image):
        control = self.vehicle.get_control()
        image.save_to_disk(f'out/{[int((datetime.datetime.now() - self.start_time).total_seconds()), control.steer, control.throttle, control.brake]}.png')
        
        # we now convert image into a raw image to show in our display
        image.convert(carla.ColorConverter.Raw)
        
        # convert the image into an array using standard procedure
        array = np.frombuffer(image.raw_data, dtype=np.dtype("uint8"))
        array = np.reshape(array, (image.height, image.width, 4))
        array = array[:, :, :3]
        array = array[:, :, ::-1]
        
        # show the frame in display & update it
        try:
            surf = pygame.surfarray.make_surface(np.rot90(array, 1))
            display.blit(surf, (0, 0))
            pygame.display.update()
        except:
            pass

    def start(self, time):

        # get a list of spawn points & vehicles then randomly choose from one to use
        vehicle_blueprints = self.world.get_blueprint_library().filter('*vehicle*')
        spawn_points = self.world.get_map().get_spawn_points()
        self.vehicle = self.world.spawn_actor(np.random.choice(vehicle_blueprints), np.random.choice(spawn_points))

        # make a camera and configure it
        camera_init_trans = carla.Transform(carla.Location(x=0.8, z=1.7))
        camera_blueprint = self.world.get_blueprint_library().find('sensor.camera.rgb')
        camera_blueprint.set_attribute('image_size_x', '1920')
        camera_blueprint.set_attribute('image_size_y', '1080')
        camera_blueprint.set_attribute('fov', '110') # sets field of view (FOV)

        # attach camera to vehicle and start recording
        self.camera = self.world.spawn_actor(camera_blueprint, camera_init_trans, attach_to=self.vehicle)
        self.camera.listen(lambda image: self.record(image))

        # autopilot obviously
        self.vehicle.set_autopilot(True)

        try:
            elapsed = 0
            # in Carla, we have to call tick() or wait_for_tick() after altering anything in order to reflect change
            while elapsed <= time*60:
                self.world.tick()
                if elapsed != int((datetime.datetime.now() - self.start_time).total_seconds()):
                    elapsed = int((datetime.datetime.now() - self.start_time).total_seconds())
                    clear()
                    print(f'Time elapsed: {int(((datetime.datetime.now() - self.start_time).total_seconds())/60.0)}m {int((datetime.datetime.now() - self.start_time).total_seconds())}s')
            self.stop()
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        try:
            self.camera.stop() # destroy sensor in main smiulation (server)
            self.vehicle.destroy()
        except:
            pass
        print("Vehicle destroyed")
        try:
            pygame.quit()
        except:
            pass
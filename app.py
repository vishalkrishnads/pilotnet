from utils.screen import clear, warn, message, error
from utils.collect import Collector
from utils.piloterror import PilotError
import carla, random, time

class Menu():

    def run_1():
        'Train using generated data'
        print("Doing 1")

    def run_2():
        'Generate new data'
        message('Connecting to CARLA world')
        client = carla.Client('localhost', 2000)
        try:
            world = client.get_world()
            message('Connected to CARLA server')
        except:
            try:
                warn('There seems to be a problem with your CARLA server. Retrying with WSL address...')
                client = carla.Client('172.27.144.1', 2000) # the host IP can be found with $(hostname).local from WSL
                world = client.get_world()
                message('Connected to CARLA server')
            except:
                raise PilotError('Connection to CARLA simulator failed. Check your CARLA installation, confirm simulator is running on port 2000.\nIf in WSL, refer to the troubleshooting guide for tips.')
        time = int(input('Enter the time you need the generator to run for (in minutes) >> '))
        clear()
        collector = Collector(world, time)

    def run_3():
        'Predict on a single video frame'
        print("Doing 3")

    def run_4():
        'Predict on live video feed'
        raise PilotError("Um sorry bruh. Live video prediction isn't available yet. I'm working on it keep an eye here.")

    def run_5():
        'Wrap up. I wanna quit.'
        message('Hope you enjoyed PilotNet. Report any issues on GitHub..')

    @staticmethod
    def execute(user_input):
        task_name = f'run_{user_input}'
        try:
            menu = getattr(Menu, task_name)
            clear()
        except AttributeError:
            shitquotes = [
                'Uh huh, where are your eyes at? Open sesame...',
                "Now what's up with that?",
                'Um sorry not on this menu...',
                "Sorry I couldn't read your mind. Come again?",
                "Good choice, congrats. Now try again."]
            raise PilotError(random.choice(shitquotes))
        else:
            menu()
    
    @staticmethod
    def generate_instructions():
        do_methods = [m for m in dir(Menu) if m.startswith('run_')]
        menu_string = "\n".join(
            [f'{method[-1]}.  {getattr(Menu, method).__doc__}' for method in do_methods])
        print(menu_string)
    
    @staticmethod
    def run():
        user_input = 0
        while(user_input != 5):
            clear()
            Menu.generate_instructions()
            user_input = int(input("Enter your choice >> "))
            try:
                Menu.execute(user_input)
            except PilotError:
                y = 'n'
                while y != 'y':
                    y = input("OK read the error, return to main menu (y) >> ")

def main():
    Menu.run()

if __name__ == '__main__':
    main()
# pilotnet
A TensorFlow implementation of the paper [Explaining How a Deep Neural Network Trained with
End-to-End Learning Steers a Car](https://arxiv.org/pdf/1704.07911.pdf) by NVIDIA, Google Research & New York University.

## Installation
Follow the steps to install and try this locally in your system

### Prerequisites
1. [Anaconda/Miniconda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html)
2. [CARLA simulator](http://carla.org)

### Steps
1. Clone the repository
    ```
    https://github.com/vishalkrishnads/pilotnet.git
    ```
2. Change working directory
    ```
    cd pilotnet
    ```
3. Create a conda environment specificially with Python 3.8 and activate it
    ```
    conda create -n "pilotnet" python=3.8.0
    conda activate pilotnet
    ```
4. Install tensorflow into the environment by following the [instructions](https://www.tensorflow.org/install/) in the official documentation. If you're not using a [CUDA capable GPU](https://developer.nvidia.com/cuda-gpus) or don't have a GPU, skip to the next step.
5. Install other required modules
    ```
    pip install -r requirements.txt
    ```
6. Run the app
    ```
    python app.py
    ```

## Usage

* Run the `app.py` file. It is the entry point. You will be presented with a menu
    ```
    $ python app.py
    # a banner
    1.  Train using generated data
    2.  Generate new data
    3.  Predict on a single video frame
    4.  Predict on live video feed
    5.  Wrap up. I wanna quit.
    Enter your choice >> 
    ```
* Enter your choice and follow the prompts. This is an infinitely looping menu. Choose 5 to leave.

## Issues
1. Training
    * If your machine is not that compute intensive, this model can't be forced to take in high quality images, say like 1920x1080. If you try to do this, it will raise an exception that the resources have finished and quit. Try scaling the quality up slowly from the default values and see where it sticks for your system.
    * Sometimes, you might get too excited and try to train 100 epochs on 2 minutes of recordings. This will obviously end with an error saying that the generator can't produce enough data for all these epochs. Either record more data or reduce epochs.

2. Data Generator
    * In WSL, the data generator has a fallback system for WSL connections. But just in case yours is failing, try using the `ping $(hostname).local` command to find the host IP address. Now, open `app.py` and change the IP from `127.27.144.1` to your IP address in `Collector.run2()`. Restart.
        ```python
        # ...
        warn('There seems to be a problem with your CARLA server. Retrying with WSL address...')

        # change here
        # client = carla.Client('172.27.144.1', 2000)
        client = carla.Client('<your IP>', 2000)
        
        world = client.get_world()
        # ...
        ```
    * There have been many reports online of not being able to connect to CARLA server but most of these relate to blocked ports or network issues. Check your computer by following code. If this crashes, then try fixing this first and then the generator should work
        ```python
        import carla

        client = carla.Client('localhost', 2000)
        world = client.get_world()
        ```
    * If your disk doesn't have enough empty space, then it's obvious why the generator crashses. It stores recordings in the `recordings/` directory. Try clearing space.

3. Predicting on frame
    * The only possible issue here would be to enter paths of stuff that doesn't exist. Maybe a test image or saved model. The script will crash if you enter something wrong. Try double checking the paths.

## Directory structure
```
pilotnet
    |
    |-pilotnet
    |   |
    |   |- data.py (a custom datatype for training)
    |   |- model.py (the actual model cum helpers)
    |
    |-utils
    |   |
    |   |-collect.py (data collector)
    |   |-screen.py (screen utilities)
    |
    |-app.py (entry point for running app)
    |-requirements.txt (python requirements file)
    |-README.md (this documentation)
```

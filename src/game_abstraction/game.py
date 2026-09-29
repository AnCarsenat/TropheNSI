class Game:
    def __init__(self,flags:list[str]):
        self.delta_time = 0.0
        self.current_scene = None

        # load flags

        self.debugging = False
        if "debugging" in flags:
            self.debugging = True
        
    
    def tick(self, delta_time:float)->None:
        self.delta_time = delta_time

        ...

        if self.current_scene is not None:
            self.current_scene.tick()
        # ALL LOGIC GOES HERE
        # LOGIC PROPAGATES :
        # Game.currentScene.tick()
        # => node1.tick()
        #      => node1_child.tick()
        # => node2.tick()
        # NODES THAT ARE ADDED FIRST RUN FIRST.
        # NODES THAT ARE ADDED LAST RUN LAST.
        # We should prolly implement multi-threading so it runs well
        # And define another way to load ressources etc.



    def load(self)->None:
        if self.current_scene is not None:
            self.current_scene.load()
        ...
        # ALL LOADS GO HERE
        # LOADS PROPAGATE
        
        # WHEN EVERYTHING IS LOADED SET 

    def draw(self):
        if self.current_scene is not None:
            self.current_scene.load()
        ...
        # ALL DRAWING TO SCREEN / VISUAL GOES HERE

    # USE THREADS

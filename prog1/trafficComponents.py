class Vehicle:
    def __init__(self,destination,borntime):
        self.destination = destination
        self.borntime = borntime
    def __str__(self):
        return f"Vehicle({self.destination}, {self.borntime})"

class Light:
    def __init__(self,period,green_period):
        self._period = period  
        self._green_period = green_period 
        self._internal_time = 0
        
    def __str__(self):
        if self.is_green():
            return "(G)"
        else:
            return "(R)"
    
    def step(self):
        self._internal_time = (self._internal_time + 1) % (self._period)
    
    def is_green(self):
        if self._internal_time < self._green_period:
            return True
        else:
            return False
        
class Lane:
    def __init__(self,length):
        self._lane = [None for _ in range(length)]  # Bygger lista med None-objekt (=avsaknad av fordon)
    
    def get_first(self):
        return self._lane[0]
    
    def remove_first(self):
        v = self._lane[0]
        self._lane[0] = None
        return v
    
    def step(self):
        for i, v in enumerate(self._lane):
            if i == 0:
                continue                    # Hoppar över första platsen
            
            if v and not self._lane[i-1]:   # Kollar om det finns ett fordon och om föregående plats är tom
                self._lane[i-1] = v
                self._lane[i] = None
        
    def is_last_free(self):
        if not self._lane[-1]:      # Returnerar True om None-typ (= inget fordon) 
            return True
        else:
            return False
        
    def enter(self,v):
        self._lane[-1] = v
    
    def number_in_lane(self):
        return len(self._lane) - self._lane.count(None)

    def __str__(self):             # Skriver ut i format "[.S.WS..]"
        return "[" + "".join([ v.destination if v else "." for v in self._lane]) + "]"  # Returnerar destination av fordon
                                                                                        #  eller "." vid avsaknad av ett











# ----------------------------------

    
def demo_lane():
    """For demonstration of the class Lane"""
    a_lane = Lane(10)
    print(a_lane)
    v = Vehicle('N', 34)
    a_lane.enter(v)
    print(a_lane)

    a_lane.step()
    print(a_lane)
    for i in range(20):
        if i % 2 == 0:
            u = Vehicle('S', i)
            a_lane.enter(u)
        a_lane.step()
        print(a_lane)
        if i % 3 == 0:
            print('  out: ',
                  a_lane.remove_first())
    print('Number in lane:',
          a_lane.number_in_lane())

def demo_light():
    """Demonstrats the Light class"""
    a_light = Light(7, 3)
    for i in range(15):
        print(i, a_light,
              a_light.is_green())
        a_light.step()


def main():
    """Demonstrates the classes"""
    print('\nLight demonstration\n')
    demo_light()
    print('\nLane demonstration')
    demo_lane()


if __name__ == '__main__':
    main()

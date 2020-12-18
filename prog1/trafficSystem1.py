from statistics import mean, median
from time import sleep
import destinations
import trafficComponents as tc


class TrafficSystem:
    def __init__(self):
        self.time = 0
        self.lane1 = tc.Lane(5)
        self.lane2 = tc.Lane(5)
        self.light = tc.Light(10,8)
        self.destinations = destinations.Destinations()
        self.tailback = []

    def snapshot(self):
        """Print a snap shot of the current state of the system."""
        
        print(self.lane1, 
              self.light, 
              self.lane2, 
              [x.destination for x in self.tailback])
        
        
    def step(self):
        """Take one time step for all components."""
        
        self.lane1.remove_first()                                    #   i. Ta ut första fordonet från den första (vänstra) filen i figuren. 
        self.lane1.step()                                            #  ii. Stega den första filen med dess step-metod. 
        if self.light.is_green() and self.lane1.is_last_free():      # iii. Om signalen är grön så flytta första fordonet på den andra (högra) filen till den första. 
            self.lane1.enter( self.lane2.remove_first() ) 
        self.light.step()                                            #  iv. Stega signalen med dess step-metod. 
        self.lane2.step()                                            #   v. Stega den andra filen. 
        
        dest = self.destinations.step()                              #  vi. Anropa step-metoden i Destinations-objektet. 
        if dest:                                                     #      Om denna returnerar en destination (d.v.s. något annat än None) . 
            self.tailback.append(tc.Vehicle(dest, self.time))        #         så skapa ett fordon
        if self.lane2.is_last_free() and len(self.tailback) > 0:     #            och lägg det sist på den andra filen
            self.lane2.enter( self.tailback.pop(0) )
        
        
        self.time += 1

    def in_system(self):
        """Return the number of vehicles in the system."""
        pass

    def print_statistics(self):
        """Print statistics about the run."""
        pass











# -------------------------------------------

def main():
    ts = TrafficSystem()
    for i in range(100):
        ts.snapshot()
        ts.step()
        #sleep(0.1)
    print('\nFinal state:')
    ts.snapshot()
    print()
    ts.print_statistics()


if __name__ == '__main__':
    main()

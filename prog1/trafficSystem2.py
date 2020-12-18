from statistics import mean, median
from time import sleep
import destinations
import trafficComponents as tc


class TrafficSystem:
    def __init__(self, lane_length, lanews_length, light_period, west_green, south_green):
        self.time = 0

        self.lane = tc.Lane(lane_length)
        self.lane_west = tc.Lane(lanews_length)
        self.lane_south = tc.Lane(lanews_length)
        self.light_west = tc.Light(light_period,west_green)
        self.light_south = tc.Light(light_period,south_green)

        self.counter = {"blocked": 0, "queue": 0, "W": [], "S": [], "created_vehicles": 0}

        self.block_status = " "     # För utskrift. Markeras med '*' vid blockering, mellanslag då fil är tillgänglig
        self.queue = []             # Kö vid punkt E

        self.destinations = destinations.Destinations()

       

    def snapshot(self):
        print("\n\t",self.light_west,
              self.lane_west,
              self.block_status,
              self.lane, 
              [x.destination for x in self.queue],"\n\t",
              self.light_south,
              self.lane_south)

    def get_lane(self, vehicle):            # Returnerar fordonets eftersökta fil
        lane_direction = {"W": self.lane_west, "S": self.lane_south}
        return lane_direction[ vehicle.destination ]

    def exit_counter(self, vehicle):
        t = self.time - vehicle.borntime    # Beräknar fordonets tid i systemet
        d = vehicle.destination
        self.counter[d].append(t)

        
    def step(self):
        lane = self.lane
        queue = self.queue
        counter = self.counter

        for ws_lane in ((self.lane_west, self.light_west), (self.lane_south,self.light_south)): # Kör igenom med tupler av fil och tillhörande trafiksignal
            if ws_lane[1].is_green() and ws_lane[0].get_first() != None:    # Kollar efter grönljus och väntande fordon
                self.exit_counter( ws_lane[0].get_first() )                 # För statistik över lämnande fordon
                ws_lane[0].remove_first()
                
            ws_lane[0].step() # Stegar fil
            ws_lane[1].step() # Stegar trafiksignal

        if lane.get_first():                                                        # Kollar om fordon väntar på filbyte
            if self.get_lane(lane.get_first()).is_last_free():                      # Kollar om rätt trafiksignalfil är tillgänglig
                self.get_lane(lane.get_first()).enter( lane.remove_first() )        #     flyttar till fil

                self.block_status = " "     # 
            else:                           #  Uppdaterar blockeringsstatus och räknare
                counter["blocked"] += 1     #
                self.block_status = "*"     #

        lane.step()    
        
        dest = self.destinations.step()                     # Skapar nya fordon enligt destinations        
        if dest:                                                      
            queue.append(tc.Vehicle(dest, self.time))
            counter["created_vehicles"] += 1

        if len(queue) > 0 and lane.is_last_free():          # Flyttar om plats i fil finns flr väntande fordon
            lane.enter( queue.pop(0) )

        if len(queue) > 0:
            counter["queue"] += 1

        self.time += 1

    def in_system(self):
        return self.lane_west.number_in_lane() + self.lane_south.number_in_lane() + self.lane.number_in_lane()

    def print_statistics(self):

        time = self.time
        block_count = self.counter["blocked"]
        queue_count = self.counter["queue"]
        total_count = self.counter["created_vehicles"]
        w = sorted(self.counter["W"])
        s = sorted(self.counter["S"])
        
        print(f'''

Statistics after {time} timesteps:

Created vehicles: \t{total_count}
In system       : \t{self.in_system()}

At exit         West           South
Vehicles out:    {len(w)}             {len(s)}
Minimal time:    {w[0]}             {s[0]}
Maximal time:    {w[-1]}             {s[-1]}
Mean time   :    {round(mean(w),1)}           {round(mean(s),1)}
Median time :    {median(w)}             {median(s)}

Blocked     : {round(block_count / time * 100,1)}%
Queue       : {round(queue_count / time * 100,1)}%
''')













# ------------------------------------

def main():
    ts = TrafficSystem(lane_length, lanews_length, light_period, west_green, south_green)
    for i in range(100):
        ts.snapshot()
        ts.step()
        #sleep(0.1)
    print('\nFinal state:')
    ts.snapshot()
    print()
    ts.print_statistics()


if __name__ == '__main__':
    
    lane_length  =  11       # Length first (rightmost) lane
    lanews_length = 8        # Length lanes in front of signals
    light_period =  14       # Period for the lights
    west_green   =  6        # Green period westbound light
    south_green  =  4        # Green period southbound light
    
    main()




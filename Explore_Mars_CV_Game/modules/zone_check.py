class Zone:
    def __init__(self, x, y, x2, y2, zone_type):
        self.x = x  # Top-left x
        self.y = y  # Top-left y
        self.x2 = x2  # Bottom-right x
        self.y2 = y2  # Bottom-right y
        self.zone_type = zone_type
        self.analyzed = False

    def analyze(self):
        if not self.analyzed:
            self.analyzed = True
            return True
        return False

    def is_rover_inside(self, rover_x, rover_y):
        """Check if the rover's position is inside the zone's bounding box."""
        return (self.x <= rover_x <= self.x2) and (self.y <= rover_y <= self.y2)
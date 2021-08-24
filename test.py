
#{"msg": "updateData", "speed": 3, "pace": 488.63240295941256, "distance": 33.8, "calhr": 310.3248}

def calc_speed(speed):
    speed = float(speed / 2)
    speed = speed / 10
    if speed < 0:
        speed = 0
    if speed > 3.8:
        speed = 3.8
    return speed

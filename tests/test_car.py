from src.car import Car


def test_acceleration():
    car = Car(0, 0)
    car.update(1, 0)
    assert car.velocity > 0


def test_friction():
    car = Car(0, 0)
    car.velocity = 5
    car.update(0, 0)
    assert car.velocity < 5


def test_turning():
    car = Car(0, 0)
    car.velocity = 5
    initial_angle = car.angle
    car.update(0, 1)
    assert car.angle != initial_angle

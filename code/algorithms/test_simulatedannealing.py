from .simulatedannealing import Simulatedannealing, District

def test_temperature_change():
    """ Here we test that the linear temperature change
        works the way we want it to
    """

    district = District(1, "costs-own")
    simul = Simulatedannealing(district, 100, 10)
    
    assert simul.temp == 10

    begin_temp = simul.temp_0
    simul.iterations = 1

    simul.linear_temperature_change()

    assert simul.temp == 9.9
    
    simul.iterations = 2
    simul.linear_temperature_change()

    assert simul.temp == 9.8

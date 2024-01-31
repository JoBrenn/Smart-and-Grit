from code.modules.battery import Battery
from code.modules.house import House

def test_add_delete_house():
    """ Here we test that a house
        is added  and deleted correctly
    """

    battery = Battery(1, (2,2), 3, 1000)
    house = House(1, (1,1), 1)
    battery.add_house(house)
    assert house in battery.houses
    assert battery.left_over_capacity == 2
    
    battery.delete_house(house)
    assert house not in battery.houses
    assert battery.left_over_capacity == 3
    assert battery.return_capacity() == 3




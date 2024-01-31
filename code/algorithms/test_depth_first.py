from .depth_first import DepthFirst, District

def test_valid_capacity():
    """ Here we test that the valid capacity
        check works as wished
    """

    district = District(2, "costs-own")
    df = DepthFirst(district)

    battery = district.batteries[0]
    battery_cap = battery.capacity

    assert df.valid_capacity(district) is True

    # Assign all houses to same battery
    for house in district.houses:
        battery.add_house(house)

    assert df.valid_capacity(district) is False

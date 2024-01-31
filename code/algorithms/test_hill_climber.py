from .hill_climber import HillClimber, Battery, District

def test_return_costs():
    """ Here we test that within the HillClimber class
        the penalties and costs are determined and 
        returned right and check validness right
    """

    district = District(1, "costs-own")
    hc = HillClimber(district)
    battery = district.batteries[0]
    battery_cap = battery.capacity

    assert hc.check_valid(district) is True

    total_output = 0

    # Keep track of total output and assign
    # all houses to same battery
    for house in district.houses:
        total_output += house.output
        battery.add_house(house)
    
    capacity_exceedance = battery.left_over_capacity

    assert hc.return_penalty(battery) == abs(capacity_exceedance) * 10
    assert hc.return_total_cost(district) == district.return_cost() + \
                                             hc.return_penalty(battery)
    assert hc.check_valid(district) is False

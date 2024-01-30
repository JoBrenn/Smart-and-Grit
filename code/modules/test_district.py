from code.modules.district import District

def test_return_output():
    district = District(1, "costs-own")
    assert district

def test_return_cost():
    district = District(2, "costs-own")
    assert district.return_cost() == 25000
    
    house_0 = district.houses[0]
    battery_0 = district.batteries[0]
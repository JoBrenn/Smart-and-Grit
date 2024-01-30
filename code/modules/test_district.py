from district import District

def test_return_output():
    district = District(1, "costs-own")
    assert district

def test_return_cost():
    district = District(2, "costs-own")
    assert district.return_cost() == 25000
    
    house_0 = district.houses[0]
    house_0.house_dict["cables"] = [(1,1), (1,2)]
    battery_0 = district.batteries[0]
    battery_0.add_house(house_0)
    assert district.return_cost() == 25009
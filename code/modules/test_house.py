from code.modules.house import House

def test_add_cable_segment():
    """ Here we test that a cable coordinate
        is added  and deleted correctly and the 
        right length is returned
    """

    house = House(1, (1,1), 1)
    house.add_cable_segment((1,2))
    assert house.str_cables == ["1,2"]
    assert house.cables == [(1,2)]
    house.add_cable_segment((1,3))
    assert house.return_cable_length() == 1
    house.delete_cables()
    assert len(house.str_cables) == 0
    assert len(house.cables) == 0
    assert house.return_cable_length() == -1
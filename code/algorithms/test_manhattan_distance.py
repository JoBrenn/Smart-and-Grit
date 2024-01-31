from .manhattan_distance import get_cable_points, \
    return_manhattan_distance, create_cable, House


def test_get_cable_points():
    """ Here we test that the right in between 
        point is returned
    """

    assert get_cable_points((1,1), (2,2)) == ((1,1), (1,2), (2,2))
    assert get_cable_points((2,2), (2,2)) == ((2,2), (2,2), (2,2))


def test_return_manhattan():
    """ Here we test that the right Manhattan distance
        is returned 
    """

    house = House(3, (4,4), 50)
    assert return_manhattan_distance(house, (5,5)) == 2
    assert return_manhattan_distance(house, (4,9)) == 5
    assert return_manhattan_distance(house, (9,4)) == 5


def test_create_cable():
    """ Here we test that a cable is rightly created
        along the Manhattan distance
    """

    house = House(3, (1,1), 50)
    create_cable(house, (3,3))
    assert house.cables == [(1,1), (1,2), (1,3), (2,3), (3,3)]

    house_2 = House(3, (4,5), 50)
    create_cable(house_2, (2,2))
    assert house_2.str_cables == ["4,5", "4,4", "4,3", "4,2",
                                  "3,2", "2,2"]

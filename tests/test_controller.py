from curby.gather.service import billboardservice

def test_controller():
    assert(len(billboardservice.get_popular(1)) == 1)
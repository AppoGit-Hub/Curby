from curby.gather.controller import billboardcontroller

def test_controller():
    assert(len(billboardcontroller.get_popular(1)) == 1)
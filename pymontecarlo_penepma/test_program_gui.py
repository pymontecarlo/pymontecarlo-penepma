# """"""

# # Standard library modules.

# # Third party modules.
# import pytest

# # Local modules.
# from pymontecarlo_penepma.program_gui import NumberTrajectoriesTerminationField

# # Globals and constants variables.

# @pytest.fixture
# def numbertrajectoriesfield():
#     return NumberTrajectoriesTerminationField()

# def test_numbertrajectoriesfield_default(qtbot, numbertrajectoriesfield):
#     trajectories = numbertrajectoriesfield.numbersTrajectories()
#     assert len(trajectories) == 1
#     assert trajectories[0] == pytest.approx(1e38, abs=1e-4)

# def test_numbertrajectoriesfield_nolimit_false(qtbot, numbertrajectoriesfield):
#     numbertrajectoriesfield.suffixWidget().click()
#     assert not numbertrajectoriesfield.widget().hasAcceptableInput()

#     # Enter trajectories
#     qtbot.keyClicks(numbertrajectoriesfield.widget().lineedit, "999")
#     trajectories = numbertrajectoriesfield.numbersTrajectories()
#     assert len(trajectories) == 1
#     assert trajectories[0] == pytest.approx(999, abs=1e-4)

#     # Clear again
#     numbertrajectoriesfield.suffixWidget().click()
#     trajectories = numbertrajectoriesfield.numbersTrajectories()
#     assert len(trajectories) == 1
#     assert trajectories[0] == pytest.approx(1e38, abs=1e-4)
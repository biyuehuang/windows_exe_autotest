from importlib import import_module

def main():
    fails = 0
    execution_results = []
    module = import_module('color_saturation')
    test_test_ = getattr(module,'ColorSaturation')
    test = test_test_()

    test.prepare_assumptions()
    test.set_up()
    test.execute()
    test.tear_down()
    test.process_results()

    execution_results.append(test.assumptions)
    assumptions_results = [assumption.result for assumption in test.assumptions]
    test_passed = all(assumptions_results)

    if not test_passed:
        fails = assumptions_results.count(False)
        print("Tests Failed!")
    else:
        print("Tests Passed!")

    print('****TESTS RESULTS****\nTotal:{} | Passed:{} | Failed:{} | \n'
               .format(len(assumptions_results), len(assumptions_results) - fails, fails))


if __name__ == "__main__":
    main()


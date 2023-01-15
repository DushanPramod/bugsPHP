import argument_parser
import myProject
import myTest

param_dict = argument_parser.arg_parser()
if(param_dict["task"] == "checkout"):
    myProject.checkout(param_dict)
elif(param_dict["task"] == "install"):
    myTest.install(param_dict)
elif(param_dict["task"] == "test" and param_dict["test-case"] != None):
    myTest.run_single_test_case(param_dict)
elif(param_dict["task"] == "test"):
    myTest.run_all_test(param_dict)
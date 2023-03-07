import myProject
import os
import subprocess as sp
import sys
import pydash as _


def install(param_dict):
    print('Installing packages ...')
    SCRIPTDIR = os.path.abspath(os.path.dirname(sys.argv[0]))
    bug_info = myProject.get_bug_info(param_dict)

    if not os.path.isdir(os.path.join(param_dict['output'], bug_info['repo_name'])):
        print("can't find the project folder")
        exit()
    
    proj_path = os.path.join(param_dict['output'], bug_info['repo_name'])

    sp.call(['php', '-r', 'copy("https://getcomposer.org/installer", "composer-setup.php");'], shell=False, cwd=proj_path)
    sp.call(['php', '-r', "if (hash_file('sha384', 'composer-setup.php') === '55ce33d7678c5a611085589f1f3ddf8b3c52d662cd01d4ba75c0ee0459970c2200a51f492d557530c71c15d8dba01eae') { echo 'Installer verified'; } else { echo 'Installer corrupt'; unlink('composer-setup.php'); } echo PHP_EOL;"], shell=False, cwd=proj_path)
    sp.call(["php", "composer-setup.php"], shell=False, cwd=proj_path)
    sp.call(['php', '-r', 'unlink("composer-setup.php");'], shell=False, cwd=proj_path)
    sp.call(['php', "composer.phar", 'config', '--no-plugins', 'allow-plugins', 'true'], shell=False, cwd=proj_path)
    sp.call(["php", "composer.phar", "self-update", "2.5.1"], shell=False, cwd=proj_path)
    sp.call(["php", "composer.phar", "install", "--no-interaction", "--no-progress", "--quiet", "--ignore-platform-reqs"], shell=False, cwd=proj_path)



def formatted_test_case_ref(test_case):
    ref = test_case['@className'] + '::' + test_case['@methodName'] 
    ref = ref.split('\\')[-1]
    if('with data set' in ref):
        splitted = ref.split('with data set')
        if('#' in splitted[1]):
            ref = splitted[0].strip() + '.*'+splitted[1].strip()+'$'
        else:
            ref = splitted[0].strip() + '.*' + splitted[1].strip()
    return ref


def get_chunked_test_cases_cmd_list(test_cases):
    max_cmd_string_length = 30000
    concatenated_test_cases_list = []
    temp = []
    for test_case in test_cases:
        if(len(_.join(temp + [formatted_test_case_ref(test_case)], '\|')) > max_cmd_string_length):
            concatenated_test_cases_list.append(_.join(temp, '\|'))
            temp = []
        else:
            temp.append(formatted_test_case_ref(test_case))
    concatenated_test_cases_list.append(_.join(temp, '\|'))
    return concatenated_test_cases_list



def run_all_test(param_dict):
    SCRIPTDIR = os.path.abspath(os.path.dirname(sys.argv[0]))
    bug_info = myProject.get_bug_info(param_dict)

    if(not os.path.isdir(os.path.join(param_dict['output'], bug_info['repo_name']))):
        print("can't find the project folder")
        exit()
    
    for test_case_chunck in get_chunked_test_cases_cmd_list(bug_info['test_results']['fixed']):
        test_script_cmd = ''
        if(bug_info['repo_full_name'] == 'magento/magento2'):
            test_script_cmd = 'vendor/bin/' + bug_info['test_framework'] + ' ' + bug_info['test_folder'] + ' --filter ' + test_case_chunck
        else:
            test_script_cmd = 'vendor/bin/' + bug_info['test_framework'] + ' --filter ' + test_case_chunck
    
        try:
            # print(test_script_cmd)
            sp.call(test_script_cmd, shell=True, cwd=os.path.join(param_dict['output'], bug_info['repo_name']))
        except Exception as e:
            print(e)


def run_single_test_case(param_dict):
    SCRIPTDIR = os.path.abspath(os.path.dirname(sys.argv[0]))
    bug_info = myProject.get_bug_info(param_dict)

    if(not os.path.isdir(os.path.join(param_dict['output'], bug_info['repo_name']))):
        print("can't find the project folder")
        exit()
    
    test_case_no = param_dict['test-case']
    if(test_case_no <= 0 or test_case_no > len(bug_info['test_results']['fixed'])):
        print("can't find the test case")
        exit()
    
    test_script_cmd = ''
    if(bug_info['repo_full_name'] == 'magento/magento2'):
        test_script_cmd = 'vendor/bin/' + bug_info['test_framework'] + ' ' + bug_info['test_folder'] + ' --filter ' + formatted_test_case_ref(bug_info['test_results']['fixed'][test_case_no-1])
    else:
        test_script_cmd = 'vendor/bin/' + bug_info['test_framework'] + ' --filter ' + formatted_test_case_ref(bug_info['test_results']['fixed'][test_case_no-1])
    
    try:
        # print(test_script_cmd)
        sp.call(test_script_cmd, shell=True, cwd=os.path.join(param_dict['output'], bug_info['repo_name']))
    except Exception as e:
        print(e)
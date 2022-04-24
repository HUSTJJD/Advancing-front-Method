import os
import time
path = './in-100-out-50-front'
filenames = []
for  a, b,files in os.walk('../dat/'):
    for filename in files:
        if os.path.splitext(filename)[1] == '.dat':
            filenames.append(os.path.splitext(filename)[0])
print(filenames)
os.chdir(path)
# for filename in filenames[1:]:
#     os.mkdir(filename)

##############################################################################
######################## write script ########################################
##############################################################################

# with open('./2032c/2032c.glf') as template_file: 
#     template_lines = template_file.readlines()
#     print(template_lines)
#     for filename in filenames[1:]:
#         new_lines = template_lines
#         glf_path =  './' + filename + '/' + filename + '.glf'
#         new_lines[17] = '  $_TMP(mode_1) initialize -strict -type Automatic C:/Users/JJD/Desktop/project_data/dat/' + filename +'.dat\n'
#         new_lines[410] = '  $_TMP(mode_1) initialize -strict -type CAE C:/Users/JJD/Desktop/project_data/cas/in-100-out-50-front/'+ filename +'/'+ filename +'.cas\n'
#         new_lines[415] = 'pw::Application save C:/Users/JJD/Desktop/project_data/cas/in-100-out-50-front/'+ filename +'/'+ filename + '.pw\n'
#         with open(glf_path,'w+') as f:
#             f.writelines(new_lines)
#             f.close()
#     template_file.close()

##############################################################################
########################## make run script batch #############################
##############################################################################
lines = []
for filename in filenames:
    lines.append('%CD%' +'\\' + 'in-100-out-50-front' + '\\'+ filename  + '\\' + filename + '.glf\n')
with open('../run_script.bat','w+') as f:
    f.writelines(lines)
    f.close()

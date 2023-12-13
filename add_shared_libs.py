import sys
import os

global  AdminConfig


def read_custom_libs(root_folder):
    # Add custom URLs
    conf_file = open('/tmp/custom-shared-libs.csv', 'r')
    library_list = []
    i = 0
    for line in conf_file.readlines():
        if i == 0:
            i = i + 1  # skip header
        else:
            shared_config = line.split(",")
            library_name = shared_config[0]
            library_list.append(root_folder + library_name.rstrip())

    return ';'.join(library_list)

# Main

print ("Setting shared libs...")

cell_id = AdminConfig.getid('/Cell:DefaultCell01')
root_folder = '/work/wasconf/shlibs/esposizioneContratti/'

#jar_file_list = '/work/wasconf/shlibs/esposizioneContratti/axiom-api-1.2.20.jar;/work/wasconf/shlibs/esposizioneContratti/axis2-transport-http-1.7.8.jar;/work/wasconf/shlibs/esposizioneContratti/httpclient-4.5.6.jar;/work/wasconf/shlibs/esposizioneContratti/axiom-impl-1.2.20.jar;/work/wasconf/shlibs/esposizioneContratti/axis2-transport-local-1.7.8.jar;/work/wasconf/shlibs/esposizioneContratti/httpcore-4.4.10.jar;/work/wasconf/shlibs/esposizioneContratti/axis2-adb-1.7.8.jar;/work/wasconf/shlibs/esposizioneContratti/commons-codec-1.4.jar;/work/wasconf/shlibs/esposizioneContratti/neethi-3.0.3.jar;/work/wasconf/shlibs/esposizioneContratti/axis2-kernel-1.7.8.jar;/work/wasconf/shlibs/esposizioneContratti/commons-httpclient-3.1.jar;/work/wasconf/shlibs/esposizioneContratti/woden-core-1.0M10.jar'
jar_file_list = read_custom_libs(root_folder)

AdminConfig.create('Library', cell_id, [['name', 'shared_libs'], ['description', 'Librerie condivise per Esecuzione Contratti'], ['classPath', jar_file_list]])

AdminConfig.save()

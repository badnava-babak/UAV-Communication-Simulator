set(name takeoff-and-land-simple-example)
set(source_files ${name}.cc)
#set(header_files)
set(libraries_to_link ${libardupilot})
build_lib_example(
        NAME "${name}"
        SOURCE_FILES "${source_files}"
        LIBRARIES_TO_LINK "${libraries_to_link}")


set(name takeoff-and-land-application-example)
set(source_files ${name}.cc)
#set(header_files)
set(libraries_to_link ${libardupilot} ${liblte})
build_lib_example(
        NAME "${name}"
        SOURCE_FILES "${source_files}"
        LIBRARIES_TO_LINK "${libraries_to_link}")



set(name custom-scenario-example)
set(source_files
        ${name}.cc
        custom/custom-scenario.cc
        custom/custom-scenario-network-technology-helper.cc
        custom/custom-scenario-lte-helper.cc
        custom/custom-scenario-application-helper.cc
        )
set(header_files
        custom/custom-scenario.h
        custom/custom-scenario-network-technology-helper.h
        custom/custom-scenario-lte-helper.h
        custom/custom-scenario-application-helper.h
        )
set(libraries_to_link ${libardupilot} ${liblte})
build_lib_example(
        NAME "${name}"
        SOURCE_FILES "${source_files}"
        HEADER_FILES "${header_files}"
        LIBRARIES_TO_LINK "${libraries_to_link}")




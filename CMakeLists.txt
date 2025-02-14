check_include_file_cxx(stdint.h HAVE_STDINT_H)
if (HAVE_STDINT_H)
    add_definitions(-DHAVE_STDINT_H)
    #        add_definitions("-Wall -Wextra -Werror")
endif ()
set(CMAKE_VERBOSE_MAKEFILE ON)

set(name ardupilot)

set(source_files
        model/ardupilot.cc
        model/proto/telemetry-message.pb.cc
        model/proto/control-message.pb.cc
        model/UAVApp.cc
        model/GCSApp.cc
        model/UAVSimInfo.cc
        model/scenario-definition.cc
        model/psc-application-helper.cc
        model/psc-application.cc
        model/psc-application-configuration.cc
        model/my-constant-position-mobility-model.cc
        helper/ardupilot-helper.cc
        helper/ardupilot-network-helper.cc
        )

set(header_files
        model/ardupilot.h
        model/proto/telemetry-message.pb.h
        model/proto/control-message.pb.h
        model/UAVApp.h
        model/GCSApp.h
        model/UAVSimInfo.h
        model/scenario-definition.h
        model/psc-application-helper.h
        model/psc-application.h
        model/psc-application-configuration.h
        model/my-constant-position-mobility-model.h
        helper/ardupilot-helper.h
        helper/ardupilot-network-helper.h
        )


# only this line was needed, but in order for this line to work we need to make sure that the C++ linker is aware of mavsdk
# so '/usr/local/lib' needs to be added to LD_LIBRARY_PATH
# before using also look at proto/Readme.md and install protobuf. Just make sure one version of protobuf is installed on the system.


link_libraries(mavsdk protobuf)

set(libraries_to_link
        ${libcore}
        )

if (${ENABLE_EXAMPLES})
    set(examples_as_tests_sources
            #test/ardupilot-examples-test-suite.cc
            )
endif ()

set(test_sources
        test/ardupilot-test-suite.cc
        ${examples_as_tests_sources}
        )

build_lib(
        LIBNAME "${name}"
        SOURCE_FILES "${source_files}"
        HEADER_FILES "${header_files}"
        LIBRARIES_TO_LINK "${libraries_to_link}"
        TEST_SOURCES "${test_sources}"
)

cmake_minimum_required(VERSION 3.5)
project(Mp3Processor C)

set(CMAKE_C_STANDARD 99)
set(CMAKE_C_STANDARD_REQUIRED ON)

add_executable(mp3processor)

target_include_directories(mp3processor
    PRIVATE 
        include
    )
target_sources(mp3processor 
    PRIVATE
        source/main.c
        source/file_operations.c
        source/cyclic_redundancy_check.c
    )

if (APPLE)
    set(EXECUTABLE_OUTPUT_PATH ${CMAKE_SOURCE_DIR}/bin/Mac)
    target_link_libraries(mp3processor m)
elseif (WIN32)
    set(EXECUTABLE_OUTPUT_PATH ${CMAKE_SOURCE_DIR}/bin/Win)
endif ()

cmake_minimum_required(VERSION 4.0)
project(README)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

include(FetchContent)
FetchContent_Declare(
  pugixml
  GIT_REPOSITORY https://github.com/zeux/pugixml.git
  GIT_TAG v1.15
)
set(CMAKE_EXPORT_COMPILE_COMMANDS True)
FetchContent_MakeAvailable(pugixml)

add_executable(${PROJECT_NAME} main.cpp)
target_link_libraries(${PROJECT_NAME} PRIVATE pugixml)

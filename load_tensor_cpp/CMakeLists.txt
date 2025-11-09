cmake_minimum_required(VERSION 3.18 FATAL_ERROR)
project(load_tensor)

find_package(Torch PATHS "/mnt/data/usrApp/anaconda3/lib/python3.12/site-packages/torch/share/cmake/Torch" REQUIRED)

add_executable(load_main load_tensor.cpp)

# 链接CUDA库
target_link_libraries(load_main PRIVATE
    ${TORCH_LIBRARIES}  # PyTorch核心库
)

target_include_directories(load_main PRIVATE
    ${TORCH_INCLUDE_DIRS}  # PyTorch头文件
)
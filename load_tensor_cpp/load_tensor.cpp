#include<iostream>
#include<fstream>
#include<string>
#include<vector>
#include <torch/torch.h>

enum TorchType {
    INT32,
    FP16,
    BF16,
    FP32
};

template<class T>
T read_data(std::fstream& file_handle) {
    T ret;
    file_handle.read((char*)&ret, sizeof(T));
    return ret;
}

uint32_t get_elem_size(TorchType torch_type) {
    if(torch_type == TorchType::INT32 || torch_type == TorchType::FP32) {
        return 4;
    }
    return 2;
}

torch::Dtype map_dtype(TorchType torch_type) {
    if(torch_type == TorchType::INT32) {
        return torch::kInt;
    }
    else if(torch_type == TorchType::FP16) {
        return torch::kHalf;
    }
    else if(torch_type == TorchType::BF16) {
        return torch::kBFloat16;
    }
    return torch::kFloat32;
}

torch::Tensor init_tensor(std::vector<int> shape, TorchType torch_type) {
    auto options = torch::TensorOptions().dtype(map_dtype(torch_type));
    // 需要使用int64来初始化tensor
    std::vector<int64_t> shape_vec;
    shape_vec.reserve(shape.size());
    for(auto each_dim : shape) shape_vec.push_back(each_dim);
    torch::Tensor tensor = torch::empty(shape_vec, options);
    
    return tensor;
}

// 从文件中加载q tensor
void load_tensor_from_simple(std::string filePath, TorchType torch_type) {
    // 读取文件
    std::fstream file_handle(filePath, std::ios::in|std::ios::binary);
    int dim_num = read_data<int>(file_handle);
    // 读取每个维度
    std::vector<int> dims(dim_num);
    uint32_t total_elem_num = 1;
    for(uint32_t id_dim=0;id_dim<dim_num;++id_dim) {
        dims[id_dim] = read_data<int>(file_handle);
        total_elem_num*=dims[id_dim];
    }

    // 读取完整的数据
    uint32_t elem_size = get_elem_size(torch_type);
    // 根据大小初始化tensor
    torch::Tensor tensor = init_tensor(dims, torch_type);

    // 读取torch的实际数据
    file_handle.read((char*)tensor.data_ptr(), elem_size*total_elem_num);

    std::cout<<"dim content"<<std::endl;
    for(auto id_dim=0;id_dim<dims.size();++id_dim) {
        std::cout<<dims[id_dim]<<" ";
    }
    std::cout<<std::endl;

    // 打印tensor内容
    // std::cout<<tensor<<std::endl;
}

int main() {
    load_tensor_from_simple("/mnt/data/temp/q.bin", TorchType::BF16);
}
#include <iostream>
#include <string>
#include <stdexcept>

void printPaddedString(const std::string& inputStr, size_t targetLength) {
    // 检查输入字符串长度是否超过目标长度
    if (inputStr.length() > targetLength) {
        throw std::invalid_argument("错误：字符串长度超过指定字符数！");
    }
    
    // 创建结果字符串，初始化为输入字符串
    std::string result = inputStr;
    
    // 补足空格到目标长度
    result.append(targetLength - inputStr.length(), ' ');
    
    // 打印到控制台
    std::cout << result << std::endl;
}


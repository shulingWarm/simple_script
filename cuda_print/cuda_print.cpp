#include <stdio.h>
#include <cuda_runtime.h>

void printGPUProperties(cudaDeviceProp& prop) {
    printf("╔══════════════════════════════════════════════════════════╗\n");
    printf("║ GPU Information                                          ║\n");
    printf("╠══════════════════════════════════════════════════════════╣\n");
    printf("║ GPU Name:              %-30s ║\n", prop.name);
    printf("║ Compute Capability:    %d.%d                              ║\n", prop.major, prop.minor);
    printf("║ SMs (Multiprocessors): %-30d ║\n", prop.multiProcessorCount);
    printf("╠══════════════════════════════════════════════════════════╣\n");
    printf("║ Register Information                                     ║\n");
    printf("╠══════════════════════════════════════════════════════════╣\n");
    printf("║ Total registers per SM:     %-28d ║\n", prop.regsPerMultiprocessor);
    printf("║ Max registers per block:    %-28d ║\n", prop.regsPerBlock);
    
    // 处理不同CUDA版本中regsPerThread字段的差异
    #ifdef __CUDACC__
    #if (CUDA_VERSION >= 11000) || (defined(__CUDA_ARCH__) && __CUDA_ARCH__ >= 700)
    // CUDA 11.0+ 或 Compute Capability 7.0+ 支持regsPerThread
    printf("║ Max registers per thread:   %-28d ║\n", prop.regsPerThread);
    #else
    printf("║ Max registers per thread:   255 (default limit)         ║\n");
    #endif
    #else
    printf("║ Max registers per thread:   255 (default limit)         ║\n");
    #endif
    
    printf("║ Warp size:                  %-28d ║\n", prop.warpSize);
    printf("║ Max threads per SM:         %-28d ║\n", prop.maxThreadsPerMultiProcessor);
    printf("║ Max warps per SM:           %-28d ║\n", 
           prop.maxThreadsPerMultiProcessor / prop.warpSize);
    
    // 计算不同架构的详细信息
    int regsPerSM = prop.regsPerMultiprocessor;
    int warp_size = prop.warpSize;
    int maxWarpsPerSM = prop.maxThreadsPerMultiProcessor / warp_size;
    
    // 如果每个线程使用最大寄存器数（通常是255）
    int maxRegsPerThread = 255;  // CUDA编译器限制的最大值
    int maxThreadsUsingMaxRegs = regsPerSM / maxRegsPerThread;
    int maxWarpsUsingMaxRegs = maxThreadsUsingMaxRegs / warp_size;
    
    printf("║ Max threads (255 regs/thread): %-24d ║\n", maxThreadsUsingMaxRegs);
    printf("║ Max warps (255 regs/thread):   %-24d ║\n", maxWarpsUsingMaxRegs);
    
    // 添加共享内存信息
    printf("║ Shared Memory per SM:      %-28d KB ║\n", prop.sharedMemPerMultiprocessor / 1024);
    printf("║ Max Shared Memory per Block: %-25d KB ║\n", prop.sharedMemPerBlock / 1024);
    printf("║ Max Threads per Block:      %-28d ║\n", prop.maxThreadsPerBlock);
    
    printf("╚══════════════════════════════════════════════════════════╝\n\n");
}

int main() {
    int deviceCount;
    cudaGetDeviceCount(&deviceCount);
    
    if (deviceCount == 0) {
        printf("No CUDA-capable devices found.\n");
        return 1;
    }
    
    for (int device = 0; device < deviceCount; ++device) {
        cudaDeviceProp prop;
        cudaGetDeviceProperties(&prop, device);
        printf("\nDevice %d:\n", device);
        printGPUProperties(prop);
    }
    
    return 0;
}
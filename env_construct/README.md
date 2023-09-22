
# 环境部署

## 1. RedHat EL环境部署

### 1.1 安装docker容器引擎
步骤：
1. 更新yum

    `sudo yum update`
2. 安装docker

    `curl -sSL https://get.docker.com/ | sh`

### 1.2 安装nvidia和cuda驱动
步骤：
1. 确认系统是否支持GPU
   ```
   # lspci | grep -i nvidia
   > 88:00.0 3D controller: NVIDIA Corporation GV100GL [Tesla V100 PCIe 32GB] (rev a1)
   > 89:00.0 3D controller: NVIDIA Corporation GV100GL [Tesla V100 PCIe 32GB] (rev a1)
   > b2:00.0 3D controller: NVIDIA Corporation GV100GL [Tesla V100 PCIe 32GB] (rev a1)
   ```
2. 确认系统版本
   ```
   # uname -m && cat /etc/*release
   x86_64
   CentOS Linux release 7.9.2009 (Core)
   NAME="CentOS Linux"
   VERSION="7 (Core)"
   ID="centos"
   ID_LIKE="rhel fedora"
   VERSION_ID="7"
   PRETTY_NAME="CentOS Linux 7 (Core)"
   ANSI_COLOR="0;31"
   CPE_NAME="cpe:/o:centos:centos:7"
   HOME_URL="https://www.centos.org/"
   BUG_REPORT_URL="https://bugs.centos.org/"
   
   CENTOS_MANTISBT_PROJECT="CentOS-7"
   CENTOS_MANTISBT_PROJECT_VERSION="7"
   REDHAT_SUPPORT_PRODUCT="centos"
   REDHAT_SUPPORT_PRODUCT_VERSION="7"
   
   CentOS Linux release 7.9.2009 (Core)
   CentOS Linux release 7.9.2009 (Core)  
   ```
3. 确认安装GCC版本
   ```
   # gcc --version
   > gcc (GCC) 4.8.5 20150623 (Red Hat 4.8.5-44)
   > Copyright (C) 2015 Free Software Foundation, Inc.
   > This is free software; see the source for copying conditions.  There is NO
   > warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
   ```
4. 系统安装kernel相关package
   ```
   # yum install kernel-devel-$(uname -r) kernel-headers-$(uname -r)
   ```
5. 下载NVIDIA CUDA Toolkit

   地址：[nvidia官网](https://www.nvidia.cn/Download/index.aspx?lang=cn#)
   
   如图所示：
![img.png](img.png)

6. 本地安装
   ```shell
   # rpm -ivh nvidia-driver-local-repo-rhel7-418.226.00-1.0-1.x86_64.rpm
   ```
7. 安装vulkan-filesystem

   vulkan-filesystem为第3方提供的package，并非Redhat提供的package，因此直接centos的网站上下载rpm包，进行安装。
   ```
   # yum install wget
   # wget http://mirror.centos.org/centos/7/os/x86_64/Packages/vulkan-filesystem-1.1.97.0-1.el7.noarch.rpm
   # yum localinstall vulkan-filesystem-1.1.97.0-1.el7.noarch.rpm
   ```
8. 安装nvidia-driver-latest-dkms
   ```
   # yum install nvidia-driver-latest-dkms
   ```
9. 安装cuda-drivers

   yum命令安装cuda-drivers，在这里使用本地的nvidia-driver-local-rhel7-418.226.00.repo，因此指定–disablerepo=rhel-7-server-rpms。
   ```
   # yum --disablerepo=rhel-7-server-rpms install cuda-drivers
   ```
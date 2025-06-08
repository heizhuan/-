# 虚拟机环境搭建指南

## 一、VMware安装

1. 下载VMware Workstation
   - 访问官网：https://www.vmware.com/products/workstation-pro.html
   - 下载最新版本
   - 运行安装程序，按提示完成安装

2. 安装许可证
   - 启动VMware
   - 输入许可证密钥
   - 完成激活

## 二、CentOS安装

1. 下载CentOS 7
   - 访问：https://www.centos.org/download/
   - 选择CentOS 7 ISO
   - 下载DVD ISO镜像

2. 创建虚拟机
   ```
   步骤1: 打开VMware，选择"创建新的虚拟机"
   步骤2: 选择"典型配置"
   步骤3: 选择"安装光盘映像文件"，选择下载的ISO文件
   步骤4: 选择安装位置
   步骤5: 设置磁盘大小：50GB
   步骤6: 自定义硬件：
         - 内存：4GB
         - 处理器：2核
         - 网络适配器：桥接模式
   ```

3. 安装CentOS
   ```
   步骤1: 选择语言：中文
   步骤2: 设置分区：
         - /boot: 1GB
         - swap: 4GB
         - /: 剩余空间
   步骤3: 设置网络：开启网络
   步骤4: 设置时区：Asia/Shanghai
   步骤5: 设置root密码
   步骤6: 创建普通用户
   ```

4. 基础配置

   a. 更新系统
   ```bash
   sudo yum update -y
   ```

   b. 安装基础工具
   ```bash
   sudo yum install -y wget net-tools vim
   ```

   c. 配置网络
   ```bash
   # 编辑网络配置
   sudo vim /etc/sysconfig/network-scripts/ifcfg-ens33

   # 修改以下内容
   BOOTPROTO=static
   ONBOOT=yes
   IPADDR=192.168.1.100  # 根据实际网络修改
   NETMASK=255.255.255.0
   GATEWAY=192.168.1.1
   DNS1=8.8.8.8
   ```

   d. 配置主机名
   ```bash
   # 设置主机名
   sudo hostnamectl set-hostname hadoop-master

   # 编辑hosts文件
   sudo vim /etc/hosts
   # 添加以下内容
   192.168.1.100 hadoop-master
   ```

5. 安全配置

   a. 配置防火墙
   ```bash
   # 开启防火墙
   sudo systemctl start firewalld
   sudo systemctl enable firewalld

   # 开放必要端口
   sudo firewall-cmd --zone=public --add-port=22/tcp --permanent
   sudo firewall-cmd --reload
   ```

   b. 配置SELinux
   ```bash
   # 编辑SELinux配置
   sudo vim /etc/selinux/config
   # 修改
   SELINUX=permissive
   ```

6. 创建项目目录
   ```bash
   # 创建项目目录
   mkdir -p ~/ecommerce_analysis
   cd ~/ecommerce_analysis
   ```

## 三、验证安装

1. 检查系统信息
   ```bash
   # 查看系统版本
   cat /etc/redhat-release

   # 查看内存
   free -h

   # 查看磁盘
   df -h

   # 查看网络
   ip addr
   ```

2. 检查网络连接
   ```bash
   # 测试网络连通性
   ping www.baidu.com
   ```

## 四、注意事项

1. 确保虚拟机有足够的资源（CPU、内存、磁盘空间）
2. 网络配置要根据实际环境调整
3. 定期创建虚拟机快照，方便恢复
4. 记录下所有配置的密码和重要参数 
# Basis: ROS 2 Humble Desktop
FROM osrf/ros:humble-desktop-full

# Vermeidung von Benutzerinteraktionen während der Installation
ENV DEBIAN_FRONTEND=noninteractive

# 1. System-Updates & Essentielle Build-Tools
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    python3-colcon-common-extensions \
    python3-pip \
    python3-rosdep \
    python3-vcstool \
    wget \
    gnupg2 \
    lsb-release \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 2. Hardware-nahe Tools & micro-ROS Support
RUN apt-get update && apt-get install -y \
    picocom \
    minicom \
    libgoogle-glog-dev \
    libgtest-dev \
    cppcheck \
    clang-format \
    gdb \
    udev \
    && rm -rf /var/lib/apt/lists/*

# 3. ROS 2 Dependencies & Navigation Stack
RUN apt-get update && apt-get install -y \
    ros-humble-navigation2 \
    ros-humble-nav2-bringup \
    ros-humble-ros2-control \
    ros-humble-ros2-controllers \
    ros-humble-xacro \
    && rm -rf /var/lib/apt/lists/*

# 4. Workspace-Setup
ARG USERNAME=developer
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Erstelle Non-Root User und füge ihn der Gruppe 'dialout' hinzu
# Das ist ESSENZIELL für USB-Zugriff ohne sudo
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && usermod -aG dialout $USERNAME \
    && apt-get update && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Automatische ROS 2 Source-Einträge
RUN echo "source /opt/ros/humble/setup.bash" >> /home/$USERNAME/.bashrc

USER $USERNAME
WORKDIR /workspace

# Initialisiere rosdep (als User)
RUN rosdep update

CMD ["bash"]
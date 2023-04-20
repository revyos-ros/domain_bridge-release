%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/iron/.*$
%global __requires_exclude_from ^/opt/ros/iron/.*$

Name:           ros-iron-domain-bridge
Version:        0.5.0
Release:        4%{?dist}%{?release_suffix}
Summary:        ROS domain_bridge package

License:        Apache 2.0
Source0:        %{name}-%{version}.tar.gz

Requires:       ros-iron-rclcpp
Requires:       ros-iron-rclcpp-components
Requires:       ros-iron-rcutils
Requires:       ros-iron-rosbag2-cpp
Requires:       ros-iron-rosidl-default-runtime
Requires:       ros-iron-rosidl-typesupport-cpp
Requires:       ros-iron-zstd-vendor
Requires:       yaml-cpp-devel
Requires:       ros-iron-ros-workspace
BuildRequires:  ros-iron-ament-cmake
BuildRequires:  ros-iron-rclcpp
BuildRequires:  ros-iron-rclcpp-components
BuildRequires:  ros-iron-rcutils
BuildRequires:  ros-iron-rosbag2-cpp
BuildRequires:  ros-iron-rosidl-default-generators
BuildRequires:  ros-iron-rosidl-typesupport-cpp
BuildRequires:  ros-iron-zstd-vendor
BuildRequires:  yaml-cpp-devel
BuildRequires:  ros-iron-ros-workspace
BuildRequires:  ros-iron-rosidl-typesupport-fastrtps-c
BuildRequires:  ros-iron-rosidl-typesupport-fastrtps-cpp
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}
Provides:       ros-iron-rosidl-interface-packages(member)

%if 0%{?with_tests}
BuildRequires:  ros-iron-ament-cmake-gmock
BuildRequires:  ros-iron-ament-lint-auto
BuildRequires:  ros-iron-ament-lint-common
BuildRequires:  ros-iron-example-interfaces
BuildRequires:  ros-iron-launch
BuildRequires:  ros-iron-launch-testing
BuildRequires:  ros-iron-launch-testing-ament-cmake
BuildRequires:  ros-iron-rmw-cyclonedds-cpp
BuildRequires:  ros-iron-rmw-fastrtps-cpp
BuildRequires:  ros-iron-rmw-implementation-cmake
BuildRequires:  ros-iron-rosgraph-msgs
BuildRequires:  ros-iron-test-msgs
%endif

%if 0%{?with_weak_deps}
Supplements:    ros-iron-rosidl-interface-packages(all)
%endif

%description
ROS 2 Domain Bridge

%prep
%autosetup -p1

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/iron/setup.sh" ]; then . "/opt/ros/iron/setup.sh"; fi
mkdir -p .obj-%{_target_platform} && cd .obj-%{_target_platform}
%cmake3 \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_PREFIX="/opt/ros/iron" \
    -DAMENT_PREFIX_PATH="/opt/ros/iron" \
    -DCMAKE_PREFIX_PATH="/opt/ros/iron" \
    -DSETUPTOOLS_DEB_LAYOUT=OFF \
%if !0%{?with_tests}
    -DBUILD_TESTING=OFF \
%endif
    ..

%make_build

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/iron/setup.sh" ]; then . "/opt/ros/iron/setup.sh"; fi
%make_install -C .obj-%{_target_platform}

%if 0%{?with_tests}
%check
# Look for a Makefile target with a name indicating that it runs tests
TEST_TARGET=$(%__make -qp -C .obj-%{_target_platform} | sed "s/^\(test\|check\):.*/\\1/;t f;d;:f;q0")
if [ -n "$TEST_TARGET" ]; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/iron/setup.sh" ]; then . "/opt/ros/iron/setup.sh"; fi
CTEST_OUTPUT_ON_FAILURE=1 \
    %make_build -C .obj-%{_target_platform} $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif

%files
/opt/ros/iron

%changelog
* Thu Apr 20 2023 Jacob Perron <jacob@openrobotics.org> - 0.5.0-4
- Autogenerated by Bloom

* Tue Mar 21 2023 Jacob Perron <jacob@openrobotics.org> - 0.5.0-3
- Autogenerated by Bloom


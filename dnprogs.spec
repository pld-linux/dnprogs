Summary: DECnet tools and libraries
Name: dnprogs

%define dnet_major 1
%define dnet_version %{dnet_major}.2

%define dap_major 1
%define dap_version %{dap_major}.05a

%define dnprogs_version %{dap_version}

Version: %{dnprogs_version}
Release: 2
Copyright: GPL
Group: Networking/Utilities
URL: http://linux.dreamtime.org/decnet/
Source: ftp://ftp.dreamtime.org/pub/decnet/%{name}-%{version}.tar.gz
Patch0: dnprogs-1.05a-make.patch.gz
Patch1: dnprogs-1.05a-rc.patch.gz
ExclusiveOS: Linux
Prereq: /sbin/chkconfig /sbin/ldconfig
BuildRoot:	/tmp/%{name}-%{version}-root

%description
DECnet programs for Linux.

These tools are the application layer interface for DECnet on Linux systems.
They provide file/terminal access facilities between OpenVMS and Linux and 
remote execution of commands.

To use them you will need to have DECnet built into your kernel.
See http://linux.dreamtime.org/decnet/ to get the kernel patch and
instructions on how to apply it.

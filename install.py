#!/usr/bin/env python

import os
import fnmatch
import argparse
import sys
import platform

# This script need root privilege
if os.getuid() != 0:
    raise Exception("This installer script need root privilege!!!")

# Global variables
script_path = os.path.dirname(os.path.realpath(sys.argv[0]))
backupdir = os.path.join(script_path, "backup")

# Dectet arch

def os_arch():
    if(platform.machine() == 'x86_64'):
        return "amd64"
    else:
        raise Exception("This arch %s not support yet!!" % (platform.machine()))

# Exclude file list
exclude = [ 'install.py', '.git', '.directory', '.gitignore' ]


def backup(src):
    """Backup files to ./backup directory"""
    try:
        if os.path.exists(src):
            print("backup %s to %s" % (os.path.realpath(src), os.path.realpath(backupdir + src)))
            os.makedirs(os.path.realpath(backupdir + src))
            os.rename(os.path.realpath(src), os.path.realpath(backupdir + src))
    except OSError, e:
        print(type(e), str(e))


def restore(src):
    try:
        if os.path.exists(os.path.realpath(backupdir + src)):
            print("restore backup %s to %s" % (os.path.realpath(backupdir + src), os.path.realpath(src)))
            os.rename(os.path.realpath(backupdir + src), os.path.realpath(src))
    except OSError, e:
        print(type(e), str(e))


def backup_and_symlink(src, dest):
    """Symlinks file and backup old file."""
    try:
        backup(dest)
        os.symlink(src, dest)
        print("create symlink %s to %s" %(dest, src))
    except OSError, e:
        print(type(e), str(e))


def install_config(dst):
    for f in os.listdir('.'):
        if not any(fnmatch.fnmatch(f, p) for p in exclude):
            path = os.path.join(os.path.expanduser(dst), f)

            if args.uninstall:
                if os.path.isfile(path) or os.path.islink(path):
                    os.unlink(path)
                    restore(path)
            else:
                backup_and_symlink(os.path.abspath(f), path)


def main(args):
    """Install gentoo-config"""
    # install arch specific config
    os.chdir(os.path.join('./conf', os_arch() + '/etc'))
    install_config('/etc/')

    if args.uninstall:
        print("Uninstall complete!!")
    else:
        print("Install complete.")


# Main
if __name__ == "__main__":
    # make sure backupdir exist
    if not os.path.exists(backupdir):
        os.mkdir(backupdir)

    parser = argparse.ArgumentParser(description = "Install coldnew's  gentoo-config to sstem.")
    parser.add_argument("--uninstall", action="store_true",
                        help="Uninstall all files in coldnew's gentoo-config")
    args = parser.parse_args()

    main(args)

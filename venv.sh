#!/bin/bash


# GENERAL ENVIRONMENT

WORKSPACE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$WORKSPACE" || exit 1

VENV_NAME="venv"

PYTHON_BIN="python"
PYTHON_VERSION=$($PYTHON_BIN -c "import sys; print(f'python{sys.version_info.major}.{sys.version_info.minor}')")


# OS-SPECIFIC ENVIRONMENT

if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    # ------- WINDOWS ENV ------- #
    ACTIVATE_PATH="$VENV_NAME/Scripts/activate"
    VENV_PYTHON="$VENV_NAME/Scripts/python.exe"
    SITE_PACKAGES="$VENV_NAME/Lib/site-packages"
else
    # ------- LINUX ENV ------- #
    ACTIVATE_PATH="$VENV_NAME/bin/activate"
    VENV_PYTHON="$VENV_NAME/bin/python"
    SITE_PACKAGES="$VENV_NAME/lib/$PYTHON_VERSION/site-packages"
fi


# HELPER FUNCTIONS

write() {
    local content="$1"
    local target_file="$2"
    echo "$content" > "$target_file"
}

venv_activate() {
    echo "Activating VENV..."
    if [ -d "$VENV_NAME" ]; then
        source $ACTIVATE_PATH
        echo "VENV activated."
    else
        echo "VENV does not exist!"
    fi
}

venv_deactivate() {
    echo "Deactivating VENV..."
    if [ -n "$VIRTUAL_ENV" ]; then
        type deactivate >/dev/null 2>&1 && deactivate
        echo "VENV deactivated."
    else
        echo "VENV was not active!"
    fi
}

install_requirements() {
    venv_activate

    echo "Upgrading PIP..."
    $VENV_PYTHON -m pip install --upgrade pip --no-cache-dir
    echo "PIP upgraded."

    echo "Installing 'requirements.txt'..."
    if [ -f "requirements.txt" ]; then
        $VENV_PYTHON -m pip install -r requirements.txt --no-cache-dir
        echo "Requirements installed."
    fi

    venv_deactivate
}

modify_pythonpath() {
    echo "Modifying PYTHONPATH..."

    local venv_path="$(realpath "$SITE_PACKAGES")"
    local content="$(realpath --relative-to="$venv_path" "$WORKSPACE")/Lib"

    if [ ! -d "$WORKSPACE/Lib" ]; then
        echo "Directory 'Lib' could not be found in the workspace!"
        exit 1
    fi

    write "$content" "$SITE_PACKAGES/pythonpath.pth"

    echo "PYTHONPATH modified."
}


# SCRIPT FUNCTIONS

build_venv() {
    echo "Building VENV..."
    if [ -d "$VENV_NAME" ]; then
        echo "VENV already exists!"
        exit 1
    else
        $PYTHON_BIN -m venv $VENV_NAME
    fi

    install_requirements

    modify_pythonpath

    echo "Done."
}

reload_venv() {
    echo "Reloading VENV..."

    install_requirements

    modify_pythonpath

    echo "Done."
}

rebuild_venv() {
    remove_venv
    echo
    build_venv
}

remove_venv() {
    echo "Removing VENV..."

    venv_deactivate

    rm -rf $VENV_NAME

    echo "Done."

}


# SCRIPT

case "$1" in
    build)
        build_venv
        ;;
    reload)
        reload_venv
        ;;
    remove)
        remove_venv
        ;;
    rebuild)
        rebuild_venv
        ;;
    *)
        echo "Usage: venv.sh [build|reload|rebuild|remove]"
        ;;
esac

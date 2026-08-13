#!/usr/bin/bash

if [ -z "$BASEDIR" ]; then
  BASEDIR="/data/openpilot"
fi

source "$BASEDIR/launch_env.sh"

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

function agnos_init {
  # wait longer for weston to come up
  if [ -f "$BASEDIR/prebuilt" ]; then
    sleep 3
  fi

  # TODO: move this to agnos
  sudo rm -f /data/etc/NetworkManager/system-connections/*.nmmeta

  # set success flag for current boot slot
  sudo abctl --set_success

  # Check if AGNOS update is required
  if [ $(< /VERSION) != "$AGNOS_VERSION" ]; then
    AGNOS_PY="$DIR/system/hardware/tici/agnos.py"
    MANIFEST="$DIR/system/hardware/tici/agnos.json"
    if $AGNOS_PY --verify $MANIFEST; then
      sudo reboot
    fi
    $DIR/system/hardware/tici/updater $AGNOS_PY $MANIFEST
  fi
}

function build_source_ui {
  local ui_commit
  local ui_stamp="/data/ui_build_commit"
  local ui_log="/data/community/crashes/ui_source_build.txt"
  local error_log="/data/community/crashes/error.txt"
  local ui_binary="$BASEDIR/selfdrive/ui/_ui"
  local ui_backup="/tmp/openpilot_ui_prebuilt_backup"

  ui_commit="$(git -C "$BASEDIR" rev-parse HEAD 2>/dev/null)"
  [ -n "$ui_commit" ] || return 0
  [ "$(cat "$ui_stamp" 2>/dev/null)" = "$ui_commit" ] && return 0

  echo "Building source UI for $ui_commit"
  mkdir -p "$(dirname "$ui_log")"
  cp -f "$ui_binary" "$ui_backup"
  # Translation files are compiled into the generated Qt assets object. Remove
  # those generated outputs so an update cannot reuse an older embedded .qm.
  rm -f "$ui_binary" \
        "$BASEDIR/selfdrive/assets/assets.cc" \
        "$BASEDIR/selfdrive/assets/assets.o" \
        "$BASEDIR/selfdrive/ui/assets.o"

  if cd "$BASEDIR" && scons -j2 --minimal selfdrive/ui/_ui >"$ui_log" 2>&1; then
    echo "$ui_commit" > "$ui_stamp"
    rm -f "$ui_backup"
    if grep -q '^\[SOURCE UI BUILD FAILED\]' "$error_log" 2>/dev/null; then
      rm -f "$error_log"
    fi
    echo "Source UI build completed"
  else
    echo "Source UI build failed; restoring prebuilt UI"
    {
      echo "[SOURCE UI BUILD FAILED]"
      echo "Commit: $ui_commit"
      echo "The previous prebuilt UI was restored. Build log tail:"
      echo
      tail -n 120 "$ui_log"
    } > "$error_log"
    cp -f "$ui_backup" "$ui_binary"
    rm -f "$ui_backup"
  fi
}

function launch {
  # Remove orphaned git lock if it exists on boot
  [ -f "$DIR/.git/index.lock" ] && rm -f $DIR/.git/index.lock

  # Pull time from panda
  $DIR/selfdrive/boardd/set_time.py

  # Check to see if there's a valid overlay-based update available. Conditions
  # are as follows:
  #
  # 1. The BASEDIR init file has to exist, with a newer modtime than anything in
  #    the BASEDIR Git repo. This checks for local development work or the user
  #    switching branches/forks, which should not be overwritten.
  # 2. The FINALIZED consistent file has to exist, indicating there's an update
  #    that completed successfully and synced to disk.

  if [ -f "${BASEDIR}/.overlay_init" ]; then
    find ${BASEDIR}/.git -newer ${BASEDIR}/.overlay_init | grep -q '.' 2> /dev/null
    if [ $? -eq 0 ]; then
      echo "${BASEDIR} has been modified, skipping overlay update installation"
    else
      if [ -f "${STAGING_ROOT}/finalized/.overlay_consistent" ]; then
        if [ ! -d /data/safe_staging/old_openpilot ]; then
          echo "Valid overlay update found, installing"
          LAUNCHER_LOCATION="${BASH_SOURCE[0]}"

          mv $BASEDIR /data/safe_staging/old_openpilot
          mv "${STAGING_ROOT}/finalized" $BASEDIR
          cd $BASEDIR

          echo "Restarting launch script ${LAUNCHER_LOCATION}"
          unset AGNOS_VERSION
          exec "${LAUNCHER_LOCATION}"
        else
          echo "openpilot backup found, not updating"
          # TODO: restore backup? This means the updater didn't start after swapping
        fi
      fi
    fi
  fi

  # handle pythonpath
  ln -sfn $(pwd) /data/pythonpath
  export PYTHONPATH="$PWD"

  # hardware specific init
  agnos_init

  # This release keeps the proven prebuilt driving stack and model, while the
  # restored UI source is rebuilt once per Git revision.
  build_source_ui

  # write tmux scrollback to a file
  tmux capture-pane -pq -S-1000 > /tmp/launch_log

  # start manager
  cd selfdrive/manager
  ./build.py && ./mapd_installer.py && ./manager.py
  # if broken, keep on screen error
  while true; do sleep 1; done
}

launch

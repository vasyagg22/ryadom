#!/usr/bin/env bash
set -euo pipefail
dump_startup_logs() {
  echo "::group::Android startup diagnostics"
  adb logcat -d -v threadtime | grep -E -A 22 'FATAL EXCEPTION|AndroidRuntime|ReactNativeJS|SoLoader|UnsatisfiedLinkError|No Firebase App|Process: app\.duo\.offlineai|am_crash|F libc' | tail -n 280 || true
  adb shell dumpsys activity exit-info app.duo.offlineai | tail -n 130 || true
  echo "::endgroup::"
}
apk="$(find pocketpal/android/app/build/outputs/apk/prod/release -type f -name '*.apk' | head -n 1)"
test -s "$apk"
adb install -r "$apk"
adb logcat -c
echo "Starting app on emulator"
if ! adb shell am start -n app.duo.offlineai/com.pocketpal.MainActivity; then
  echo "::error::Android refused to start the app activity"
  dump_startup_logs
  exit 1
fi
sleep 25
if ! adb shell pidof app.duo.offlineai; then
  echo "::error::App crashed or exited during smoke test"
  dump_startup_logs
  exit 1
fi
echo "SMOKE_TEST_PASS app.duo.offlineai"

#!/usr/bin/env python3
"""Configure Android build.gradle.kts: arm64-only + release without R8/shrink (match working APK)."""
import sys

gradle_file = 'src-tauri/gen/android/app/build.gradle.kts'
content = open(gradle_file).read()

# 1. Restrict ABI to arm64-v8a only
if 'abiFilters' not in content:
    content = content.replace(
        'defaultConfig {',
        'defaultConfig {\n        ndk { abiFilters += listOf("arm64-v8a") }'
    )
    print('Added ABI filter: arm64-v8a only')

# 2. Add release signing config with v1+v2 signing
signing = '''    signingConfigs {
        create("release") {
            storeFile = file(System.getenv("HOME") + "/paidx.keystore")
            storePassword = "paidx123"
            keyAlias = "paidx"
            keyPassword = "paidx123"
            enableV1Signing = true
            enableV2Signing = true
        }
    }
'''
if 'signingConfigs' not in content:
    content = content.replace('    buildTypes {', signing + '    buildTypes {')
    print('Added signingConfigs with v1+v2 signing')

# 3. Configure release: use signing, disable R8/minify/shrink
if 'signingConfig = signingConfigs.getByName("release")' not in content:
    content = content.replace(
        'getByName("release") {',
        'getByName("release") {\n'
        '            signingConfig = signingConfigs.getByName("release")\n'
        '            isMinifyEnabled = false\n'
        '            isShrinkResources = false'
    )
    print('Configured release: signing + R8 disabled + shrink disabled')

open(gradle_file, 'w').write(content)
print('Done: gradle config matches working APK')

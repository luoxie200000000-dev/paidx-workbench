#!/usr/bin/env python3
"""Configure Android build.gradle.kts for arm64-only release builds."""
import os

gradle_file = 'src-tauri/gen/android/app/build.gradle.kts'
content = open(gradle_file).read()

# 1. Restrict ABI to arm64-v8a only
if 'abiFilters' not in content:
    content = content.replace(
        'defaultConfig {',
        'defaultConfig {\n        ndk { abiFilters += listOf("arm64-v8a") }'
    )

# 2. Add release signing config
signing = '''    signingConfigs {
        create("release") {
            storeFile = file(System.getenv("HOME") + "/paidx.keystore")
            storePassword = "paidx123"
            keyAlias = "paidx"
            keyPassword = "paidx123"
        }
    }
'''
if 'signingConfigs' not in content:
    content = content.replace('    buildTypes {', signing + '    buildTypes {')

# 3. Configure release build type to use signing
if 'signingConfig = signingConfigs.getByName("release")' not in content:
    content = content.replace(
        'getByName("release") {',
        'getByName("release") {\n            signingConfig = signingConfigs.getByName("release")'
    )

open(gradle_file, 'w').write(content)
print('Gradle config updated: arm64-v8a only + release signing')

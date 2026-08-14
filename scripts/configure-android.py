#!/usr/bin/env python3
"""Configure Android build.gradle.kts: arm64-only + release without R8 (match working APK)."""
import re

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

# 3. Replace isMinifyEnabled = true -> false (regex overrides existing setting)
content = re.sub(r'isMinifyEnabled\s*=\s*true', 'isMinifyEnabled = false', content)
print('Set isMinifyEnabled = false (disable R8)')

# 4. Add signingConfig to release buildType
if 'signingConfig = signingConfigs.getByName("release")' not in content:
    content = content.replace(
        'getByName("release") {',
        'getByName("release") {\n            signingConfig = signingConfigs.getByName("release")'
    )
    print('Added signingConfig to release buildType')

open(gradle_file, 'w').write(content)
print('Done')

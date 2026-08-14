#!/usr/bin/env python3
"""Configure Android build.gradle.kts: arm64-only + release without R8/shrink/crunch."""
import re

gradle_file = 'src-tauri/gen/android/app/build.gradle.kts'
content = open(gradle_file).read()

print('=== ORIGINAL build.gradle.kts ===')
print(content)
print('=== END ORIGINAL ===')

# 1. Restrict ABI to arm64-v8a only
if 'abiFilters' not in content:
    content = content.replace(
        'defaultConfig {',
        'defaultConfig {\n        ndk { abiFilters += listOf("arm64-v8a") }'
    )
    print('Added ABI filter: arm64-v8a only')

# 2. Add release signing config
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
    print('Added signingConfigs')

# 3. Replace isMinifyEnabled = true -> false (regex to override existing setting)
content = re.sub(r'isMinifyEnabled\s*=\s*true', 'isMinifyEnabled = false', content)
print('Set isMinifyEnabled = false')

# 4. Replace isShrinkResources = true -> false
content = re.sub(r'isShrinkResources\s*=\s*true', 'isShrinkResources = false', content)
print('Set isShrinkResources = false')

# 5. Add signingConfig to release buildType + crunchPngs = false
if 'signingConfig = signingConfigs.getByName("release")' not in content:
    content = content.replace(
        'getByName("release") {',
        'getByName("release") {\n'
        '            signingConfig = signingConfigs.getByName("release")\n'
        '            crunchPngs = false'
    )
    print('Added signingConfig + crunchPngs=false to release')

# 6. Also disable crunchPngs globally for release
if 'crunchPngs' not in content:
    content = content.replace(
        'getByName("release") {',
        'getByName("release") {\n            crunchPngs = false'
    )

open(gradle_file, 'w').write(content)

print()
print('=== MODIFIED build.gradle.kts ===')
print(content)
print('=== END MODIFIED ===')

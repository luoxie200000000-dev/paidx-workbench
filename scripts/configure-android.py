#!/usr/bin/env python3
"""Configure Android build.gradle.kts: arm64-v8a only (match working debug APK)."""
gradle_file = 'src-tauri/gen/android/app/build.gradle.kts'
content = open(gradle_file).read()

if 'abiFilters' not in content:
    content = content.replace(
        'defaultConfig {',
        'defaultConfig {\n        ndk { abiFilters += listOf("arm64-v8a") }'
    )
    print('Added ABI filter: arm64-v8a only')
else:
    print('ABI filter already present')

open(gradle_file, 'w').write(content)

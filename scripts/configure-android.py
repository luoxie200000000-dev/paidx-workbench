#!/usr/bin/env python3
"""Configure Android build.gradle.kts:
- arm64-v8a only (modern Android phones)
- Disable R8 minify + resource shrink (caused crash and missing icons)
- Release signed with debug keystore, v1+v2 signatures (matches working APK)
"""
import re

gradle_file = 'src-tauri/gen/android/app/build.gradle.kts'
content = open(gradle_file).read()
original = content

# 1. arm64-v8a only
if 'abiFilters' not in content:
    content = content.replace(
        'defaultConfig {',
        'defaultConfig {\n        ndk { abiFilters += listOf("arm64-v8a") }'
    )
    print('Added ABI filter: arm64-v8a only')
else:
    print('ABI filter already present')

# 2. Disable R8 minify (regex replace so the template's `true` is actually overridden)
content, n = re.subn(r'isMinifyEnabled\s*=\s*true', 'isMinifyEnabled = false', content)
print(f'minifyEnabled -> false: {n} replacement(s)')

# 3. Disable resource shrink (only effective when minify on, but disable explicitly)
if re.search(r'isShrinkResources\s*=\s*true', content):
    content, n = re.subn(r'isShrinkResources\s*=\s*true', 'isShrinkResources = false', content)
    print(f'shrinkResources -> false: {n} replacement(s)')
else:
    content = content.replace(
        'isMinifyEnabled = false',
        'isMinifyEnabled = false\n            isShrinkResources = false',
        1,
    )
    print('Added isShrinkResources = false')

# 4. Release build signed with debug keystore (v1+v2 signing on by default)
m = re.search(r'create\("release"\)\s*\{', content)
if m and 'signingConfig' not in content.split('create("release")')[1][:2000]:
    content = re.sub(
        r'(create\("release"\)\s*\{)',
        r'\1\n            signingConfig = signingConfigs.getByName("debug")',
        content,
        count=1,
    )
    print('Release build now signed with debug keystore')

if content != original:
    open(gradle_file, 'w').write(content)
    print('build.gradle.kts updated')

print('\n===== Modified buildTypes/signingConfigs section =====')
for section in ['signingConfigs', 'buildTypes']:
    idx = content.find(section)
    if idx >= 0:
        print(content[idx:idx + 700])
        print('...')

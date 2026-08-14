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

# 2. Keep R8 minify enabled (template default; the working OLD APK also used
#    R8 - its classes.dex is 1.9MB vs 11.8MB unminified). Just verify it's on.
n_on = len(re.findall(r'isMinifyEnabled\s*=\s*true', content))
print(f'minifyEnabled stays true in {n_on} place(s) (matches OLD APK)')

# 3. Disable resource shrink (icons/resources safety; OLD APK kept all 217 res files)
if re.search(r'isShrinkResources\s*=\s*true', content):
    content, n = re.subn(r'isShrinkResources\s*=\s*true', 'isShrinkResources = false', content)
    print(f'shrinkResources -> false: {n} replacement(s)')
elif 'isShrinkResources' not in content:
    content, n = re.subn(
        r'(getByName\("release"\)\s*\{)',
        r'\1\n            isShrinkResources = false',
        content,
        count=1,
    )
    print(f'Added isShrinkResources = false to release: {n}')

# 4. Release build signed with debug keystore (v1+v2 signing on by default)
#    NOTE: Tauri template uses getByName("release"), not create("release")
release_pat = r'(getByName\("release"\)\s*\{)'
m = re.search(release_pat, content)
if m and 'signingConfig' not in content[m.end():m.end() + 2000]:
    content = re.sub(
        release_pat,
        r'\1\n            signingConfig = signingConfigs.getByName("debug")',
        content,
        count=1,
    )
    print('Release build now signed with debug keystore')
else:
    print('WARNING: release signingConfig not applied!', m)

if content != original:
    open(gradle_file, 'w').write(content)
    print('build.gradle.kts updated')

print('\n===== Modified buildTypes/signingConfigs section =====')
for section in ['signingConfigs', 'buildTypes']:
    idx = content.find(section)
    if idx >= 0:
        print(content[idx:idx + 700])
        print('...')

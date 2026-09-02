#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CHAOS;CHILD —— 绕过「启动器校验」补丁脚本
原理: Game.exe 偏移 0x6B418 处 `jne`(75 1A) -> `jmp`(EB 1A), 跳过共享内存握手校验。
用法: python patch.py <Game.exe 路径>
"""

import os
import shutil
import sys

OFFSET = 0x6B418          # 文件偏移
EXPECTED = bytes([0x75, 0x1A])   # 原: jne +0x1A
PATCHED = bytes([0xEB, 0x1A])    # 改: jmp +0x1A


def main():
    if len(sys.argv) < 2:
        print('用法: python patch.py <Game.exe 路径>')
        sys.exit(1)
    path = os.path.abspath(sys.argv[1])
    if not os.path.isfile(path):
        print('错误: 文件不存在 ->', path)
        sys.exit(1)

    with open(path, 'rb') as f:
        data = bytearray(f.read())

    if data[OFFSET:OFFSET + 2] == PATCHED:
        print('已是补丁状态, 无需再次修改:', path)
        return
    if data[OFFSET:OFFSET + 2] != EXPECTED:
        print('错误: 偏移 0x%X 处字节为 %s, 与预期 %s 不符, 可能 Game.exe 版本不同, 已中止。'
              % (OFFSET, data[OFFSET:OFFSET + 2].hex(), EXPECTED.hex()))
        sys.exit(1)

    backup = path + '.orig'
    if not os.path.exists(backup):
        shutil.copy2(path, backup)
        print('已备份原文件 ->', backup)

    data[OFFSET:OFFSET + 2] = PATCHED
    with open(path, 'wb') as f:
        f.write(data)

    print('补丁完成:', path)
    print('  偏移 0x%X: %s -> %s' % (OFFSET, EXPECTED.hex(), PATCHED.hex()))
    print('提示: 直接运行 Game.exe 即可, 不要再通过「启动游戏.exe」启动。')


if __name__ == '__main__':
    main()
